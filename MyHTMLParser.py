from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    """My HTML Parser for arXiv RSS feed"""

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []

    def handle_data(self, data):
        """get content

        Args:
            data: string written in html format (example: "<p>hello world </p>")

        """
        if data.strip(" ") != ",":
            self.data.append(data.strip(" "))

