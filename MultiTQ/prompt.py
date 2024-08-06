
action_templates = [
    'get_tail_entity({head},{rel},{time})',
    'get_head_entity({tail},{rel},{time})',
    'get_time({head},{rel},{tail})',
    'get_before({entities},{your specified time})',
    'get_after({entities},{your specified time})',
    'get_first({entities})',
    'get_last({entities})',
    'get_between({entities},{your specified start time},{your specified end time})',
    
]

EXAMPLES_ALL ='''Examples 0:
Question: In which month did the City Mayor of Philippines first praise Ona?
Action 0:$get_time(City_Mayor_(Philippines),Praise_or_endorse,Ona)$
Response 0: entities = [('City_Mayor_(Philippines)', '2014-10-07')]
Action 1: $get_first({entities})$
Response 1: entities = [('City_Mayor_(Philippines)', '2014-10-07')]
Action 2: $answer(2014-10)$
Response 2: Correct!

Examples 1:
Question: Who wanted to cooperate with Japan in November, 2005?
Action 0: $get_head_entity(Japan,Express_intent_to_cooperate,2005-11)$
response 0: entities = [('Government_Official_(Russia)', '2005-11-01'), ('China', '2005-11-01'), '...', ('South_Korea', '2005-11-30')]
Action 1: $answer(South_Korea)$
response 1: Correct!

Examples 2:
Question: Who was the first to request a meeting with Togo in 2005?
Action 0: $get_head_entity(Togo,Express_intent_to_meet_or_negotiate,2005)$
response 1: entities = [('Head_of_Government_(Togo)', '2005-02-09'), ('African_Union', '2005-02-11'), '...', ('Ministry_(Nigeria)', '2005-04-29')]"],
Action 1: $get_first({entities})$
response 1: entities = [('Head_of_Government_(Togo)', '2005-02-09')]
Action 2: $answer(Head_of_Government_(Togo))$
response 2: Correct!

Examples 3:
Question: Who had a telephone conversation with France after 2009-01?
Action 0: $get_head_entity(France,Discuss_by_telephone,no time constraints)$
Response 0: entities = [('China', '2007-03-03'), ('China', '2007-03-04'), '...', ('Angela_Merkel', '2015-02-10')]
Action 1: $get_after({entities},2009-01)$
Response 1:entities = [('Barack_Obama', '2009-01-26'), ('Barack_Obama', '2009-05-04'), '...', ('Angela_Merkel', '2015-02-10')]
Action 2: $answer(Angela_Merkel)$
Response 2: Correct!

Examples 4:
Question: Which country first did Iran made optimistic comments on after Dmitry Anatolyevich Medvedev?
Action 0: $get_time(Iran,Make_optimistic_comment,Dmitry_Anatolyevich_Medvedev)$
Response 0: entities = [('Iran', '2008-05-07')]
Action 1: $get_tail_entity(Iran,Make_optimistic_comment,no time constraints)$
Response 1:entities =entities = [('Iraq', '2005-06-15'), ('Mahmoud_Ahmadinejad', '2005-06-25'), '...', ('Japan', '2015-09-21')]
Action 2: $get_after({entities},2008-05-07)$
Response 2: entities = [('Javier_Solana', '2008-06-07'), ('China', '2008-10-16'), '...', ('Japan', '2015-09-21')]
Action 3: $get_first({entities})$
Response 3: entities = [('Javier_Solana', '2008-06-07')]
Action 4: $answer(Javier_Solana)$
Response 4: Correct!

Examples 5:
Question: Before the Police of Kenya, who used conventional military force against Kikuyu?'
Action 0: $get_time(Police_(Kenya),Use_conventional_military_force,Kikuyu)$
Response 0:entities = [('Police_(Kenya)', '2005-02-18')]
Action 1:$get_head_entity(Kikuyu,Use_conventional_military_force,no time constraints)$
Response 1: entities = [('Maasai', '2005-01-26'), ('Maasai', '2005-01-31'), '...', ('Maasai', '2005-02-24')]
Action 2: $get_before({entities},2005-02-18)$
Response 2: entities = [('Maasai', '2005-01-31'), ('Maasai', '2005-02-17'), ('Maasai', '2005-01-26')]
Action 3: $answer(Maasai)$
Response 3: Correct!

Examples 6:
Question: Before 12 May 2006, with which country did Iran announce its intention to cooperate?
Action 0: $get_head_entity(Iran,Express_intent_to_cooperate,no time constraints)$
Response 0: entities = [('Ethiopia', '2005-02-16'), ('France', '2005-04-05'), '...', ('China', '2015-12-24')]
Action 1: $get_before({entities}, 2006-05-12)$
Response 1: entities = [('Ethiopia', '2005-02-16'), ('Kazakhstan', '2005-05-18'), ('Iraq', '2005-10-11'), ('China', '2006-02-04'), ('Malaysia', '2005-05-14')]
Action 2:  $answer(Ethiopia)$
Response 2: Correct!

Examples 7:
Question: Before Mali's militant, which country was the last to criticise France?
Action 0: $get_time(Militant_(Mali),Criticize_or_denounce,France)$
Response 0: entities = [('Militant_(Mali)', '2013-01-21')]
Action 1: $get_first({entities})$
Response 1: entities = [("Government_(Cote_d'Ivoire)", '2005-01-20'), ('International_Federation_of_Human_Rights', '2005-02-04'), '...', ('Royal_Administration_(Spain)', '2015-12-24')]
Action 2: $get_last({entities})$
Response 2: entities = [('Royal_Administration_(Spain)', '2015-12-24')]
Action 3: $answer(Royal_Administration_(Spain))$
Response 3: Correct!

Examples 8:
Question: Who was the last to give a criticism to Iran before Pervez Musharraf did?
Action 0: $get_time(Pervez_Musharraf,Criticize_or_denounce,Iran)$
Response 0: entities = [('Pervez_Musharraf', '2006-01-17')]
Action 1: $get_head_entity(Iran,Criticize_or_denounce,no time constraints)$
Response 1: entities = [('Shirin_Ebadi', '2005-01-05'), ('Human_Rights_Watch', '2005-01-17'), '...', ('Eshaq_Jahangiri', '2015-12-14')]
Action 2: $get_before({entities},2006-01-17)$
Response 2: entities = [('Shirin_Ebadi', '2005-01-05'), ('Human_Rights_Watch', '2005-01-17'), '...', ('Angela_Merkel', '2006-01-16')]
Action 3: $get_last({entities})$
Response 3: entities = [('Angela_Merkel', '2006-01-16')]
Action 4: $answer(Angela_Merkel)$
Response 4: Correct!

Examples 9:
Question: At what time did Xi Jinping first make optimistic remarks on Japan?
Action 0: $get_time(Xi_Jinping,Make_optimistic_comment,Japan)$
Response 0: entities = [('Xi_Jinping', '2008-04-18'), ('Xi_Jinping', '2014-11-10'), '...', ('Xi_Jinping', '2015-12-01')]
Action 1: $get_first({entities})$
Response 1:entities = [('Xi_Jinping', '2008-04-18')]
Action 2: $answer(2008-04-18)$
Response 2: Correct!
'''

