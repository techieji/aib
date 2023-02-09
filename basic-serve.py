from bottle import *
import json

f = open('data.jsonl', 'r')

"""<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global'
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>"""

s = '<script type="text/javascript" async="" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML-full"></script>'

@get('/')
def serve():
    d = json.loads(next(f))
    return '<html>' + s + '\n'.join(d['questions']) + '</html>'

run()