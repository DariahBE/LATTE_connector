# -*- coding: utf-8 -*-
from extract_text_from_db import connect_and_extract as extractor
import json

#choose which language detector is being used:      #langid or spacy
data = extractor(False)
text = data[0]
implement = data[2]

if implement == 'spacy':
    import spacy
    from spacy.language import Language
    from spacy_langdetect import LanguageDetector
    def get_lang(nlp, name):
        return LanguageDetector()
    nlp = spacy.load("en_core_web_md", disable=['tokenizer', 'ner', 'textcat'])
    Language.factory("language_detector", func=get_lang)
    nlp.add_pipe('language_detector', last=True)
    doc = nlp(text)
    lang = doc._.language['language']               #returns the ISO 639-1 code of a language
    certainty = doc._.language['score']

elif implement == 'langid':
    from langid.langid import LanguageIdentifier, model
    lang_identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    doc = lang_identifier.classify(text) # ('en', 0.999999999999998)
    lang = doc[0]
    certainty = doc[1]



##All language codes supported by langid.py
lookup= {
    'af': 'Afrikaans', 'am': 'Amharic', 
    'an': 'Aragonese', 'ar': 'Arabic',
    'as': 'Assamese', 'az': 'Azerbaijani',
    'be': 'Belarusian', 'bg': 'Bulgarian',
    'bn': 'Bengali', 'br': 'Breton',
    'bs': 'Bosnian', 'ca': 'Catalan',
    'cs': 'Czech', 'cy': 'Welsh',
    'da': 'Danish', 'de': 'German',
    'dz': 'Dzongkha', 'el': 'Greek',
    'en': 'English', 'eo': 'Esperanto',
    'es': 'Spanish', 'et': 'Estonian',
    'eu': 'Basque', 'fa': 'Persian',
    'fi': 'Finnish', 'fo': 'Faroese',
    'fr': 'French', 'ga': 'Irish',
    'gl': 'Galician', 'gu': 'Gujarati',
    'he': 'Hebrew', 'hi': 'Hindi',
    'hr': 'Croatian', 'ht': 'Haitian Creole',
    'hu': 'Hungarian', 'hy': 'Armenian',
    'id': 'Indonesian', 'is': 'Icelandic',
    'it': 'Italian', 'ja': 'Japanese',
    'jv': 'Javanese', 'ka': 'Georgian',
    'kk': 'Kazakh', 'km': 'Central Khmer',
    'kn': 'Kannada', 'ko': 'Korean',
    'ku': 'Kurdish', 'ky': 'Kirghiz',
    'la': 'Latin', 'lb': 'Luxembourgish',
    'lo': 'Lao', 'lt': 'Lithuanian',
    'lv': 'Latvian', 'mg': 'Malagasy',
    'mk': 'Macedonian', 'ml': 'Malayalam',
    'mn': 'Mongolian', 'mr': 'Marathi',
    'ms': 'Malay', 'mt': 'Maltese',
    'nb': 'Norwegian Bokmål', 'ne': 'Ndonga',
    'nl': 'Dutch', 'nn': 'Norwegian Nynorsk',
    'no': 'Norwegian', 'oc': 'Occitan',
    'or': 'Oriya', 'pa': 'Panjabi',
    'pl': 'Polish', 'ps': 'Pushto',
    'pt': 'Portuguese', 'qu': 'Quechua',
    'ro': 'Romanian', 'ru': 'Russian',
    'rw': 'Kinyarwanda', 'se': 'Northern Sami',
    'si': 'Sinhalese', 'sk': 'Slovak',
    'sl': 'Slovenian', 'sq': 'Albanian',
    'sr': 'Serbian', 'sv': 'Swedish',
    'sw': 'Swahili', 'ta': 'Tamil',
    'te': 'Telugu', 'th': 'Thai',
    'tl': 'Tagalog', 'tr': 'Turkish',
    'ug': 'Uighur', 'uk': 'Ukrainian',
    'ur': 'Urdu', 'vi': 'Vietnamese',
    'vo': 'Volapük', 'wa': 'Walloon',
    'xh': 'Xhosa', 'zh': 'Chinese',
    'zu': 'Zulu'
}
langString = lookup[lang]
print(json.dumps({'languageCode':lang, 'language': langString, 'certainty':certainty}))