DECISION_INSTRUCTION = '''
Please use the tool provided below to interact with the knowledge graph. You will find a list of actions categorized into time-based queries, entity queries, and specific time queries. There may be more than one answer to the question, but you only need to answer one correct answer that satisfies the question.

To solve this question, you need to first identify the entities and relationships in the question, selecting the appropriate actions to retrieve the required information, and finally, providing the correct answer. 

Time-based Queries:
Retrieve the time of a specific event based on the head/subject entity, relation and tail/object entity by using the $get_time(HEAD, RELATION, TAIL)$ function, .
Identify entities/events that occurred before a given time by using the $get_before(ENTITY_LIST, SPECIFIED_TIME)$ function.
Identify entities/events that occurred after a given time by using the $get_after(ENTITY_LIST, SPECIFIED_TIME)$ function.
Identify entities/events that occurred between two specific times by using the $get_between(ENTITY_LIST, START_TIME, END_TIME)$ function.

Entity Queries:
Identify the tail/object entity based on the head/subject entity and relation by using the $get_tail_entity(CURRENT_HEAD, RELATION, OPTIONAL_TIME_CONSTRAINT)$ function.
Identify the head/suject entity based on the tail/object entity and relation by using the $get_head_entity(CURRENT_TAIL, RELATION, OPTIONAL_TIME_CONSTRAINT)$ function.

Specific Time Queries:
Pinpoint entities with the earliest occurrence by using the $get_first(ENTITY_LIST)$ function.
Identify entities with the latest occurrence by using the $get_last(ENTITY_LIST)$ function.
To provide your answer, use the $answer(YOUR_ANSWER)$ function.

Note: Always enclose the selected action in $ and provide a reason for your choice if necessary.

Examples for your reference: {examples}
(end of examples)

Current Challenge:

Question: {question}

Methodology: {methodology}
(end of methodology)


Previous Actions: {history}
(end of previous actions)


Available Actions: {actions}

Choose your next action from the available actions above, ensuring its completeness. If you have found the answer, remember to use the answer function.

Organize your output by strictly following the format below:

Action:
<Choose your next action from the available actions above. Note: Always enclose the selected action in $. Replace {your specified time} with a specified time in the format YYYY or YYYY-MM or YYYY-MM-DD>

Reason:
<Explain the reason for choosing this action.>
'''

