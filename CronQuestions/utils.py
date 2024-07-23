import pandas as pd
import numpy as np
import pickle
import os
import openai
from openai import OpenAI
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from sentence_transformers import  util
import torch
import numpy as np
from tqdm import tqdm
import requests
import json
from collections import defaultdict


client = OpenAI(api_key='sk-xxxx',base_url="https://xxxx")

def gpt4(prompt):
    response= client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert at analysing to get a methodology from a case and you give a detailed methodology to solve that type of problem based on the case provided."},
            {"role": "user", "content": prompt}
        ],
            temperature=0.0
    )
    return response.choices[0].message.content


def chatgpt(prompt):
    response= client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a decision-maker guiding an agent through a temporal knowledge graph. The goal is to help the agent navigate and query until it uncovers the correct answer. The agent will suggest various methods and queries, and based on the question's semantics and previous steps, you'll choose the best option. Let's do step by step."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0
    )
    return response.choices[0].message.content





def get_history_text(inference,history_dict,qid):
    history_text = []

    # Add question to history
    history_text.append(f"Question: {history_dict[qid]['question']['paraphrases'][0]}")

    # Process history data
    process_data = history_dict[qid]['process']
    for i, (action, response) in enumerate(zip(process_data['history_candidate_actions'], process_data['history_response'])):
        history_text.append(f"Candidate actions {i}: {action}")
        history_text.append(f"LLM Action {i}: {response}")
        
        retrieval_data = process_data.get('history_retrieval', [])
        retrieval_text = retrieval_data[i] if i < len(retrieval_data) else 'Wrong action, unable to get data.'
        history_text.append(f"Retrieval {i}: {retrieval_text}")

    # Add result to history
    if history_dict[qid]['result']:
        history_text.append('Correct!')
    else:
        try:
            answers = [inference.id2text[x] for x in history_dict[qid]['question']['answers']]
        except:
            answers = history_dict[qid]['question']['answers']
        history_text.append(f"Wrong! The answer is {answers}")

    # Print final history text
    return '\n'.join(history_text)


class CronQuestions():
    def __init__(self, path='../data/cronquestions'):
        # question,kg,id2text,rel2text = get_cronquestions(path)
        # load preprocessed data
        with open('../data/cronquestions/data.pkl', 'rb') as f:
            question, kg, id2text, rel2text = pickle.load(f)
        for key, value in id2text.items():
            id2text[key] = str(value).replace(',', '-')
        self.question = question
        self.kg = kg
        # self.inference = KG_inference(kg)
        self.id2text = id2text
        self.rel2text = rel2text

    def get_cronquestions(self, path='../data/cronquestions'):
        question = np.load(path + '/questions/test.pickle', allow_pickle=True)
        kg = pd.read_csv(path + '/kg/full.txt', sep='\t', header=None)
        kg.columns = ['head', 'rel', 'tail', 'start', 'end']
        id2text = {}
        id2text_df = pd.read_csv(path + '/kg/wd_id2entity_text.txt', sep='\t', header=None)
        for i in id2text_df.index:
            id2text[id2text_df.loc[i][0]] = id2text_df.loc[i][1]
        rel2text = {}
        rel2text_df = pd.read_csv(path + '/kg/wd_id2relation_text.txt', sep='\t', header=None)
        for i in rel2text_df.index:
            rel2text[rel2text_df.loc[i][0]] = rel2text_df.loc[i][1]
        return question, kg, id2text, rel2text

    def __getitem__(self, qid):
        q = self.question[qid]['paraphrases'][0]
        tq = self.question[qid]['template']
        try:
            head = self.question[qid]['annotation']['head']
            head_text = self.id2text[head]
        except:
            head = 'None'
            head_text = 'None'
        try:
            tail = self.question[qid]['annotation']['tail']
            tail_text = self.id2text[tail]

        except:
            tail = 'None'
            tail_text = 'None'
        try:
            time = str(list(self.question[qid]['times'])[0])
        except:
            time = 'no time constraints'
        try:
            event = self.question[qid]['annotation']['event_head']
            event_text = self.id2text[event]
        except:
            event = 'None'
            event_text = 'None'
        rel_list = []
        for h in [head, tail, event]:
            rel_list += list(self.kg[self.kg['head'] == h].rel.unique())
            rel_list += list(self.kg[self.kg['tail'] == h].rel.unique())
        rel_list = list(set(rel_list))
        rel_text = [self.rel2text[x] for x in rel_list]
        return q, head_text, rel_text, tail_text, time, event_text, self.question[qid]['answers'],tq



