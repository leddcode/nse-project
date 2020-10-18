from collections import Counter

import requests
from bs4 import BeautifulSoup


def get_scopes():
    req = requests.get("https://rotter.net/forum/listforum.php")
    charset = req.encoding
    content = req.text.encode(charset)

    soup = BeautifulSoup(content, "html.parser")
    scopes = soup.find_all("tr", {"bgcolor": "#FDFDFD"})

    data = []
    for scope in scopes:
        try:
            a_tag = scope.find("a")
            href = a_tag["href"]
            text = a_tag.text
            time = scope.find("font", {"class": "text13b"}).text
            date = scope.find("font", {"color": "000000"}).text
            author = scope.find("font", {"class": "text13r"}).text
            scope_data = {
                "author": author,
                "date": date,
                "href": href,
                "text": text,
                "time": time
            }
            data.append(scope_data)
        except Exception as e:
            print(e)
    return data


def filter_scopes(search_query, scopes):
    exect = []
    possible = []
    search_data = search_query.split()
    for scope in scopes:
        vals = scope.values()
        for val in vals:
            if search_query in val:
                exect.append(scope)
            elif any(elem in val for elem in search_data):
                possible.append(scope)
    return exect + possible


def count_words(scopes):
    words = []
    for scope in scopes:
        words.extend(scope["text"].split())
    c = Counter(word for word in words if word.isalpha() and len(word) > 3)
    return c.most_common(10)


def get_news():
    req = requests.get("https://rotter.net/news/news.php?nws=1")
    charset = req.encoding
    content = req.text.encode(charset)

    soup = BeautifulSoup(content, "html.parser")
    ss = soup.find("center")
    trr = ss.find_all("tr")

    data = []
    for tr in trr:
        try:
            tdd = tr.find_all("td")
            if len(tdd) == 3:
                data.append(
                    {
                        "date": tdd[0].text,
                        "source": tdd[1].text,
                        "title": tdd[2].text,
                        "href": tdd[2].find("a")["href"]
                    }
                )
        except Exception as e:
            print(e)
    return data
