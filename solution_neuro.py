import libneuro
import datetime
import pytz
from datetime import timedelta

nn = libneuro.NeuroNetLibrary()
nlu = libneuro.NeuroNluLibrary()
nv = libneuro.NeuroVoiceLibrary()
check_call_state = libneuro.check_call_state
InvalidCallStateError = libneuro.InvalidCallStateError

hello_logic_enitity_list = [
    "confirm",
    "wrong_time",
    "repeat",
]

main_logic_enitity_list = [
    "recommendation_score",
    "recommendation",
    "repeat",
    "wrong_time",
    "question"
]

mem = {
    "hello": "<Name>, добрый день! Вас беспокоит компания X,"
                    "мы проводим опрос удовлетворенности нашими услугами."
                    "Подскажите, вам удобно сейчас говорить?",
    "hello_repeat": "Это компания X  Подскажите,"
                           "вам удобно сейчас говорить?",
    "hello_null": "Извините, вас не слышно. Вы могли бы повторить",
    "recommend_main": "Скажите, а готовы ли вы рекомендовать нашу"
                             "компанию своим друзьям? Оцените, пожалуйста,"
                             "по шкале от «0» до «10», где «0» - "
                             "не буду рекомендовать,«10» - обязательно"
                             "порекомендую.",
    "recommend_repeat": "Как бы вы оценили возможность"
                               "порекомендовать нашу компанию своим знакомым"
                               "по шкале от 0 до 10, где 0 - точно не "
                               "порекомендую, 10 - обязательно порекомендую.",
    "recommend_repeat_2": "Ну если бы вас попросили порекомендовать"
                                 "нашу компанию друзьям или знакомым, вы бы "
                                 "стали это делать? Если «да» - то оценка "
                                 "«10», если точно нет – «0».",
    "recommend_score_negative": "Ну а от 0 до 10 как бы вы оценили бы:"
                                       "0, 5 или может 7 ?",
    "recommend_score_neutral": "Ну а от 0 до 10 как бы вы оценили ?",
    "recommend_score_positive": "Хорошо,  а по 10-ти бальной шкале "
                                       "как бы вы оценили 8-9 или может 10 ?",
    "recommend_null": "Извините вас свосем не слышно,  повторите "
                             "пожалуйста ? ?",
    "recommend_default": "повторите пожалуйста ",
    "hangup_positive": "Отлично!  Большое спасибо за уделенное время!"
                              "Всего вам доброго!",
    "hangup_negative": "Я вас понял. В любом случае большое спасибо за "
                              "уделенное время!  Всего вам доброго. ",
    "hangup_wrong_time": "Извините пожалуйста за беспокойство. Всего"
                                " вам доброго",
    "hangup_null": "Вас все равно не слышно, будет лучше если я "
                          "перезвоню. Всего вам доброго"
}


def main():
    nn.call(
        nn.dialog['msisdn'],
        entry_point='main_online_container',
        on_success_call='after_call_success',
        on_failed_call='after_call_failed'
    )


def main_online_container():
    try:
        hello_main()
    except InvalidCallStateError:
        nn.log("Call ended")
        nn.log("Exception", str(e))
    except Exception as e:
        nn.log("Exception", str(e))
    else:
        nn.log("Call success")
    finally:
        call_start_time = nn.env('call_start_time')
        Msk = pytz.timezone('Europe/Moscow')
        input_format = '%Y-%m-%dT%H:%M:%S.%f'
        datetime_call_start_time = datetime.datetime.strptime(
            call_start_time,
            input_format
        )
        nn.env(
          'call_start', 
          datetime_call_start_time.astimezone(Msk).strftime("%d-%m-%Y %H:%M:%S")
        )
        nn.log(
            'Local time', 
            datetime_call_start_time.astimezone(Msk).strftime("%d-%m-%Y %H:%M:%S")
        )
        call_uuid = nn.env('call_uuid')
        nn.env('call_record',
               f"https://cms-v3.neuro.net/player?url=/api/v2/log/call/stream/{call_uuid}")
        nn.log('call_uuid', call_uuid)
        nn.log('call_record',
               f"https://cms-v3.neuro.net/player?url=/api/v2/log/call/stream/{call_uuid}")
        nn.log('attempt', nn.env('attempt'))
        nn.log('status', nn.env('status'))
        nn.log('result', nn.env('result'))


@check_call_state()
def hello():
    nn.log('unit', 'hello')
    nv.say('recommend_main')
    return hello_main()


@check_call_state()
def hello_repeat():
    nn.log('unit', 'hello_repeat')
    nv.say(mem['hello_repeat'])
    return hello_main()


