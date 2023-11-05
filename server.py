from datetime import date
from flask import Flask, render_template, request
from shuffler import get_shuffle_response

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def homepage():
  if request.method == 'POST':
    content = request.form['content']
    result = get_shuffle_response(request=content, date=date.today(),
                                  enable_extraction=True)
    return render_template('homepage.html', result=result)
  return render_template('homepage.html')
