import requests
from datetime import datetime
import feedparser

# appropriately set these url
WEB_HOOK_URL_ALL = ""
WEB_HOOK_URL_CS_IT = ""
WEB_HOOK_URL_CS_LG = ""
WEB_HOOK_URL_DIS_NN = ""
WEB_HOOK_URL_STAT_MECH = ""
WEB_HOOK_URL_STAT_ML = ""

HOOK_DICTIONARY = {
    "ALL": WEB_HOOK_URL_ALL,
    "cs.IT": WEB_HOOK_URL_CS_IT,
    "cs.LG": WEB_HOOK_URL_CS_LG,
    "cond-mat.dis-nn": WEB_HOOK_URL_DIS_NN,
    "cond-mat.stat-mech": WEB_HOOK_URL_STAT_MECH,
    "stat.ml": WEB_HOOK_URL_STAT_ML
}


def main():
    for key, url in HOOK_DICTIONARY.items():
        print(key)
        if key == "ALL":
            term_list = [
                "cond-mat.dis-nn",
                "cond-mat.stat-mech",
                "cs.IT",
                "cs.LG",
                "stat.ML"
            ]

            for term in term_list:
                find_new_articles(url, term=term)
            requests.post(WEB_HOOK_URL_ALL, json={"text": "###### END ######"})
        else:
            find_new_articles(url, term=key)
            requests.post(url, json={"text": "###### END ######"})


def find_new_articles(WEB_HOOK_URL, term, max_num_of_results=100):
    """find new articles and send title, authors and summary to slack

    Args:
        WEB_HOOK_URL: slack web hook url
        term: field
        max_num_of_results: max number of results

    Returns:
        None
    """
    query = "cat:{0}&start=0&max_results={1}&sortBy=lastUpdatedDate&".format(term, max_num_of_results)
    url = "http://export.arxiv.org/api/query?search_query=" + query
    atom = feedparser.parse(url)

    day = datetime.now().day
    weekday = datetime.now().isoweekday()
    if weekday == 1:
        diff = 3
    else:
        diff = 1

    text = "\n".join([
        "=" * 100,
        "*{0} : {1}*".format(datetime.now().strftime("%Y/%m/%d"), term),
        "=" * 100
    ])
    requests.post(WEB_HOOK_URL, json={"text": text})
    for index, entry in enumerate(atom["entries"]):
        if entry["updated_parsed"][2] == (day - diff):
            title = entry["title"].replace("\n", "").replace("\n", "").replace("\n", "")
            print(title)

            author_name_list = []
            for author in entry["authors"]:
                author_name_list.append(author["name"])
            author_names = "    " + ", ".join(author_name_list)

            link_url = entry["id"]

            if "arxiv_comment" in entry.keys():
                comment = entry["arxiv_comment"]
            else:
                comment = "None"

            summary = entry["summary"]

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
                                      "pretext": "*No.{0} ({1}):*".format(index + 1, term),
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


if __name__ == "__main__":
    main()
