# -*- coding: utf-8 -*-
import requests


# text - переводимый текст
# sourceLangauge (auto, en, uh, ru) - язык вводимого текста
# targetLangauge (en, uk, ru) - язык в который производится перевод
def request_googleapis_translate_a(text: str, sourceLangauge: str = 'auto', targetLanguage: str = 'ru'):
    params = {
        'client': 'gtx',
        'dt': 't',
        'dj': 1,
        'sl': sourceLangauge,
        'tl': targetLanguage,
        'q': text,
    }

    url: str = 'https://translate.googleapis.com/translate_a/single'
    response = requests.get(url=url, params=params, timeout=30)

    if response.status_code != requests.codes.ok:
        response.raise_for_status()

    answer = response.json()
    sentences = (sentence['trans'] for sentence in answer['sentences'])     # сбор всех предложений из json

    return ' '.join(sentences)