@check_call_state()
def hello_null():
    hello_null_counter = nn.counter('hello_null', '+')
    if hello_null_counter >= 1:
        return hangup_null()
    nn.log('unit', 'hello_null')
    nv.say(mem['hello_null'])
    return hello_main()


@check_call_state()
def recommend_main():
    nn.log('unit', 'recommend_main')
    nv.say('recommend_main')
    return play_main()


@check_call_state()
def recommend_repeat():
    nn.log('unit', 'recommend_repeat')
    nv.say(mem['recommend_repeat'])
    return play_main()


@check_call_state()
def recommend_repeat_2():
    nn.log('unit', 'recommend_repeat_2')
    nv.say(mem['recommend_repeat_2'])
    return play_main()


@check_call_state()
def recommend_score_negative():
    nn.log('unit', 'recommend_score_negative')
    nv.say(mem['recommend_score_negative'])
    return play_main()


@check_call_state()
def recommend_score_neutral():
    nn.log('unit', 'recommend_score_neutral')
    nv.say(mem['recommend_score_neutral'])
    return play_main()


@check_call_state()
def recommend_score_positive():
    nn.log('unit', 'recommend_score_positive')
    nv.say(mem['recommend_score_positive'])
    return play_main()


@check_call_state()
def recommend_null():
    recommend_null_counter = nn.counter('recommend_null', '+')
    if recommend_null_counter >= 1:
        return hangup_null()
    nn.log('unit', 'hello_null')
    nv.say(mem['hello_null'])
    return hello_main()


@check_call_state()
def recommend_default():
    recommend_default_counter = nn.counter('recommend_default', '+')
    if recommend_default_counter >= 1:
        return hangup_null()
    nv.say(mem['recommend_default'])
    return play_main()


@check_call_state()
def hangup_positive():
    nn.log('unit', 'hangup_positive')
    nv.say(mem['hangup_positive'])
    nv.hangup()
    return


@check_call_state()
def hangup_negative():
    nn.log('unit', 'hangup_negative')
    nv.say(mem['hangup_negative'])
    nv.hangup()
    return


@check_call_state()
def hangup_wrong_time():
    nn.log('unit', 'hangup_wrong_time')
    nv.say(mem['hangup_wrong_time'])
    nv.hangup()
    return


@check_call_state()
def hangup_null():
    nn.log('unit', 'hangup_null')
    nv.say(mem['hangup_null'])
    nv.hangup()
    return


@check_call_state()
def forward():
    nv.say(mem['forward'])
    nv.bridge('operator')
    return


@check_call_state()
def hello_main():
    nv.set_default(
        'listen',
        no_input_timeout=4000,
        recognition_timeout=30000,
        speech_complete_timeout=1500,
        asr_complete_timeout=2500
    )
    nn.log('unit', 'hello_main')
    with nv.listen(
        ('None', 'None', 5, 'OR'),
        entities=hello_logic_enitity_list
    ) as r:
        pass
    return hello_logic(r)


@check_call_state()
def hello_logic(r):
    nn.log('unit', 'hello_logic')
    hello_logic_count = nn.counter('hello_logic', '+')
    if hello_logic_count >= 10:
        nn.log('Recursive callback detected')
        nv.say(mem['hangup_wrong_time'])
        nv.hangup()
        return
    if not r:
        nn.log('condition', 'NULL')
        return hello_null()
    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return recommend_main()
    if r.has_entity('repeat'):
        nn.log('condition', 'repeat=True')
        return hello_repeat()
    if r.has_entity('confirm'):
        nn.log('condition', 'confirm=True')
        return recommend_main()
    if not r.has_entity('confirm'):
        nn.log('condition', 'confirm=False')
        return hangup_wrong_time()
    if r.has_entity('wrong_time'):
        nn.log('condition', 'wrong_time=True')
        return hangup_wrong_time()


@check_call_state()
def play_main(prompt_text="hello"):
    nv.set_default(
        'listen',
        no_input_timeout=4000,
        recognition_timeout=30000,
        speech_complete_timeout=1500,
        asr_complete_timeout=2500
    )
    nn.log('unit', 'recommend_main')
    with nv.listen(
        ('None', 'None', 5, 'OR'),
        entities=main_logic_enitity_list
    ) as r:
        pass
    return main_logic(r)


