import webbrowser

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"구글에서 '{query}'를 검색합니다."
