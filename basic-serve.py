from bottle import *
import json
from linecache import getline

s = '<script type="text/javascript" async="" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML-full"></script>'

@get('/question/<n:int>')
def frontend(n):
    d = json.loads(getline('data.jsonl', n))
    spec = '\n'.join(d['specs'])
    qs = '\n'.join(d['questions'])
    return '<html>' + s + spec + '\n' + qs + '</html>'

@get('/api/question/<n:int>')
def question_api(n):
    return json.loads(getline('data.jsonl', n))

run()