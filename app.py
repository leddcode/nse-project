from search import process_search
from scraper import get_scopes, filter_scopes, count_words, get_news

from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key = b'What>do>you>call>a_Russian-that[enjoys}programming?Computin.'


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        req = request.form
        search_query = req.get('search')
        search_period = req.get('period')
        articles = process_search(search_query, search_period)
        return render_template('index.html', articles=articles, search_query=search_query)
    return render_template('index.html')


@app.route('/scopes', methods=["GET", "POST"])
def scopes():
    if not 'theme' in session:
        session['theme'] = 'cyborg'
    if not 'refresh' in session:
        session['refresh'] = 'off'

    scopes = get_scopes()
    authors = (scope['author'] for scope in scopes)

    theme = request.form.get("theme")
    refresh = request.form.get("refresh")

    # POST request - theme switching
    if theme != session.get('theme') and theme is not None:
        session['theme'] = theme
        top_occurrences = count_words(scopes)
        return render_template('scopes.html', scopes=scopes, authors=authors, top=top_occurrences, theme=theme, refresh=session.get('refresh'))

    # POST request - refreshing
    if refresh != session.get('refresh') and refresh is not None:
        session['refresh'] = refresh
        top_occurrences = count_words(scopes)
        return render_template('scopes.html', scopes=scopes, authors=authors, top=top_occurrences, theme=session.get('theme'), refresh=refresh)
    
    # POST request - search
    if request.form.get("search_scope"):
        req = request.form
        search_query = req.get('search_scope')
        filtered_scopes = filter_scopes(search_query, scopes)
        return render_template('scopes.html', scopes=filtered_scopes, authors=authors, theme=session.get('theme'), refresh=session.get('refresh'))

    # GET request
    top_occurrences = count_words(scopes)
    return render_template('scopes.html', scopes=scopes, authors=authors, top=top_occurrences, theme=session.get('theme'), refresh=session.get('refresh'))


@app.route('/scopes/author/<id>', methods=["GET", "POST"])
def author_posts(id=None):
    scopes = get_scopes()
    author_scopes = (scope for scope in scopes if scope['author'] == id)
    authors = (scope['author'] for scope in scopes)

    theme = request.form.get("theme")
    refresh = request.form.get("refresh")

    # POST request - theme switching
    if theme != session.get('theme') and theme is not None:
        session['theme'] = theme
        return render_template('scopes.html', scopes=author_scopes, authors=authors, id=id, theme=theme, refresh=session.get('refresh'))

    # POST request - refreshing
    if refresh != session.get('refresh') and refresh is not None:
        session['refresh'] = refresh
        return render_template('scopes.html', scopes=author_scopes, authors=authors, id=id, theme=session.get('theme'), refresh=refresh)

    # POST request - search
    if request.form.get("search_scope"):
        req = request.form
        search_query = req.get('search_scope')
        filtered_scopes = filter_scopes(search_query, author_scopes)
        return render_template('scopes.html', scopes=filtered_scopes, authors=authors, id=id, theme=session.get('theme'), refresh=session.get('refresh'))
    
    # GET request
    return render_template('scopes.html', scopes=author_scopes, authors=authors, id=id, theme=session.get('theme'), refresh=session.get('refresh'))


@app.route('/scopes/top/<id>', methods=["GET", "POST"])
def top_posts(id=None):
    scopes = get_scopes()
    top_scopes = [scope for scope in scopes if id in scope["text"].split()]
    authors = [scope['author'] for scope in scopes]
    top_occurrences = count_words(scopes)

    theme = request.form.get("theme")
    refresh = request.form.get("refresh")

    # POST request - theme switching
    if theme != session.get('theme') and theme is not None:
        session['theme'] = theme
        return render_template('scopes.html', scopes=top_scopes, authors=authors, top=top_occurrences, theme=theme, refresh=session.get('refresh'))

    # POST request - refreshing
    if refresh != session.get('refresh') and refresh is not None:
        session['refresh'] = refresh
        return render_template('scopes.html', scopes=top_scopes, authors=authors, top=top_occurrences, theme=session.get('theme'), refresh=refresh)

    # POST request - search
    if request.form.get("search_scope"):
        req = request.form
        search_query = req.get('search_scope')
        filtered_scopes = filter_scopes(search_query, top_scopes)
        return render_template('scopes.html', scopes=filtered_scopes, authors=authors, id=id, theme=session.get('theme'), refresh=session.get('refresh'))

    # GET request
    return render_template('scopes.html', scopes=top_scopes, authors=authors, id=id, top=top_occurrences, theme=session.get('theme'), refresh=session.get('refresh'))


@app.route('/news', methods=["GET", "POST"])
def news():
    if not 'theme' in session:
        session['theme'] = 'cyborg'
    if not 'refresh' in session:
        session['refresh'] = 'off'

    news = get_news()
    sources = [n['source'] for n in news]

    theme = request.form.get("theme")
    refresh = request.form.get("refresh")

    # POST request - theme switching
    if theme != session.get('theme') and theme is not None:
        session['theme'] = theme
        return render_template('news.html', news=news, sources=sources, theme=theme, refresh=session.get('refresh'))

    # POST request - refreshing
    if refresh != session.get('refresh') and refresh is not None:
        session['refresh'] = refresh
        return render_template('news.html', news=news, sources=sources, theme=session.get('theme'), refresh=refresh)

    return render_template('news.html', news=news, sources=sources, theme=session.get('theme'), refresh=session.get('refresh'))


@app.route('/news/source/<id>', methods=["GET", "POST"])
def source_news(id=None):
    news = get_news()
    filtered_news = (n for n in news if n['source'] == id)
    sources = (n['source'] for n in news)

    theme = request.form.get("theme")
    refresh = request.form.get("refresh")

    # POST request - theme switching
    if theme != session.get('theme') and theme is not None:
        session['theme'] = theme
        return render_template('news.html', news=filtered_news, sources=sources, id=id, theme=theme, refresh=session.get('refresh'))

    # POST request - refreshing
    if refresh != session.get('refresh') and refresh is not None:
        session['refresh'] = refresh
        return render_template('news.html', news=filtered_news, sources=sources, id=id, theme=session.get('theme'), refresh=refresh)

    # GET request
    return render_template('news.html', news=filtered_news, sources=sources, id=id, theme=session.get('theme'), refresh=session.get('refresh'))


if __name__ == "__main__":
    app.run()
