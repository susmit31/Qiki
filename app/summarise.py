import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
import json
from bs4 import BeautifulSoup

def fetch_article(url, title):
    query_params = {'origin':'*', 'action':'parse', 'page': title, 'format':'json'}
    res = requests.get(url, params=query_params)
    html = res.json()['parse']['text']['*']
    parsed = BeautifulSoup(html, features='lxml')

    txt = ''
    for para in parsed.find_all('p'):
        txt += para.text + '\n'

    return txt
    
def summarize_text(text, n_sent=30):
    # Tokenize text
    text_sm = text.lower()
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords = set(stopwords + list(punctuation))
    text_sents_tok = nltk.tokenize.sent_tokenize(text_sm)
    text_words_tok = [nltk.tokenize.word_tokenize(stc) for stc in text_sents_tok] 
    text_toks = [word for stc in text_words_tok for word in stc]
    text_toks = [word for word in text_toks if word not in stopwords]
    
    # Compute frequencies
    freqs = {tok:0 for tok in text_toks}
    maxfreq = 0
    for tok in text_toks:
        freqs[tok] += 1
        if freqs[tok] > maxfreq:
            maxfreq = freqs[tok]
    freqs = {f: freqs[f]/maxfreq for f in freqs}

    # Rank sentences
    sent_scores = [0 for i in range(len(text_sents_tok))]
    for i in range(len(text_words_tok)):
        s = text_words_tok[i]
        score = 0
        for w in s:
            score += freqs.get(w,0)
        sent_scores[i] = score
    ranked = sorted(list(range(len(sent_scores))), key=lambda i: -sent_scores[i])[:n_sent]
    print(ranked)
    
    # Make summary
    summary = ''
    text_sent = sent_tokenize(text)
    for i in range(len(text_sent)):
        if i in ranked:
            summary +=' '+text_sent[i]
            
    return summary.strip()
