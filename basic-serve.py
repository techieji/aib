from bottle import *
import json
from linecache import getline
import re

hook('after_request')
def enable_cors():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
    response.set_header('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')

@get('/api/total_question/<n:int>')
def get_question(n):
    enable_cors()
    return json.loads(getline('data.jsonl', n))

@get('/question/<n:int>')
def frontend(n):
    d = get_question(n)
    spec = '\n'.join(d['specs'])
    qs = '\n'.join(d['questions'])
    return f"""
<html>
    <head>
        <script type="text/javascript" async="" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML-full"></script>
    </head>
    <body>
        <a href="/question/{n-1}">Back</a>
        <a href="/question/{n+1}">Next</a><br>
        {spec}<br>
        {qs}
    </body>
</html>    
"""

@get('/api/metadata/<n:int>')
def metadata_api(n):
    return get_question(n)['md']

def extract_math(s):
    l = []
    def sub_fn(m):
        l.append(m.group(0))
        return f"!MATH<{len(l) - 1}>"
    return {
        "non-math": re.sub(r'\\\(.*\\\)', sub_fn, s),
        "extracted-math": l
    }

@get('/api/question/<n:int>')
def question_api(n):
    enable_cors()
    qs = get_question(n)['questions']
    return list(map(extract_math, qs))

run()
