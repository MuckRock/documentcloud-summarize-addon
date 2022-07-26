"""
A Flask app that routes http requests to summarize().
"""
from flask import Flask, render_template, request, url_for, flash, redirect
from .summarize.summarize import summarize

app = Flask(__name__)
app.config['SECRET_KEY'] = '2af224ae93084a1385c8e8cb4a6724448c548c19891cbb17'

summary = '[Summary will appear here.]'

@app.route("/", methods=('GET', 'POST'))
def index():
    global summary
    if request.method == 'POST':
        content = request.form['content']

        if not content:
            flash('Content is required!')
        else:
            flash('Starting summarization…')
            summary = summarize(
              content,
              sentence_to_cluster_ratio = int(request.form['sentence_to_cluster_ratio'])
            )
            return redirect(url_for('index'))

    return render_template('index.html', summary=summary)
