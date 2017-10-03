# coding: utf-8
from ._requests import get
from .html import clean_html, doc2html, html2doc
from .clean import clean_content


class Extractor(object):

    def __init__(self, input, url, **kwargs):
        self.url = url
        self.doc = clean_html(input, url, todoc=True)
        self.body = self.doc.find('body')
        if self.body is None:
            raise ValueError('body is not found.')
        self.html = doc2html(self.doc)
        self.content_selector = kwargs.get('content_selector')
        self.title_selector = kwargs.get('title_selector')

    @property
    def title(self):
        if not hasattr(self, '_title'):
            self._title = self.xtitle
        return self._title

    @property
    def xtitle(self):
        node = self.doc.cssselect(self.title_selector)
        return (node and node[0].text or '').strip()

    @property
    def images(self):
        images = set()
        for img in html2doc(self.content).iter('img'):
            src = img.get('src')
            if src and src.strip():
                images.add(src.strip())
        return list(images)

    @property
    def content(self):
        if not hasattr(self, '_content'):
            self._content = self.xcontent
        return self._content

    @property
    def xcontent(self):
        node = self.doc.cssselect(self.content_selector)
        return doc2html((node or None) and node[0])

    @property
    def lines(self):
        return [doc2html(node) for node in html2doc(self.content).getchildren()]

    def article(self):
        return dict(title=self.title, images=self.images, content=self.content, lines=self.lines)


def url2article(url, **kwargs):
    html = get(url)
    extractor = Extractor(html, url, **kwargs)
    return extractor.article()
