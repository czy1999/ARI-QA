import pandas as pd
import numpy as np
import pickle
import os
import openai
from prompt import action_templates,SUMMARY_INSTRUCTION
import json
import pandas as pd
from sklearn.cluster import KMeans
from utils import MultiTQ
from sentence_transformers import SentenceTransformer
from sentence_transformers import  util
import torch
import numpy as np
from tqdm import tqdm
from utils import chatgpt,gpt4
import pandas as pd
import numpy as np
import re
import time



def get_actions(head_text, rel_texts, tail_text, time, event_text, entities=None,LLM_rel_choose=None):
    choose = []
    # Iterate over all relations
    if LLM_rel_choose is not None:
        rel_texts = [LLM_rel_choose]
    for rel_text in rel_texts:
        go_for_entity = action_templates[0].replace('{head}', head_text).replace('{rel}', rel_text)
        choose.append(go_for_entity.replace('{time}', time))
        choose.append(go_for_entity.replace('{time}', 'no time constraints'))
        go_for_time = action_templates[2].replace('{head}', head_text).replace('{rel}', rel_text).replace('{tail}',tail_text)
        if 'None' not in go_for_time:
            choose.append(go_for_time)
            
        go_for_entity_tail = action_templates[0].replace('{head}', tail_text).replace('{rel}', rel_text)
        choose.append(go_for_entity_tail.replace('{time}', time))
        choose.append(go_for_entity_tail.replace('{time}', 'no time constraints'))
        go_for_time = action_templates[2].replace('{head}', tail_text).replace('{rel}', rel_text).replace('{tail}',head_text)
        if 'None' not in go_for_time:
            choose.append(go_for_time)
            
        go_for_entity_piror = action_templates[1].replace('{tail}', tail_text).replace('{rel}', rel_text)
        choose.append(go_for_entity_piror.replace('{time}', time))
        choose.append(go_for_entity_piror.replace('{time}', 'no time constraints'))

        go_for_entity_piror_tail = action_templates[1].replace('{tail}', head_text).replace('{rel}', rel_text)
        choose.append(go_for_entity_piror_tail.replace('{time}', time))
        choose.append(go_for_entity_piror_tail.replace('{time}', 'no time constraints'))
    
    if len(entities)>0:
        for i in range(3, 7):
            choose.append(action_templates[i])#.replace('{time}', time))
        # for time join entities
        # choose.append(action_templates[7]) #.replace('{start}', str(entities[0][1])).replace('{end}', str(entities[0][2])))
        for e in entities[:2]:
            if type(e) == str or type(e) == int:
                choose.append('answer({})'.format(e))
            else:
                choose.append('answer({})'.format(e[0]))
                # choose.append('answer({})'.format(e[1]))
        choose.append('answer({your specified time})')

    choose = list(set(choose))
    choose = [x for x in choose if '(None' not in x]
    choose = ['$' + x + '$' for x in choose]
    return choose


