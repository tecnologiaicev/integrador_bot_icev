from bs4 import BeautifulSoup

def limparHtml(html):
    soup = BeautifulSoup(html, "html.parser")

    return soup.text