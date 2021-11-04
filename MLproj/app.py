import os
import sys
import pymysql
from seqtolang import Detector
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

detector = Detector()

if (os.environ.get('SEQTOLANG_TEXT') is None):
    print("Make sure to pass SEQTOLANG_TEXT environment variable.")
    sys.exit(1)

dbsrv = os.environ['sqlhost']
user = os.environ['sqluser']
pw = os.environ['sqlsec']
db = os.environ['sqldb']
conn = pymysql.connect(host=dbsrv, user=user, passwd=pw, db=db)
cur = conn.cursor()

text = os.environ['SEQTOLANG_TEXT']

tokens = detector.detect(text)

RLanguage = tokens[0][0]

print(RLanguage)

classifier = pipeline('sentiment-analysis')

m = classifier(text)

Score = m[0]['score']
SClass = m[0]['label']

print(m)

q = """insert into Reviews (filename, username, moviename, releaseyear, producer, director, originalreview, translated, rlanguage, score, sclass ) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

if (RLanguage == 'eng'):
    cur.execute(q, (os.environ['FileName'], os.environ['UserName'], os.environ['MovieName'], os.environ['ReleaseYear'], os.environ['Producer'], os.environ['Director'], text, text, RLanguage, Score, SClass))
    conn.commit()

elif (RLanguage == 'de' or RLanguage == 'deu'):

    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-en")
    tokenized_text = tokenizer.prepare_seq2seq_batch([text], return_tensors='pt')
    translation = model.generate(**tokenized_text)
    translated_text = tokenizer.batch_decode(translation, skip_special_tokens=True)[0]
    print(translated_text)
    cur.execute(q, (os.environ['FileName'], os.environ['UserName'], os.environ['MovieName'], os.environ['ReleaseYear'], os.environ['Producer'], os.environ['Director'], text, translated_text, RLanguage, Score, SClass))
    conn.commit()

elif (RLanguage == 'fr' or RLanguage == 'fra'):

    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
    tokenized_text = tokenizer.prepare_seq2seq_batch([text], return_tensors='pt')
    translation = model.generate(**tokenized_text)
    translated_text = tokenizer.batch_decode(translation, skip_special_tokens=True)[0]
    print(translated_text)
    cur.execute(q, (os.environ['FileName'], os.environ['UserName'], os.environ['MovieName'], os.environ['ReleaseYear'], os.environ['Producer'], os.environ['Director'], text, translated_text, RLanguage, Score, SClass))
    conn.commit()