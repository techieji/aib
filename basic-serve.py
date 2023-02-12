from bottle import *
import json
from linecache import getline

s = '<script type="text/javascript" async="" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML-full"></script>'

# hook('after_request')
# def enable_cors():
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@get('/question/<n:int>')
def frontend(n):
    d = json.loads(getline('data.jsonl', n))
    spec = '\n'.join(d['specs'])
    qs = '\n'.join(d['questions'])
    return '<html>' + s + spec + '\n' + qs + '</html>'

@get('/api/question/<n:int>')
def question_api(n):
    response.headers['Access-Control-Allow-Origin'] = '*'
<<<<<<< HEAD
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'
=======
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
>>>>>>> 4d19ac649619d4aafea63aed8a56517bf0a96369
    return json.loads(getline('data.jsonl', n))

run()
