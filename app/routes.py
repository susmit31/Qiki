from flask import render_template, redirect, url_for
from app import app
from app.forms import SearchForm
import sys
from app.summarise import fetch_article, summarize_text

pgs = {'index': 'Home', 'search':'Find', 'browse': 'Browse'}

@app.route('/')
def index():
    return "Ahoy matey!"

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.query.data
        is_url = form.is_url.data
        print((query, is_url), file=sys.stdout)
        return redirect(url_for('summary', title=query))
    return render_template('search.html', title='search', form=form, pgs = pgs)

@app.route('/browse')
def browse():
    return '<h1>Nvm dude</h1>'

@app.route('/summary/<title>')
def summary(title):
    article_txt = fetch_article('https://en.wikipedia.org/w/api.php',title)
    summary = summarize_text(article_txt, n_sent=25)
    return render_template('summary.html', summary=summary)