SUMMARY_INSTRUCTION =  '''Carefully analyze the following correct and incorrect examples. From these, extract and summarize the corresponding patterns and principles. Based on these examples, provide a comprehensive methodology that describes how to correctly tackle this type of problem, highlighting the key steps and common pitfalls to avoid.

Task Defination:
Please use the tool provided below to interact with the knowledge graph. You will find a list of actions categorized into time-based queries, entity queries, and specific time queries. There may be more than one answer to the question, but you only need to answer one correct answer that satisfies the question.
Time-based Queries:
Retrieve the time of a specific event based on the head/subject entity, relation and tail/object entity by using the $get_time(HEAD, RELATION, TAIL)$ function, .
Identify entities/events that occurred before a given time by using the $get_before(ENTITY_LIST, SPECIFIED_TIME)$ function.
Identify entities/events that occurred after a given time by using the $get_after(ENTITY_LIST, SPECIFIED_TIME)$ function.
Identify entities/events that occurred between two specific times by using the $get_between(ENTITY_LIST, START_TIME, END_TIME)$ function.
Entity Queries:
Identify the tail/object entity based on the head/subject entity and relation by using the $get_tail_entity(CURRENT_HEAD, RELATION, OPTIONAL_TIME_CONSTRAINT)$ function.
Identify the head/suject entity based on the tail/object entity and relation by using the $get_head_entity(CURRENT_TAIL, RELATION, OPTIONAL_TIME_CONSTRAINT)$ function.
Specific Time Queries:
Pinpoint entities with the earliest occurrence by using the $get_first(ENTITY_LIST)$ function.
Identify entities with the latest occurrence by using the $get_last(ENTITY_LIST)$ function.
To provide your answer, use the $answer(YOUR_ANSWER)$ function.
(end of Task Defination) 

Here is an example output:
Example 1:
Overall methodology Instruction: 
This type of problem involves the sequential determination of events, e.g. Who {Relation R} {entity C} before {entity B}, to find the answer {entity A} we need to reason in three steps, firstly to determine the specific temporal anchors, i.e., the occurrence time t of {entity B, Relation, and entity C}, and then to find out which head entities have generated a Relation R connection with {entity C}. Then, we find out which head entities and {entity C} have been associated with Relation R, and finally filter out the answers that satisfy the time requirement before t. The specific steps are as follows. The steps are as follows

Step-by-step Guide:
1. Firstly, use get_time to find the time, $get_time(entity B, Relation R, entity C)$, to get the quaternion {entity B, Relation R, entity C, Time t};
2. use the get_head_entity method to get the head entity, $get_head_entity(entity C, Relation R, entity C)$, to be able to get a list of quaternions;
3. use the get_before method to filter the entities that satisfy the constraints, $get_before({entities},t)$, to be able to obtain a list of entities that satisfy the conditions
4. complete the reasoning process by answering the found answer $answer(entity A)$

(end of example output)


Here is the correct samples and incorrect samples for the current question type:
Correct samples: 
{correct_examples}

Incorrect samples:
{incorrect_examples}
(end of samples)

Now start writing. Please design a methodology that describes how to correctly tackle this type of problem. The goal is to provide a comprehensive guide that highlights the key steps and common pitfalls to avoid when approaching this type of problem.organize your output by strictly following the output format as below:

Overall Instruction: 
<Define this methodology in detail.  Provide a concise guide or inference. Note that the guidance you provide should be at a methodological level, for this type of question, not for a specific one. >

Step-by-step Guide:
<A step-by-step guide or procedure detailing how to approach and solve this kind of question. Note that the steps proposed should be specific and relevant to this type of question, tell which type of action should use in each step and the reason>

'''

