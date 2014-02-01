import lxml
import requests


def get_title(url):
    try:
        headers = {"User-Agent": "SmartBot"}
        page = requests.get(url, headers=headers, timeout=5, stream=True)
        if page.status_code == 200 and page.headers.get("Content-Type", "").startswith("text/html"):
            try:
                tree = lxml.html.fromstring(page.text)
            except ValueError: # lxml seems to have issues with unicode
                tree = lxml.html.fromstring(page.content)
            title = tree.cssselect("title")[0].text_content()
            return title.strip().replace("\n", "").replace("\r", "")
    except requests.exceptions.Timeout:
        return "Timeout!"
    except IndexError: # no title element
        return "No title."