@check_call_state()
def main_logic(r):
    main_logic_count = nn.counter('main_logic', '+')
    if main_logic_count >= 10:
        nn.log('Recursive callback detected')
        nv.say('hangup_wrong_time')
        nv.hangup()
        return

    nn.log('unit', 'main_logic')
    if not r:
        nn.log('condition', 'NULL')
        return recommend_null()

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return recommend_default()

    if r.has_entity('recommendation_score'):
        if 0 <= r.entity('recommendation_score') <= 8:
            nn.log('condition', 'recommendation_score=negative_score')
            return hangup_negative()
        else:
            nn.log('condition', 'recommendation_score=positive_score')
            return hangup_positive()

    if r.has_entity('recommendation') == 'positive':
        nn.log('condition', 'recommendation=positive')
        return recommend_score_positive()

    if r.has_entity('recommendation') == 'neutral':
        nn.log('condition', 'recommendation=neutral')
        return recommend_score_neutral()

    if r.has_entity('recommendation') == 'negative':
        nn.log('condition', 'recommendation=negative')
        return recommend_score_negative()

    if r.has_entity('repeat'):
        nn.log('condition', 'repeat=True')
        return recommend_repeat()

    if r.has_entity('recommendation') == 'dont_know':
        nn.log('condition', 'recommendation=dont_know')
        return recommend_repeat_2()

    if r.has_entity('wrong_time'):
        nn.log('condition', 'wrong_time=True')
        return hangup_wrong_time()

    if r.has_entity('question'):
        nn.log('condition', 'question=True')
        return forward()


def after_call_failed():
    nn.log('unit', 'after_call_success')
    nn.env('status', '-ERR')
    nn.env('result', None)
    nn.log('unit', 'after_call_fail')
    tz = nn.get_time_zone(nn.dialog['msisdn'])
    try:
        nn.env('region', str(tz['location']))
    except KeyError:
        nn.log('Неправильно указан номер')

    attempt = nn.env('attempt')
    nn.log('attempt', attempt)
    recall_count = nn.get_recall_count()
    if not recall_count:
        recall_count = 0
    nn.log('recall_count', recall_count)
    recall_delay = nn.get_recall_delay()
    if not recall_delay:
        recall_delay = 0
    nn.log('recall_delay', recall_delay)
    if attempt >= recall_count:
        nn.log('Использованы все попытки перезвонов')
        nn.dump()
        nn.dialog.result_list_of_conv = nn.RESULT_DONE
        return
    nn.log('attempt', attempt)
    nn.call(
        '+7' + nn.dialog['msisdn'],
        'recall_delay',
        entry_point='main_online_container',
        on_success_call='after_call_success',
        on_failed_call='after_call_fail',
        proto_additional={
                'caller_id': '74951285170',
                'Remote-Party-ID': '<tel:74951285170>;party=calling;',
        }, 
    )

    nn.dump()
    return


def after_call_success():
    nn.env('status', '+OK')
    nn.log('unit', 'after_call_success')

    nn.env('uuid', nn.env('call_uuid'))
    tz = nn.get_time_zone(nn.dialog['msisdn'])
    try:
        nn.env('region', str(tz['location']))
    except KeyError:
        nn.log('Неправильно указан номер')
    attempt = nn.env('attempt')
    if not attempt:
        attempt = 5
    nn.log('attempt', attempt)
    recall_count = nn.get_recall_count()
    if not recall_count:
        recall_count = 0
    nn.log('recall_count', recall_count)
    recall_delay = nn.get_recall_delay()
    if not recall_delay:
        recall_delay = "01:00"
    nn.log('recall_delay', recall_delay)
    if attempt >= recall_count:
        nn.log('Ипользованы все попытки перезвонов')
        nn.dump()
        nn.dialog.result_list_of_conv = nn.RESULT_DONE
        return
    nn.log('attempt', attempt)
    if nn.env('recall_is_needed') == 'true':
        nn.log('Создаем звонок из after_call_success')
        nn.call(
            '+7' + nn.dialog['msisdn'],
            recall_delay, 
            entry_point='main_online_container',
            on_success_call='after_call_success',
            on_failed_call='after_call_fail',
            proto_additional={
                'caller_id': '74951285170',
                'Remote-Party-ID': '<tel:74951285170>;party=calling;',
                },
        )
        nn.dump()
        return

    if nn.env('recall_is_needed') == 'true_72':
        nn.log('Создаем звонок из after_call_success')
        nn.call('+7' + nn.dialog['msisdn'],
                datetime.utcnow() + timedelta(days=3),
                entry_point='main_online_container',
                on_success_call='after_call_success',
                on_failed_call='after_call_fail',
                proto_additional={
                    'caller_id': '74951285170',
                    'Remote-Party-ID': '<tel:74951285170>;party=calling;',
                }, )
        nn.dump()
        return


if __name__ == '__main__':
    main()
