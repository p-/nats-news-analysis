from io import BytesIO

import feedparser
import requests
import ssl

# https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


def retrieve_article_links(feedurl):
    article_urls = []

    try:
        # https://stackoverflow.com/questions/9772691/feedparser-with-timeout
        resp = requests.get(feedurl,
                            verify=True,
                            timeout=10.0
                            )
        content = BytesIO(resp.content)
        feed = feedparser.parse(content)

        for entry in feed['entries']:
            article_urls.append(entry.link)

    except Exception as e:
        print("Retrieval failed:", feedurl)
        print(e)

    article_urls = list(filter(None, article_urls))
    article_urls = list(filter(lambda item: item.startswith('http'), article_urls))
    article_urls = [i.strip() for i in article_urls]

    print("Found", len(article_urls), "articles")

    if len(article_urls) == 0:
        print("WARNING: No article URLs found in feed", feedurl)
        if feedurl.startswith("http://"):
            print("Retrying with https")
            return retrieve_article_links(feedurl.replace("http:", "https:"))

    return article_urls


if __name__ == "__main__":
    print(retrieve_article_links('https://www.hessenschau.de/index.rss'))
    print(retrieve_article_links('https://katapult-magazin.de/feed/rss'))
    print(retrieve_article_links('https://www.tomshardware.com/feeds/all'))
