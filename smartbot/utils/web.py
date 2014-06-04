import lxml
import requests


def requests_session():
    """
    Get a suitable requests session for use in SmartBot.

    In particular, this sets the `User-Agent` header to the value of
    'SmartBot'.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": "SmartBot"})
    return session


def _check_content_type(response, content_type="text/html"):
    return response.headers.get("Content-Type", "").startswith(content_type)


def get_title(url):
    """Get the title of a website."""
    try:
        page = requests_session().get(url, timeout=5, stream=True)
        if page.status_code == 200 and _check_content_type(page):
            try:
                tree = lxml.html.fromstring(page.text)
            except ValueError:  # lxml seems to have issues with unicode
                tree = lxml.html.fromstring(page.content)

            title = tree.cssselect("title")[0].text_content()
            return title.strip().replace("\n", "").replace("\r", "")
    except requests.exceptions.Timeout:
        return "Timeout!"
    except IndexError:  # no title element
        return "No title."


def sprunge(data):
    """Upload the data to `sprunge.us` (a popular plain-text paste bin)."""
    payload = {"sprunge": data}
    page = requests_session().post("http://sprunge.us", data=payload)
    return page.text
