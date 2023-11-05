from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def homepage():
  if request.method == 'POST':
    content = request.form['content']
    return render_template('homepage.html', result=content)
  return render_template('homepage.html')