EXAMPLES_WITH_RATIONALS_ALL ='''
Examples 0:
Question: In which month did the City Mayor of Philippines first praise Ona?
Action 0: $get_time(City_Mayor_(Philippines),Praise_or_endorse,Ona)$
Reason: To determine when the City Mayor of the Philippines praised Ona, we start with the get_time function.
Response 0: entities = [('City_Mayor_(Philippines)', '2014-10-07')]
Action 1: $get_first({entities})$
Reason: To find out the first time the City Mayor of the Philippines praised Ona, we utilize the get_first function.
Response 1: entities = [('City_Mayor_(Philippines)', '2014-10-07')]
Action 2: $answer(2014-10)$
Reason: Extracting the month and year from the date provided, we determine that the first praise was in October 2014. We then use the answer function to provide this response.
Response 2: Correct!

Examples 1:
Question: Who wanted to cooperate with Japan in November, 2005?
Action 0: $get_head_entity(Japan,Express_intent_to_cooperate,2005-11)$
Reason: To identify entities that expressed an intent to cooperate with Japan in November 2005, we start by using the get_head_entity function.
Response 0: entities = [('Government_Official_(Russia)', '2005-11-01'), ('China', '2005-11-01'), '...', ('South_Korea', '2005-11-30')]
Action 1: $answer(South_Korea)$
Reason: Based on the returned list of entities, we select an appropriate response and use the answer function to provide it.
Response 1: Correct!

Examples 2:
Question: Who was the first to request a meeting with Togo in 2005?
Action 0: $get_head_entity(Togo,Express_intent_to_meet_or_negotiate,2005)$
Reason: We want to find entities that expressed an intent to meet or negotiate with Togo in 2005.
Response 0: entities = [('Head_of_Government_(Togo)', '2005-02-09'), ('African_Union', '2005-02-11'), '...', ('Ministry_(Nigeria)', '2005-04-29')]
Action 1: $get_first({entities})$
Reason: Out of the entities that wanted to meet Togo, we are specifically looking for the first one.
Response 1: entities = [('Head_of_Government_(Togo)', '2005-02-09')]
Action 2: $answer(Head_of_Government_(Togo))$
Reason: Based on the earliest entity retrieved, we provide the answer.
Response 2: Correct!

Examples 3:
Question: Who had a telephone conversation with France after 2009-01?
Action 0: $get_head_entity(France,Discuss_by_telephone,no time constraints)$
Reason: To identify the entities that had a telephone conversation with France, we start by using the get_head_entity function.
Response 0: entities = [('China', '2007-03-03'), ('China', '2007-03-04'), '...', ('Angela_Merkel', '2015-02-10')]
Action 1: $get_after({entities},2009-01)$
Reason: From the list of entities, we need those that had the conversation after January 2009.
Response 1: entities = [('Barack_Obama', '2009-01-26'), ('Barack_Obama', '2009-05-04'), '...', ('Angela_Merkel', '2015-02-10')]
Action 2: $answer(Angela_Merkel)$
Reason: From the provided list, we select an appropriate entity to answer the question.
Response 2: Correct!

Examples 4:
Question: Which country first did Iran make optimistic comments on after Dmitry Anatolyevich Medvedev?
Action 0: $get_time(Iran,Make_optimistic_comment,Dmitry_Anatolyevich_Medvedev)$
Reason: To understand when Iran made optimistic comments about Dmitry Anatolyevich Medvedev, we begin by using the get_time function.
Response 0: entities = [('Iran', '2008-05-07')]
Action 1: $get_tail_entity(Iran,Make_optimistic_comment,no time constraints)$
Reason: To find out which country Iran commented on, we use the get_tail_entity function without any time constraint.
Response 1: entities = [('Iraq', '2005-06-15'), ('Mahmoud_Ahmadinejad', '2005-06-25'), '...', ('Japan', '2015-09-21')]
Action 2: $get_after({entities},2008-05-07)$
Reason: From the provided entities, we now want to know which country Iran commented on after 2008-05-07, hence using the get_after function.
Response 2: entities = [('Javier_Solana', '2008-06-07'), ('China', '2008-10-16'), '...', ('Japan', '2015-09-21')]
Action 3: $get_first({entities})$
Reason: To answer the question, we need to determine the first country on the list after the specific date, so we use the get_first function.
Response 3: entities = [('Javier_Solana', '2008-06-07')]
Action 4: $answer(Javier_Solana)$
Reason: With Javier Solana being the first entity after the specified date, we use the answer function to provide it as the response.
Response 4: Correct!

Examples 5:
Question: Before the Police of Kenya, who used conventional military force against Kikuyu?
Action 0: $get_time(Police_(Kenya),Use_conventional_military_force,Kikuyu)$
Reason: To determine when the Police of Kenya used conventional military force against Kikuyu, we start with the get_time function.
Response 0: entities = [('Police_(Kenya)', '2005-02-18')]
Action 1: $get_head_entity(Kikuyu,Use_conventional_military_force,no time constraints)$
Reason: Next, to identify all entities that used conventional military force against Kikuyu, we use the get_head_entity function without any time constraints.
Response 1: entities = [('Maasai', '2005-01-26'), ('Maasai', '2005-01-31'), '...', ('Maasai', '2005-02-24')]
Action 2: $get_before({entities},2005-02-18)$
Reason: From the returned list of entities, we want to filter out those that took action before 2005-02-18, so we use the get_before function.
Response 2: entities = [('Maasai', '2005-01-31'), ('Maasai', '2005-02-17'), ('Maasai', '2005-01-26')]
Action 3: $answer(Maasai)$
Reason: Based on the filtered entities, Maasai is identified as the entity that took action against Kikuyu before the Police of Kenya. Thus, we use the answer function to provide the response.
Response 3: Correct!

Examples 6:
Question: Before 12 May 2006, with which country did Iran announce its intention to cooperate?
Action 0: $get_head_entity(Iran,Express_intent_to_cooperate,no time constraints)$
Reason: To identify all countries that Iran expressed an intention to cooperate with, regardless of the time frame, we start by using the get_head_entity function without time constraints.
Response 0: entities = [('Ethiopia', '2005-02-16'), ('France', '2005-04-05'), '...', ('China', '2015-12-24')]
Action 1: $get_before({entities}, 2006-05-12)$
Reason: From the list of countries Iran intended to cooperate with, we need to filter out those that expressed this intent before 12 May 2006. To achieve this, we use the get_before function.
Response 1: entities = [('Ethiopia', '2005-02-16'), ('Kazakhstan', '2005-05-18'), ('Iraq', '2005-10-11'), ('China', '2006-02-04'), ('Malaysia', '2005-05-14')]
Action 2: $answer(Ethiopia)$
Reason: Based on the filtered list of countries, Ethiopia is identified as the earliest country with which Iran intended to cooperate before the specified date. We then use the answer function to provide the response.
Response 2: Correct!

Examples 7:
Question: Before Mali's militant, which country was the last to criticise France?
Action 0: $get_time(Militant_(Mali),Criticize_or_denounce,France)$
Reason: To determine the time frame in which Mali's militants criticized France, we initiate with the get_time function.
Response 0: entities = [('Militant_(Mali)', '2013-01-21')]
Action 1: $get_first({entities})$
Reason: To retrieve a list of entities that criticized France prior to Mali's militants, we utilize the get_first function.
Response 1: entities = [("Government_(Cote_d'Ivoire)", '2005-01-20'), ('International_Federation_of_Human_Rights', '2005-02-04'), '...', ('Royal_Administration_(Spain)', '2015-12-24')]
Action 2: $get_last({entities})$
Reason: From the provided list, we aim to pinpoint the most recent entity (just before Mali's militants) that criticized France. The get_last function facilitates this.
Response 2: entities = [('Royal_Administration_(Spain)', '2015-12-24')]
Action 3: $answer(Royal_Administration_(Spain))$
Reason: Based on the retrieved list, the last entity to criticize France before Mali's militants was the 'Royal Administration (Spain)'. Hence, we use the answer function to provide this response.
Response 3: Correct!

Examples 8:
Question: Who was the last to give a criticism to Iran before Pervez Musharraf did?
Action 0: $get_time(Pervez_Musharraf,Criticize_or_denounce,Iran)$
Reason: First, we need to determine when Pervez Musharraf criticized Iran.
Response 0: entities = [('Pervez_Musharraf', '2006-01-17')]
Action 1: $get_head_entity(Iran,Criticize_or_denounce,no time constraints)$
Reason: We want to identify all entities that criticized Iran.
Response 1: entities = [('Shirin_Ebadi', '2005-01-05'), ('Human_Rights_Watch', '2005-01-17'), '...', ('Eshaq_Jahangiri', '2015-12-14')]
Action 2: $get_before({entities},2006-01-17)$
Reason: From the list of entities, we filter out those that criticized Iran before Musharraf's criticism.
Response 2: entities = [('Shirin_Ebadi', '2005-01-05'), ('Human_Rights_Watch', '2005-01-17'), '...', ('Angela_Merkel', '2006-01-16')]
Action 3: $get_last({entities})$
Reason: We're looking for the most recent criticism before Musharraf's, so we use the get_last command.
Response 3: entities = [('Angela_Merkel', '2006-01-16')]
Action 4: $answer(Angela_Merkel)$
Reason: With the last entity in hand, we provide the answer.
Response 4: Correct!

Example 9:
Question: At what time did Xi Jinping first make optimistic remarks on Japan?
Action 0: $get_time(Xi_Jinping,Make_optimistic_comment,Japan)$
Reason: The goal here is to retrieve all instances when Xi Jinping made optimistic comments about Japan. This action provides a list of dates when Xi Jinping made such comments.
Response 0: entities = [('Xi_Jinping', '2008-04-18'), ('Xi_Jinping', '2014-11-10'), '...', ('Xi_Jinping', '2015-12-01')]
Action 1: $get_first({entities})$
Reason: Given the list of dates, we want to identify the first occurrence when Xi Jinping made an optimistic comment about Japan.
Response 1: entities = [('Xi_Jinping', '2008-04-18')]
Action 2: $answer(2008-04-18)$
Reason: The date '2008-04-18' is the first instance when Xi Jinping made optimistic remarks about Japan. Thus, it's the answer to the question.
Response 2: Correct!
'''


