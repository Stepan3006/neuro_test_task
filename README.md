# Модуль логики робота.

## Задача
Реализовать логику робота. Необходимо набросать основные переходы
и функции, которые вы планируете использовать для реализации скрипта используя Python.

## Библиотеки: nn, nlu, nv для написания логики
NeuroNetLibrary - python библиотека, содержит общие функции
Доступна внутри звонка и диалога в виде объекта nn (nn = NeuroNetLibrary(nlu_call, event_loop))

NeuroVoiceLibrary - python библиотека, для написания логики во время звонка на python
Доступна внутри звонка и диалога в виде объекта nlu (nlu = NeuroNluLibrary(nlu_call, event_loop) )
nlu.extract - метод для выдениея сущностей и интентов, возвращает объект NeuroNluRecognitionResult (описание в 
nv.listen)

NeuroVoiceLibrary - python библиотека, для написания логики во время звонка на python
Доступна внутри звонка в виде объекта nv nv = NeuroVoiceLibrary(nlu_call, loop)

Result – ссылка на объект NeuroNluRecognitionResult

result.utterance() Распознанный текст, очищенный от левых 
символов и сущностей preprocess_expressions

result.entity('entity_name') Возвращает значение сущности, если сущности не
существует вернет None

result.has_entity('entity_name') Наличие сущности (True, False)

result.has_entities() Наличие любых найденных сущностей (True,False)
 
result.intent('intent_name') Возвращает значение интента, если интента не 

result.has_intent('intent_name') Наличие интента (True, False)

result.has_intents() Наличие любых найденных интентов (True, False)


## Функции реализующие логику:
1. hello_logic
"""
    :param prompt_text: hello, hello_repeat, hello_null
    :return: nn.say prompt_text
"""
2. main_logic
"""
    :param prompt_name: recommend_main, recommend_repeat, recommend_repeat_2,
                        recommend_score_negative, recommend_score_positive,
                        recommend_score_neutral, recommend_null,
                        recommend_default
    :return: nv.say prompt name
 """
3. hangup_logic
"""
    :param hangup_type:  hangup_positive, hanghup_negative, 
                         hangup_wrong_time, hangup_null
    :return: hangup action
"""
4. forward_logic