class History_Memory():
    def __init__(self,n_clusters=10,history = {}):
        # Build the semantic search model
        self.n_clusters = n_clusters
        self.embedder = SentenceTransformer('multi-qa-mpnet-base-cos-v1')
        self.kmeans = KMeans(n_clusters=self.n_clusters,n_init = 10)
        self.id2text = MultiTQ().id2text
        self.history = history
        self.k2k = list(self.history.keys())
        self.summary_prompt = SUMMARY_INSTRUCTION
        self.methodology_dict = {}
        if len(self.history)>0:
            self.update_memory(self.history)
        
    def add_memory(self,to_add):
        for i in to_add:
            self.history[i] = to_add[i]
        self.update_memory(self.history)
    
    def update_memory(self,history):
        self.history = history
        self.history_questions = []
        self.k2k = list(self.history.keys())
        for i in self.history.keys():
            q = self.history[i]['question']['question']
            entities = self.history[i]['question']['entities']
            if len(entities) == 2:
                head = self.history[i]['question']['entities'][0]
                tail = self.history[i]['question']['entities'][1]
            elif len(entities) == 1:
                head = self.history[i]['question']['entities'][0]
                tail = '$'
            else:
                head = '$'
                tail = '$'
            clean_q = self.get_clean_question(q,head,tail)
            self.history_questions.append(clean_q)
        self.fit_history_memory()
        self.summmary()
        
    def fit_history_memory(self):
        t1 = self.embedder.encode(self.history_questions, convert_to_tensor=True)
        self.kmeans.fit(t1)
        
    def predict_memory_cluster(self, new_memory):
        new_memory_vector = self.embedder.encode(new_memory)
        return self.kmeans.predict([new_memory_vector])[0]
    
    def get_cluster_index(self,index_id,correctness = [True,False]):
        candidate =  np.argwhere(self.kmeans.labels_ == index_id).flatten()
        candidate = [x for x in candidate if self.history[self.k2k[x]]['result'] in  correctness]
        return candidate
    
    def get_cluster(self,index_id):
        index_list = []
        for i in self.get_cluster_index(index_id):
            index_list.append(self.history_questions[i])
        return index_list
 
    def get_question_by_cluster(self,index_id,correctness = [True,False]):
        process_list = []
        for i in self.get_cluster_index(index_id,correctness):
            process_list.append(self.history_questions[i])
        return process_list
    
    def get_process_by_cluster(self,index_id,correctness = [True,False]):
        process_list = []
        for i in self.get_cluster_index(index_id,correctness):
            process_list.append(self.get_history_text(self.k2k[i]))
        return process_list


    def process_entities(self,entities):
        entities_sorted_by_start = sorted(entities, key=lambda x: x[1])
        entities_sorted_by_end = sorted(entities, key=lambda x: x[1], reverse=True)
        if len(entities) >3:
            return 'entities = {}'.format(str(entities_sorted_by_start[:2] + ['...'] + entities_sorted_by_end[:1]))
        else:
            return 'entities = {}'.format(str(entities))
    
    def get_history_text(self,qid):
        history_text = []
        history_dict = self.history
        # Add question to history
        history_text.append(f"Question: {history_dict[qid]['question']['question']}")

        # Process history data
        process_data = history_dict[qid]['process']
        for i, (action, response) in enumerate(zip(process_data['history_candidate_actions'], process_data['history_response'])):
            # history_text.append(f"Candidate actions {i}: {action}")
            history_text.append(f"LLM Action {i}: {response}")

            retrieval_data = process_data.get('history_retrieval', [])
            retrieval_text = self.process_entities(retrieval_data[i]) if i < len(retrieval_data) else 'Wrong action, unable to get data.'
            history_text.append(f"Retrieval {i}: {retrieval_text}")

        # Add result to history
        if history_dict[qid]['result']:
            history_text.append('Correct!')
        else:
            try:
                answers = [self.id2text[x] for x in history_dict[qid]['question']['answers']]
            except:
                answers = history_dict[qid]['question']['answers']
            history_text.append(f"Wrong! The answer is {answers}")

        # Print final history text
        return '\n'.join(history_text)
    
    def get_cluster_indtsruction(self,c):
        correct = '\n\n'.join(self.get_process_by_cluster(c,correctness=[True])[:3])
        incorrect =  '\n\n'.join(self.get_process_by_cluster(c,correctness=[False])[:3])
        prompt = self.summary_prompt.replace('{correct_examples}',correct).replace('{incorrect_examples}',incorrect)
        return prompt
    
    def summmary(self):
        for c in tqdm(range(self.n_clusters)):
            prompt_instruction = self.get_cluster_indtsruction(c)
            self.methodology_dict[c] = gpt4(prompt_instruction)
            time.sleep(5)

    def get_clean_question(self,q,head_text,tail_text):
        date_pattern = date_pattern = re.compile( r'\b(?:\d{1,2}\s)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s?\d{1,2}?(?:\s|,)?\s?\d{2,4}\b|\b\d{4}\b')
        match = date_pattern.search(q)
        date_str = '2000'
        if match:
            date_str = match.group(0)
        clean_q = q.replace(head_text.replace('_',' '),'{entity}').replace(tail_text.replace('_',' '),'{entity}').replace(date_str,'{time}')
        return clean_q
    
    def human_in_loop(self,q):
        if 'before' in q and 'last' in q:
            return self.human_in_loop_instruction['before_last']
        elif 'after' in q and 'first' in q:
            return self.human_in_loop_instruction['after_first']
        else:
            return None

    def get_method_instruction(self,q,head_text,tail_text):
        # if self.human_in_loop(q) is not None:
        #     return self.human_in_loop(q)
        q = self.get_clean_question(q,head_text,tail_text)
        idx = self.predict_memory_cluster(q)
        return self.methodology_dict[idx]
    



