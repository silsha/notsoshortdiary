#!/usr/bin/env python
from flask import Flask, render_template
import requests
import dateutil.parser
import re
from jinja2 import evalcontextfilter, Markup, escape

app = Flask(__name__)
 
with open('username', 'r') as userfile:
        username = userfile.readline().rstrip()
with open('password', 'r') as pwfile:
	password = pwfile.readline().rstrip()

@app.route('/')

def index():
	r = requests.get('https://shortdiary.me/api/v1/posts/', auth=(username, password))
	posts = filter(lambda p: p['public'], r.json())
	return render_template("index.html", posts=posts)

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%b %d, %Y'
    return native.strftime(format) 
    
@app.template_filter()
@evalcontextfilter
def linebreaks(eval_ctx, value):
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)

if __name__ == '__main__':
	app.run(debug=True)
