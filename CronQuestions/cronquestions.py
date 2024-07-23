import pandas as pd
import numpy as np
import pickle
import os
import openai
from prompt import action_templates,SUMMARY_INSTRUCTION
import json
import pandas as pd
from sklearn.cluster import KMeans
from utils import CronQuestions
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


class History_Memory():
    def __init__(self,n_clusters=10,history = {}):
        # Build the semantic search model
        self.n_clusters = n_clusters
        self.embedder = SentenceTransformer('multi-qa-mpnet-base-cos-v1')
        self.kmeans = KMeans(n_clusters=self.n_clusters,n_init = 10)
        self.id2text = CronQuestions().id2text
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
            self.history_questions.append(self.history[i]['question']['template'])
        self.fit_history_memory()
        self.summmary()
        
    def fit_history_memory(self):
        t1 = self.embedder.encode(self.history_questions, convert_to_tensor=True).cpu()
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
        entities_sorted_by_end = sorted(entities, key=lambda x: x[2], reverse=True)
        if len(entities) >3:
            return 'entities = {}'.format(str(entities_sorted_by_start[:2] + ['...'] + entities_sorted_by_end[:1]))
        else:
            return 'entities = {}'.format(str(entities))
        
    def get_history_text(self,qid):
        history_text = []
        history_dict = self.history
        # Add question to history
        history_text.append(f"Question: {history_dict[qid]['question']['paraphrases'][0]}")

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
        correct = '\n\n'.join(self.get_process_by_cluster(c,correctness=[True])[:2])
        incorrect =  '\n\n'.join(self.get_process_by_cluster(c,correctness=[False])[:2])
        prompt = self.summary_prompt.replace('{correct_examples}',correct).replace('{incorrect_examples}',incorrect)
        return prompt
    
    def summmary(self):
        for c in tqdm(range(self.n_clusters)):
            prompt_instruction = self.get_cluster_indtsruction(c)
            self.methodology_dict[c] = gpt4(prompt_instruction)
            time.sleep(5)
            # prompt_instruction = self.get_cluster_indtsruction(c)
            # self.methodology_dict[c] = chatgpt(prompt_instruction)
    
    def get_method_instruction(self,q):
        idx = self.predict_memory_cluster(q)
        return self.methodology_dict[idx]
    


def get_actions(head_text, rel_texts, tail_text, time, event_text, entities=None):
    choose = []
    # Iterate over all relations
    for rel_text in rel_texts:
        go_for_entity = action_templates[0].replace('{head}', head_text).replace('{rel}', rel_text)
        choose.append(go_for_entity.replace('{time}', time))
        choose.append(go_for_entity.replace('{time}', 'no time constraints'))
        go_for_time = action_templates[2].replace('{head}', head_text).replace('{rel}', rel_text).replace('{tail}',
                                                                                                          tail_text)
        if 'None' not in go_for_time:
            choose.append(go_for_time)

        go_for_entity_tail = action_templates[0].replace('{head}', tail_text).replace('{rel}', rel_text)
        choose.append(go_for_entity_tail.replace('{time}', time))
        choose.append(go_for_entity_tail.replace('{time}', 'no time constraints'))
        go_for_time = action_templates[2].replace('{head}', tail_text).replace('{rel}', rel_text).replace('{tail}',
                                                                                                          head_text)
        if 'None' not in go_for_time:
            choose.append(go_for_time)

        go_for_entity_piror = action_templates[1].replace('{tail}', tail_text).replace('{rel}', rel_text)
        choose.append(go_for_entity_piror.replace('{time}', time))
        choose.append(go_for_entity_piror.replace('{time}', 'no time constraints'))

    if entities:
        for i in range(3, 7):
            choose.append(action_templates[i])#.replace('{time}', time))
        # for time join entities
        choose.append(action_templates[7].replace('{start}', str(entities[0][1])).replace('{end}', str(entities[0][2])))
        for e in entities[:2]:
            if type(e) == str or type(e) == int:
                choose.append('answer({})'.format(e))
            else:
                choose.append('answer({})'.format(e[0]))
                choose.append('answer({})'.format(e[1]))
                choose.append('answer({})'.format(e[2]))

    if event_text!='None' and entities==None:
        choose = []
        # go_for_entity = action_templates[0].replace('{head}',event_text).replace('{rel}','significant event')
        # choose.append(go_for_entity.replace('{time}',time))
        # choose.append(go_for_entity.replace('{time}','no time constraints'))
        go_for_time = action_templates[2].replace('{head}',event_text).replace('{rel}','significant event').replace('{tail}','occurrence')
        if 'None' not in go_for_time:
            choose.append(go_for_time)

    choose = list(set(choose))
    choose = [x for x in choose if '(None' not in x]
    choose = ['$' + x + '$' for x in choose]
    return choose