EXAMPLES_WITH_RATIONALS ='''
Examples 0:
Question: In which month did the City Mayor of Philippines first praise Ona?
Action 0: $get_time(City_Mayor_(Philippines),Praise_or_endorse,Ona)$
Reason: To determine when the City Mayor of the Philippines praised Ona, we start with the get_time function.
Response 0: entities = [('City_Mayor_(Philippines)', '2014-10-07')]
Action 1: $get_first({entities})$
Reason: To find out the first time the City Mayor of the Philippines praised Ona, we utilize the get_first function.
Response 1: entities = [('City_Mayor_(Philippines)', '2014-10-07')]
Action 2: $answer(2014-10)$
Reason: Extracting the month and year from the date provided, we determine that the first praise was in October 2014. We then use the answer function to provide this response.
Response 2: Correct!

Examples 1:
Question: Who wanted to cooperate with Japan in November, 2005?
Action 0: $get_head_entity(Japan,Express_intent_to_cooperate,2005-11)$
Reason: To identify entities that expressed an intent to cooperate with Japan in November 2005, we start by using the get_head_entity function.
Response 0: entities = [('Government_Official_(Russia)', '2005-11-01'), ('China', '2005-11-01'), '...', ('South_Korea', '2005-11-30')]
Action 1: $answer(South_Korea)$
Reason: Based on the returned list of entities, we select an appropriate response and use the answer function to provide it.
Response 1: Correct!

Examples 2:
Question: Who was the first to request a meeting with Togo in 2005?
Action 0: $get_head_entity(Togo,Express_intent_to_meet_or_negotiate,2005)$
Reason: We want to find entities that expressed an intent to meet or negotiate with Togo in 2005.
Response 0: entities = [('Head_of_Government_(Togo)', '2005-02-09'), ('African_Union', '2005-02-11'), '...', ('Ministry_(Nigeria)', '2005-04-29')]
Action 1: $get_first({entities})$
Reason: Out of the entities that wanted to meet Togo, we are specifically looking for the first one.
Response 1: entities = [('Head_of_Government_(Togo)', '2005-02-09')]
Action 2: $answer(Head_of_Government_(Togo))$
Reason: Based on the earliest entity retrieved, we provide the answer.
Response 2: Correct!

Examples 3:
Question: Who had a telephone conversation with France after 2009-01?
Action 0: $get_head_entity(France,Discuss_by_telephone,no time constraints)$
Reason: To identify the entities that had a telephone conversation with France, we start by using the get_head_entity function.
Response 0: entities = [('China', '2007-03-03'), ('China', '2007-03-04'), '...', ('Angela_Merkel', '2015-02-10')]
Action 1: $get_after({entities},2009-01)$
Reason: From the list of entities, we need those that had the conversation after January 2009.
Response 1: entities = [('Barack_Obama', '2009-01-26'), ('Barack_Obama', '2009-05-04'), '...', ('Angela_Merkel', '2015-02-10')]
Action 2: $answer(Angela_Merkel)$
Reason: From the provided list, we select an appropriate entity to answer the question.
Response 2: Correct!

Examples 4:
Question: Before the Police of Kenya, who used conventional military force against Kikuyu?
Action 0: $get_time(Police_(Kenya),Use_conventional_military_force,Kikuyu)$
Reason: To determine when the Police of Kenya used conventional military force against Kikuyu, we start with the get_time function.
Response 0: entities = [('Police_(Kenya)', '2005-02-18')]
Action 1: $get_head_entity(Kikuyu,Use_conventional_military_force,no time constraints)$
Reason: Next, to identify all entities that used conventional military force against Kikuyu, we use the get_head_entity function without any time constraints.
Response 1: entities = [('Maasai', '2005-01-26'), ('Maasai', '2005-01-31'), '...', ('Maasai', '2005-02-24')]
Action 2: $get_before({entities},2005-02-18)$
Reason: From the returned list of entities, we want to filter out those that took action before 2005-02-18, so we use the get_before function.
Response 2: entities = [('Maasai', '2005-01-31'), ('Maasai', '2005-02-17'), ('Maasai', '2005-01-26')]
Action 3: $answer(Maasai)$
Reason: Based on the filtered entities, Maasai is identified as the entity that took action against Kikuyu before the Police of Kenya. Thus, we use the answer function to provide the response.
Response 3: Correct!

Examples 5:
Question: Which country first did Iran make optimistic comments on after Dmitry Anatolyevich Medvedev?
Action 0: $get_time(Iran,Make_optimistic_comment,Dmitry_Anatolyevich_Medvedev)$
Reason: To understand when Iran made optimistic comments about Dmitry Anatolyevich Medvedev, we begin by using the get_time function.
Response 0: entities = [('Iran', '2008-05-07')]
Action 1: $get_tail_entity(Iran,Make_optimistic_comment,no time constraints)$
Reason: To find out which country Iran commented on, we use the get_tail_entity function without any time constraint.
Response 1: entities = [('Iraq', '2005-06-15'), ('Mahmoud_Ahmadinejad', '2005-06-25'), '...', ('Japan', '2015-09-21')]
Action 2: $get_after({entities},2008-05-07)$
Reason: From the provided entities, we now want to know which country Iran commented on after 2008-05-07, hence using the get_after function.
Response 2: entities = [('Javier_Solana', '2008-06-07'), ('China', '2008-10-16'), '...', ('Japan', '2015-09-21')]
Action 3: $get_first({entities})$
Reason: To answer the question, we need to determine the first country on the list after the specific date, so we use the get_first function.
Response 3: entities = [('Javier_Solana', '2008-06-07')]
Action 4: $answer(Javier_Solana)$
Reason: With Javier Solana being the first entity after the specified date, we use the answer function to provide it as the response.
Response 4: Correct!

Examples 6:
Question: Before Mali's militant, which country was the last to criticise France?
Action 0: $get_time(Militant_(Mali),Criticize_or_denounce,France)$
Reason: To determine the time frame in which Mali's militants criticized France, we initiate with the get_time function.
Response 0: entities = [('Militant_(Mali)', '2013-01-21')]
Action 1: $get_first({entities})$
Reason: To retrieve a list of entities that criticized France prior to Mali's militants, we utilize the get_first function.
Response 1: entities = [("Government_(Cote_d'Ivoire)", '2005-01-20'), ('International_Federation_of_Human_Rights', '2005-02-04'), '...', ('Royal_Administration_(Spain)', '2015-12-24')]
Action 2: $get_last({entities})$
Reason: From the provided list, we aim to pinpoint the most recent entity (just before Mali's militants) that criticized France. The get_last function facilitates this.
Response 2: entities = [('Royal_Administration_(Spain)', '2015-12-24')]
Action 3: $answer(Royal_Administration_(Spain))$
Reason: Based on the retrieved list, the last entity to criticize France before Mali's militants was the 'Royal Administration (Spain)'. Hence, we use the answer function to provide this response.
Response 3: Correct!

'''