class MultiTQ():
    def __init__(self, path='./data/MultiTQ'):
        question, kg, text2id, id2text, rel2text = self.get_multitq(path)
        self.question = question
        self.kg = kg
        self.id2text = id2text
        self.rel2text = rel2text
        self.model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

    def get_multitq(self, path='./data/MultiTQ'):
        path = './data/MultiTQ'
        with open(path + '/questions/processed_dev.json',encoding='utf-8') as f:
            question = json.load(f)
        kg = pd.read_csv(path + '/kg/full.txt', sep='\t', header=None)
        kg.columns = ['head', 'rel', 'tail', 'time']
        with open(path + '/kg/entity2id.json') as f:
            text2id = json.load(f)
            
        id2text = {v: k.replace(',', '-') for k, v in text2id.items()}
        
        with open(path + '/kg/relation2id.json') as f:
            text2rel = json.load(f)
        rel2text = {v: k for k, v in text2rel.items()}
        return question, kg, text2id, id2text, rel2text
    
    def relation_filter(self,q,rels):
        candidate_rels = ['Express_intent_to_meet_or_negotiate',
                         'Make_pessimistic_comment',
                         'Use_conventional_military_force',
                         'Provide_humanitarian_aid',
                         'Return,_release_person(s)',
                         'Make_a_visit',
                         'Sign_formal_agreement',
                         'Make_an_appeal_or_request',
                         'Express_intent_to_engage_in_diplomatic_cooperation_(such_as_policy_support)',
                         'Express_intent_to_cooperate',
                         'Praise_or_endorse',
                         'Reject',
                         'Criticize_or_denounce',
                         'Threaten',
                         'Engage_in_negotiation',
                         'Make_optimistic_comment',
                         'fight_with_small_arms_and_light_weapons',
                         'Investigate',
                         'Use_unconventional_violence',
                         'Host_a_visit',
                         'Discuss_by_telephone',
                         'Accuse']
        rels = [x for x in rels if x in candidate_rels]
        query_embedding = self.model.encode(q)
        passage_embedding = self.model.encode(rels)
        scores = util.dot_score(query_embedding, passage_embedding)
        indices = np.argsort(np.array(scores[0]))[::-1]
        top_indices = indices[:5]
        filtered_rels  = []
        for i in top_indices:
            filtered_rels.append(rels[i])
        return filtered_rels
    
    def __getitem__(self, qid):
        q = self.question[qid]['question']
        try:
            head_text = self.question[qid]['entities'][0].replace(' ','_').replace(',', '-')
        except:
            head_text = 'None'
        try:
            tail_text = self.question[qid]['entities'][1].replace(' ','_').replace(',', '-')
        except:
            tail_text = 'None'
        try:
            time = str(self.question[qid]['time'][0])
        except:
            time = 'no time constraints'

        event = 'None'
        event_text = 'None'
        
        rel_list = []
        for h in [head_text, tail_text]:
            rel_list += list(self.kg[self.kg['head'] == h].rel.unique())
            rel_list += list(self.kg[self.kg['tail'] == h].rel.unique())
        rel_text = list(set(rel_list))
        rel_text = self.relation_filter(q,rel_text )
        return q, head_text, rel_text, tail_text, time, event_text, self.question[qid]['answers']
    


def calculate_accuracy(history_dict):
    total_count = defaultdict(int)
    correct_count = defaultdict(int)

    # Iterate over history_dict to count total questions by type
    for _, v in history_dict.items():
        total_count[v['question']['type']] += 1

    # Iterate over history_dict to count correct answers by type
    for _, v in history_dict.items():
        if v['result']:
            correct_count[v['question']['type']] += 1

    total_questions = sum(total_count.values())
    total_correct = sum(correct_count.values())

    # Print the accuracy for each question type
    for question_type, total in total_count.items():
        accuracy = round(correct_count[question_type] / total, 2)
        print(question_type, '\t', accuracy, total)

    # Print overall accuracy
    overall_accuracy = total_correct / total_questions
    print("Overall Accuracy:", overall_accuracy)
    
    return overall_accuracy