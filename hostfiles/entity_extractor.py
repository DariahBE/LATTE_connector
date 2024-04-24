# -*- coding: utf-8 -*-
from extract_text_from_db import connect_and_extract as extractor

import sys
import json
import spacy
from spacy import displacy
text = extractor(True)
lang = text[1]
text = text [0]
lookupModel = {
    'el': 'el_core_news_lg',
    'en': 'en_core_web_lg', 
    'fr': 'fr_core_news_md', 
    'de': 'de_core_news_md', 
    'nl': 'nl_core_news_md'
}
usedModel = lookupModel[lang]
nlp = spacy.load(usedModel)
parse = nlp(text)

labelLookup = {
    'PERSON': 'Person',
    'GPE': 'Place', 
    'PER': 'Person',
    'LOC': 'Place'
}

total = 0
result = []
for p in parse.ents:
    if p.label_ in labelLookup:
        labelToShow = labelLookup[p.label_]
    else:
        labelToShow = 'Unspecified'
    total+=1
    subresult = {
        'text': p.text,
        'label': p.label,
        'labelTex':labelToShow,
        'startPos': p.start_char,
        'endPos': p.end_char-1
    }
    result.append(subresult)
print(json.dumps({'meta': {'found_entities_number': total, 'used_model': usedModel}, 'data':result}))