EXAMPLES ='''
Examples 0:
Question: In which month did the City Mayor of Philippines first praise Ona?
Action 0: $get_time(City_Mayor_(Philippines),Praise_or_endorse,Ona)$
Response 0: entities = [('City_Mayor_(Philippines)', '2014-10-07')]
Action 1: $get_first({entities})$
Response 1: entities = [('City_Mayor_(Philippines)', '2014-10-07')]
Action 2: $answer(2014-10)$
Response 2: Correct!

Examples 1:
Question: Who wanted to cooperate with Japan in November, 2005?
Action 0: $get_head_entity(Japan,Express_intent_to_cooperate,2005-11)$
Response 0: entities = [('Government_Official_(Russia)', '2005-11-01'), ('China', '2005-11-01'), '...', ('South_Korea', '2005-11-30')]
Action 1: $answer(South_Korea)$
Response 1: Correct!

Examples 2:
Question: Who was the first to request a meeting with Togo in 2005?
Action 0: $get_head_entity(Togo,Express_intent_to_meet_or_negotiate,2005)$
Response 0: entities = [('Head_of_Government_(Togo)', '2005-02-09'), ('African_Union', '2005-02-11'), '...', ('Ministry_(Nigeria)', '2005-04-29')]
Action 1: $get_first({entities})$
Response 1: entities = [('Head_of_Government_(Togo)', '2005-02-09')]
Action 2: $answer(Head_of_Government_(Togo))$
Response 2: Correct!

Examples 3:
Question: Who had a telephone conversation with France after 2009-01?
Action 0: $get_head_entity(France,Discuss_by_telephone,no time constraints)$
Response 0: entities = [('China', '2007-03-03'), ('China', '2007-03-04'), '...', ('Angela_Merkel', '2015-02-10')]
Action 1: $get_after({entities},2009-01)$
Response 1: entities = [('Barack_Obama', '2009-01-26'), ('Barack_Obama', '2009-05-04'), '...', ('Angela_Merkel', '2015-02-10')]
Action 2: $answer(Angela_Merkel)$
Response 2: Correct!

Examples 4:
Question: Before the Police of Kenya, who used conventional military force against Kikuyu?
Action 0: $get_time(Police_(Kenya),Use_conventional_military_force,Kikuyu)$
Response 0: entities = [('Police_(Kenya)', '2005-02-18')]
Action 1: $get_head_entity(Kikuyu,Use_conventional_military_force,no time constraints)$
Response 1: entities = [('Maasai', '2005-01-26'), ('Maasai', '2005-01-31'), '...', ('Maasai', '2005-02-24')]
Action 2: $get_before({entities},2005-02-18)$
Response 2: entities = [('Maasai', '2005-01-31'), ('Maasai', '2005-02-17'), ('Maasai', '2005-01-26')]
Action 3: $answer(Maasai)$
Response 3: Correct!

Examples 5:
Question: Which country first did Iran make optimistic comments on after Dmitry Anatolyevich Medvedev?
Action 0: $get_time(Iran,Make_optimistic_comment,Dmitry_Anatolyevich_Medvedev)$
Response 0: entities = [('Iran', '2008-05-07')]
Action 1: $get_tail_entity(Iran,Make_optimistic_comment,no time constraints)$
Response 1: entities = [('Iraq', '2005-06-15'), ('Mahmoud_Ahmadinejad', '2005-06-25'), '...', ('Japan', '2015-09-21')]
Action 2: $get_after({entities},2008-05-07)$
Response 2: entities = [('Javier_Solana', '2008-06-07'), ('China', '2008-10-16'), '...', ('Japan', '2015-09-21')]
Action 3: $get_first({entities})$
Response 3: entities = [('Javier_Solana', '2008-06-07')]
Action 4: $answer(Javier_Solana)$
Response 4: Correct!

Examples 6:
Question: Before Mali's militant, which country was the last to criticise France?
Action 0: $get_time(Militant_(Mali),Criticize_or_denounce,France)$
Response 0: entities = [('Militant_(Mali)', '2013-01-21')]
Action 1: $get_first({entities})$
Response 1: entities = [("Government_(Cote_d'Ivoire)", '2005-01-20'), ('International_Federation_of_Human_Rights', '2005-02-04'), '...', ('Royal_Administration_(Spain)', '2015-12-24')]
Action 2: $get_last({entities})$
Response 2: entities = [('Royal_Administration_(Spain)', '2015-12-24')]
Action 3: $answer(Royal_Administration_(Spain))$
Response 3: Correct!
'''