class Inference():
    def __init__(self, kg, id2text, rel2text,history,n_clusters = 10):
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
        self.history = []
        self.entities = []
        self.memory = History_Memory(n_clusters)
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
            self.history.append(['Action {}:'.format(self.tick),matches[0]])
        if len(extracted_info)>0:
            if extracted_info[0][1] is None:
                return extracted_info[1]
            if len(extracted_info[0][1]) == 0:
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
            if f not in ['get_tail_entity','get_time']:
                filtered_actions.append(action)
            elif len(self.query_knowledge_graph(f,p))>0:
                filtered_actions.append(action)
        self.history_candidate_actions.append(filtered_actions)
        return filtered_actions

    def query_knowledge_graph(self, function_name, params):
        params = [x.strip() for x in params]
        function_name = function_name.lower()
        if function_name == 'get_tail_entity':
            head = self.text2id[params[0]]
            rel = self.text2rel[params[1]]
            time = params[2]
            return self.get_tail_entity(head, rel, time)
        elif function_name == 'get_head_entity':
            tail = self.text2id[params[0]]
            rel = self.text2rel[params[1]]
            time = params[2]
            return self.get_head_entity(tail, rel, time)
        elif function_name == 'get_time':
            head = self.text2id[params[0]]
            rel = self.text2rel[params[1]]
            tail = self.text2id[params[2]]
            return self.get_time(head, rel, tail)
        elif function_name == 'get_before':
            entities = params[0]
            entities = self.entities
            time = params[1]
            return self.get_before(entities, time)
        elif function_name == 'get_after':
            entities = params[0]
            entities = self.entities
            time = params[1]
            return self.get_after(entities, time)
        elif function_name == 'get_between':
            entities = params[0]
            entities = self.entities
            s = params[1]
            e = params[2]
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
    def get_before(entities, time):
        before_entities = []
        for entity, start_time, end_time in entities:
            if int(end_time) < int(time):
                before_entities.append((entity, start_time, end_time))
        return before_entities
    
    @staticmethod
    def get_between(entities, s,e):
        between_entities = []
        for entity, start_time, end_time in entities:
            if int(end_time) <= int(e) and int(start_time) >= int(s):
                between_entities.append((entity, start_time, end_time))
        return between_entities
    
    @staticmethod
    def get_after(entities, time):
        after_entities = []
        for entity, start_time, end_time in entities:
            if int(start_time) > int(time):
                after_entities.append((entity, start_time, end_time))
        return after_entities

    @staticmethod
    def get_first(entities):
        if entities:
            first_entity = min(entities, key=lambda x: x[1])
            return [first_entity]
        else:
            return []

    @staticmethod
    def get_last(entities):
        if entities:
            last_entity = max(entities, key=lambda x: x[2])
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
            new = new[(new['start'] <= int(time)) & (new['end'] >= int(time))]
            # true_time = time[1:]
            # if time[0] == '>':
            #     new = new[new['time'] > true_time]
            # elif time[0] == '<':
            #     new = new[new['time'] < true_time]
            # else:
            #     new = new[new['time'].apply(lambda x: x.startswith(true_time))]

        if e:
            new = new[(new['head'] == e) | (new['tail'] == e)]
        if e2:
            new = new[(new['head'] == e) | (new['tail'] == e)]

        new['head'] = new['head'].apply(lambda x: self.id2text[x])
        new['tail'] = new['tail'].apply(lambda x: self.id2text[x])
        new['rel'] = new['rel'].apply(lambda x: self.rel2text[x])

        if n:
            return new.to_numpy()
        return new

    def process_entities(self,entities):
        entities_sorted_by_start = sorted(entities, key=lambda x: x[1])
        entities_sorted_by_end = sorted(entities, key=lambda x: x[2], reverse=True)
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
        if len(kg_res[0]) == 3:
            return kg_res[0][0] + ' from ' + str(kg_res[0][1]) + ' to ' + str(kg_res[0][1])
        if len(kg_res) == 1 and (type(kg_res[0])==str or type(kg_res[0])==int):
            return kg_res[0]
        kg_res = sorted(kg_res, key=lambda x: x[3])
        if len(kg_res) >= 4:
            kg_res = kg_res[:2] + [kg_res[-1]]

        texts = []
        for i, quad in enumerate(kg_res):
            relation = quad[1].replace('_', ' ')
            text = f"{quad[0]} {relation} {quad[2]} from {quad[3]} to {quad[4]}"
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
            prompt_text = 'The {} result is '.format(str(f))
            #kg_text = [str(x[0]) + ', ' + str(x[1]) + ', ' + str(x[2]) + ', from ' + str(x[3]) + ' to ' + str(x[4]) for x in kg_res]
            #kg_text = '\n'.join(kg_text[:5]) + '\n ...'
            if f == 'get_tail_entity':
                entities =  [(x[2], x[3], x[4]) for x in kg_res]
            elif f == 'get_head_entity':
                entities = [(x[0], x[3], x[4]) for x in kg_res]
            elif f == 'get_time':
                entities = [(x[0], x[3],x[4]) for x in kg_res]
            entities = list(set(entities))
            entities_text = self.process_entities(entities)
        self.entities = entities
        kg_text = self.kg_to_text(kg_res)
        # print(type(prompt_text) , type(kg_text),type(entities_text))
        self.history.append(['response {}:'.format(str(self.tick)), prompt_text +'\n'+kg_text + '\n' +entities_text])
        self.history_retrieval.append(entities)
        return kg_res,entities,end

    def check_correctness(self, answers, pred):
        if pred in self.text2id.keys():
            hit = self.text2id[pred] in answers
        else:
            try:
                hit = int(pred) in answers
            except:
                hit = False
        return hit