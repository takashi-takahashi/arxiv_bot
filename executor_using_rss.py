import requests
from datetime import datetime
from MyHTMLParser import MyHTMLParser
import feedparser

# appropriately set these url
WEB_HOOK_URL_CS_IT = ""
WEB_HOOK_URL_CS_LG = ""
WEB_HOOK_URL_DIS_NN = ""
WEB_HOOK_URL_STAT_MECH = ""
WEB_HOOK_URL_STAT_ML = ""

HOOK_DICTIONARY = {
    "cs.IT": WEB_HOOK_URL_CS_IT,
    "cs.LG": WEB_HOOK_URL_CS_LG,
    "cond-mat.dis-nn": WEB_HOOK_URL_DIS_NN,
    "cond-mat.stat-mech": WEB_HOOK_URL_STAT_MECH,
    "stat.ML": WEB_HOOK_URL_STAT_ML
}


def main():
    for key, url in HOOK_DICTIONARY.items():
        print(key)
        find_new_articles(url, term=key)
        requests.post(url, json={"text": "###### END ######"})


def find_new_articles(WEB_HOOK_URL, term):
    """find new articles and send title, authors and summary to slack

    Args:
        WEB_HOOK_URL: slack web hook url
        term: field

    Returns:
        None
    """

    rss_url = 'http://export.arxiv.org/rss/{0}'.format(term)
    rss_atom = feedparser.parse(rss_url)

    text = "\n".join([
        "=" * 100,
        "*{0} : {1}*".format(datetime.now().strftime("%Y/%m/%d"), term),
        "=" * 100
    ])
    requests.post(WEB_HOOK_URL, json={"text": text})

    for index, entry in enumerate(rss_atom["entries"]):
        title = entry["title"].replace("\n", "")
        print(title)

        link_url = entry["id"]

        author_parser = MyHTMLParser()
        author_parser.feed(entry["author"])
        author_names = ", ".join(author_parser.data)

        summary_parser = MyHTMLParser()
        summary_parser.feed(entry["summary"])
        summary = summary_parser.data[0]

        texts = "\n".join([
            # "#" * 40,
            # "*No. {0}*".format(index + 1),
            # "*TITLE: " + title + "*",
            "*<{0}|{1}>*".format(link_url, title),
            author_names,
            "\n",
            # "   URL: " + link_url,
            # "COMMENT: " + comment,
            "   " + summary
        ])

        requests.post(WEB_HOOK_URL,
                      json={
                          "attachments": [
                              {
                                  # "title": "*{0}*".format(title),
                                  "pretext": "*No.{0} ({1}):*".format(index, term),
                                  "text": texts,
                                  "mrkdwn_in": [
                                      "text",
                                      "pretext",
                                      "title"
                                  ]
                              }
                          ]
                      }
                      )
        requests.post(WEB_HOOK_URL, json={"text": "-" * 10})
        print()


if __name__ == "__main__":
    main()