HUMAN_IN_LOOP_INSTRUCTIONS = {
    'before_last':    '''
    Overall methodology Instruction: 
This type of question requires multi-step reasoning, e.g. Who was last {Relation R} {entity C} before {entity B}, to find the answer {entity A} we need to divide into four steps of reasoning, firstly, we need to determine the specific temporal anchors, i.e., the time t at which the {entity B, Relation, and Entity C} at time t, and then find out which head entities and {entity C} have generated Relation R, filter out the entities that satisfy the time requirement of before t, and finally select the answer with the last time among them. The steps are as follows
Step-by-step Guide:
1. first use get_time to find the time, $get_time(entity B, Relation R, entity C)$, to get the quaternion {entity B, Relation R, entity C, Time t}. 
2. use get_head_entity to find out which head entities have a Relation R with {entity C},$get_head_entity(entity C, Relation R, entity C)$, to be able to get a list of quaternions;
3. use the get_before method to filter entities that satisfy the after constraint, $get_before({entities},t)$, to get a list of entities that satisfy the condition
4. use the get_last method to get the entities that satisfy the first constraint, $get_last({entities},t)$, to get the list of entities that satisfy the condition
5. complete the reasoning process by answering the answers found $answer(entity A)$''',
    'after_first':'''
    Overall methodology Instruction: 
This type of question requires multi-step reasoning, e.g. Who was first {Relation R} {entity C} after {entity B}, to find the answer {entity A} we need to divide into four steps of reasoning, firstly, we need to determine the specific temporal anchors, i.e., the time t at which the {entity B, Relation, and Entity C} at time t, and then find out which head entities and {entity C} have generated Relation R, filter out the entities that satisfy the time requirement of after t, and finally select the answer with the earliest time among them. The steps are as follows
Step-by-step Guide:
1. first use get_time to find the time, $get_time(entity B, Relation R, entity C)$, to get the quaternion {entity B, Relation R, entity C, Time t}. 
2. use get_head_entity to find out which head entities have a Relation R with {entity C},$get_head_entity(entity C, Relation R, entity C)$, to be able to get a list of quaternions;
3. use the get_after method to filter entities that satisfy the after constraint, $get_after({entities},t)$, to get a list of entities that satisfy the condition
4. use the get_first method to get the entities that satisfy the first constraint, $get_first({entities},t)$, to get the list of entities that satisfy the condition.
5. complete the reasoning process by answering the answers found $answer(entity A)$''',
}