class Inference():
    def __init__(self, kg, id2text, rel2text,history=[],n_clusters=10):
        self.kg = kg
        self.id2text = id2text
        self.rel2text = rel2text
        self.text2id = {value: key for key, value in self.id2text.items()}
        self.text2rel = {value: key for key, value in self.rel2text.items()}
        self.tick = 0
        self.history_candidate_actions = []
        self.history_actions = []
        self.history_retrieval = []
        self.history_response = []
        self.memory = History_Memory(n_clusters)
        self.history = []
        self.entities = []
        self.LLM_rel_choose = None
        if len(history)>0:
            self.memory.update_memory(history)

    def get_history(self):
        return {'history':self.history,
                'history_actions':self.history_actions,
                'history_response':self.history_response,
                'history_retrieval':self.history_retrieval,
                'history_candidate_actions':self.history_candidate_actions}
    

    def reset(self):
        self.tick = 0
        self.history = []
        self.entities = []
        self.history_actions = []
        self.history_candidate_actions = []
        self.history_retrieval = []
        self.history_response = []
        self.LLM_rel_choose = None



    def extract_content(self, text, record = True):
        pattern = r'\$(.*?)\$(?!\w)'
        matches = re.findall(pattern, text)
        extracted_info = []
        for match in matches:
            if len(match) < 10:
                continue
            function_name, params = self.extract_function_info(match)
            extracted_info.append((function_name, params))
        if record:
            self.tick +=1
            self.history_actions.append('$'+ matches[0]+ '$')
            self.history.append(['Action {}:'.format(self.tick),'$' + matches[0] + '$'])
        if len(extracted_info)>0:
            if extracted_info[0][1] is None:
                return extracted_info[1]
        return extracted_info[0]

    def extract_function_info(self, match):
        pattern = r'^(\w+)\((.*?)\)$'
        result = re.match(pattern, match)
        if result:
            function_name = result.group(1)
            params = result.group(2).split(',')
            return function_name, params
        else:
            return None, None
        
    def transform_text(self,text):
        prefix, entities = text.split('(', 1)
        entity, position, time_constraint = entities[:-1].split(',')
        transformed = f"${prefix}(None,{position},{entity},{time_constraint})$"

        return transformed
        
    def action_filter(self, actions):
        filtered_actions = []
        for action in actions:
            if action in self.history_actions:
                continue
            f,p = self.extract_content(action,record = False)
            if f not in ['get_tail_entity','get_time','get_head_entity']:
                filtered_actions.append(action)
            elif len(self.query_knowledge_graph(f,p))>0:
                filtered_actions.append(action)
        self.history_candidate_actions.append(filtered_actions)
        return filtered_actions

    def query_knowledge_graph(self, function_name, params):
        params = [x.strip() for x in params]
        function_name = function_name.lower()
        if function_name == 'get_tail_entity':
            head = params[0]
            rel = params[1]
            time = params[2]
            return self.get_tail_entity(head, rel, time)
        elif function_name == 'get_head_entity':
            tail = params[0]
            rel = params[1]
            time = params[2]
            return self.get_head_entity(tail, rel, time)
        elif function_name == 'get_time':
            head = params[0]
            rel = params[1]
            tail = params[2]
            return self.get_time(head, rel, tail)
        elif function_name == 'get_before':
            entities = params[0]
            entities = self.entities
            time = params[1].strip()
            return self.get_before(entities, time)
        elif function_name == 'get_after':
            entities = params[0]
            entities = self.entities
            time = params[1].strip()
            return self.get_after(entities, time)
        elif function_name == 'get_between':
            entities = params[0]
            entities = self.entities
            s = params[1].strip()
            e = params[2].strip()
            return self.get_between(entities, s,e)
        elif function_name == 'get_first':
            entities = params[0]
            entities = self.entities
            return self.get_first(entities)
        elif function_name == 'get_last':
            entities = self.entities
            return self.get_last(entities)
        elif function_name == 'answer':
            return params
        else:
            print('Unknown function name')
            return []

    def get_tail_entity(self, head, rel, time):
        if time == 'no time constraints':
            time = 0
        return self.get_data_compare(h = head,r=rel,time=time,n=True)

    def get_head_entity(self, tail, rel, time):
        if time == 'no time constraints':
            time = 0
        return self.get_data_compare(t = tail,r=rel,time=time,n=True)
    
    def get_time(self, head, rel, tail):
        return self.get_data_compare(h = head,r=rel,t=tail,n=True)

    @staticmethod
    def get_before(entities, target_time):
        before_entities = []
        for entity, time in entities:
            if time < target_time:
                before_entities.append((entity, time))
        return before_entities
    
    @staticmethod
    def get_between(entities, s,e):
        between_entities = []
        for entity, time in entities: 
            if time <= e and time >= s:
                between_entities.append((entity, time))
        return between_entities
    
    @staticmethod
    def get_after(entities, target_time):
        after_entities = []
        for entity, time in entities:
            if time > target_time:
                after_entities.append((entity, time))
        return after_entities

    @staticmethod
    def get_first(entities):
        if len(entities)>0:
            first_entity = min(entities, key=lambda x: x[1])
            return [first_entity]
        else:
            return []

    @staticmethod
    def get_last(entities):
        if len(entities)>0:
            last_entity = max(entities, key=lambda x: x[1])
            return [last_entity]
        else:
            return []

    def get_data_compare(self, h=0, r=0, t=0, e=0, e2=0, n=False, time=0):
        new = self.kg
        if r:
            new = new[new['rel'] == r]
        if h:
            new = new[new['head'] == h]
        if t:
            new = new[new['tail'] == t]
        if time:
            new = new[new['time'].apply(lambda x: x.startswith(str(time)))]
        if e:
            new = new[(new['head'] == e) | (new['tail'] == e)]
        if e2:
            new = new[(new['head'] == e) | (new['tail'] == e)]

        if n:
            return new.to_numpy()
        return new

    def process_entities(self,entities):
        entities_sorted_by_start = sorted(entities, key=lambda x: x[1])
        entities_sorted_by_end = sorted(entities, key=lambda x: x[1], reverse=True)
        if len(entities) >3:
            return 'entities = {}'.format(str(entities_sorted_by_start[:2] + ['...'] + entities_sorted_by_end[:1]))
        else:
            return 'entities = {}'.format(str(entities))
        
    def kg_to_text(self,kg_res):
        """
        Convert a list of quadruples into a textual representation.

        Args:
        - kg_res (list): A list of quadruples, where each quadruple consists of a head entity, relation, tail entity, and a date.

        Returns:
        - str: A textual representation of the quadruples.
        """
        if len(kg_res) == 0:
            return 'No results'
        if len(kg_res[0]) == 2:
            return kg_res[0][0] + ' in ' + kg_res[0][1]
        kg_res = sorted(kg_res, key=lambda x: x[3])
        if len(kg_res) >= 4:
            kg_res = kg_res[:2] + [kg_res[-1]]

        texts = []
        for i, quad in enumerate(kg_res):
            relation = quad[1].replace('_', ' ')
            text = f"{quad[0]} {relation} {quad[2]} in {quad[3]}"
            texts.append(text)
            if i == 1 and len(kg_res) > 2:
                texts.append("...")
        return '\n'.join(texts)

    def take_action(self,response):
        if len(self.history_candidate_actions)>0:
            for a in self.history_candidate_actions[-1]:
                if a[1:-1] in response:
                    response = a
        f, p = self.extract_content(response)
        self.history_response.append(response)
        kg_res = self.query_knowledge_graph(f, p)
        prompt_text = ''
        entities = []
        end = False

        if f == 'answer':
            #kg_text = kg_res[0] if len(kg_res)>0 else None
            entities = kg_res
            entities_text = 'entities = {}'.format(str(entities))
            end = True

        elif f not in ['get_tail_entity','get_head_entity', 'get_time']:
            prompt_text = 'The {} result is '.format(str(f))
            entities = kg_res
            #kg_text = kg_res[0] if len(kg_res)>0 else None
            entities_text = 'entities = {}'.format(str(entities[:5]))
        else:
            self.LLM_rel_choose = p[1].strip()
            prompt_text = 'The {} result is '.format(str(f))
            #kg_text = [str(x[0]) + ', ' + str(x[1]) + ', ' + str(x[2]) + ', from ' + str(x[3]) + ' to ' + str(x[4]) for x in kg_res]
            #kg_text = '\n'.join(kg_text[:5]) + '\n ...'
            if f == 'get_tail_entity':
                entities =  [(x[2], x[3]) for x in kg_res]
            elif f == 'get_head_entity':
                entities = [(x[0], x[3]) for x in kg_res]
            elif f == 'get_time':
                entities = [(x[0], x[3]) for x in kg_res]
            entities = list(set(entities))
            entities_text = self.process_entities(entities)

        self.entities = entities
        # print(type(prompt_text) , type(kg_text),type(entities_text))
        kg_text = self.kg_to_text(kg_res)
        self.history.append(['response {}:'.format(str(self.tick)), prompt_text +'\n'+kg_text + '\n' +entities_text])
        self.history_retrieval.append(entities)
        return kg_res,entities,end

    def check_correctness(self, answers, pred):
        transformed_anawsers = [x.replace(' ','_').replace(',', '-') for x in answers]
        if pred in self.text2id.keys():
            hit = pred in transformed_anawsers
        else:
            try:
                hit = str(pred) in answers
            except:
                hit = False
        return hit
    
    def get_history_text(self,history_dict,qid):
        history_text = []

        # Add question to history
        history_text.append(f"Question: {history_dict[qid]['question']['question']}")

        # Process history data
        process_data = history_dict[qid]['process']
        for i, (action, response) in enumerate(zip(process_data['history_candidate_actions'], process_data['history_response'])):
            history_text.append(f"Candidate actions {i}: {action}")
            history_text.append(f"LLM Action {i}: {response}")
            
            retrieval_data = process_data.get('history_retrieval', [])
            retrieval_text = retrieval_data[i][:5] if i < len(retrieval_data) else 'Wrong action, unable to get data.'
            prefix = '' if len(retrieval_data[i])<=5 else '...'
            history_text.append(f"Retrieval {i}: {retrieval_text}"+ prefix)
            history_text.append('\n')

        # Add result to history
        if history_dict[qid]['result']:
            history_text.append('Correct!')
        else:
            answers = history_dict[qid]['question']['answers']
            history_text.append(f"Wrong! The answer is {answers}")

        # Print final history text
        return '\n'.join(history_text)