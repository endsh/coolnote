# coding: utf-8
import re
import collections
import lxml.etree
import lxml.html
import lxml.html.soupparser
from .urls import url2domain, resolve_url

__all__ = [
	'html2doc', 'doc2html', 'child2html', 'html2text', 
	'doc2text', 'clean_html', 'clean_doc', 'html2urls',
	'html2links', 'doc2urls', 'block_text', 'selector',
	'link_text', 'tags', 'reverse_tags',
]

BLOCK_TAGS = ['div','p','table','td','article','section','pre']
BLOCK_XPATH = '|'.join(['.//%s' % x for x in BLOCK_TAGS])
UTF8_PARSER = lxml.html.HTMLParser(encoding='utf-8')


def html2doc(html, url=None, retry=False):
	try:
		doc = lxml.html.fromstring(html, parser=UTF8_PARSER)
	except lxml.etree.XMLSyntaxError:
		doc = lxml.html.soupparser.fromstring(html)

	if doc.find('body') is not None and 'html' in html and not retry:
		html = re.sub('\0', '', html)
		return html2doc(html, url, True)

	if url:
		doc.make_links_absolute(url, resolve_base_href=True)
	return doc


def doc2html(doc, default=''):
	return lxml.html.tostring(doc, encoding='utf-8') if doc is not None else default


def child2html(doc, default=''):
	return ''.join(doc2html(x) for x in doc.getchildren()) if doc is not None else default


def html2text(html, code=False):
	return doc2text(html2doc(html), code=code)


def doc2text(doc, code=False):
	if doc is None:
		return ''
	if not code:
		[x.drop_tree() for x in doc.iter('pre')]
	return doc.text_content()


def clean_html(html, url=None, todoc=False):
	return clean_doc(html2doc(html, url=url), tohtml=not todoc)


def clean_doc(doc, tohtml=False):
	xpath = './/script | .//style | .//noscript | .//comment()'
	for node in doc.xpath(xpath):
		node.drop_tree()
	clean_empty_node(doc)
	return doc2html(doc) if tohtml else doc


def clean_empty_node(doc):
	count = 0
	for node in doc.iter():
		if node.tag in ['img', 'br', 'meta']:
			continue

		if node.tag == 'link' \
				and node.get('rel') != 'stylesheet' \
				and node.get('type') != 'text/css':
			continue

		if node.getparent() is not None \
				and not node.getchildren() \
				and (not node.text or not node.text.strip()):
			node.drop_tree()
			count += 1

	if count >= 1:
		clean_empty_node(doc)

	return doc


def html2urls(html, url=None, title=False):
	return doc2urls(html2doc(html, url), url2domain(url), title=title)


def html2links(html, url, title=False):
	return doc2urls(html2doc(html, url), url2domain(url), link=True, title=title)


def doc2urls(doc, domain=None, link=False, title=False):
	urls = collections.defaultdict(list) if title else set()
	for a in doc.iter('a'):
		url = a.get('href')
		text = a.text_content() or a.get('title')
		if not url or not url.strip() or len(url) > 256 \
				or not text or not text.strip() \
				or not url.startswith('http://') \
				or re.search('bbs|[\/.](t|v|d)\.|video|about|thread|forum|down', url) \
				or not link and domain and domain != url2domain(url) \
				or link and domain and domain == url2domain(url):
			continue
		url = resolve_url(url)
		if title:
			urls[url.strip()].append(text.strip())
		else:
			urls.add(url.strip())
	return urls if title else list(urls)


def block_text(node, default=''):
	if node is None:
		return default

	blocks = len(node.xpath(BLOCK_XPATH))
	children = len(node.getchildren())
	if blocks > 1 or blocks == 1 \
			and node.tag not in BLOCK_TAGS \
			and (node.text and node.text.strip() or children > 1):
		return default

	text = ''
	for child in node.iter():
		if child.text:
			text += child.text.strip()
		if child != node and child.tail:
			text += child.tail.strip()
	return text


def selector(node, default=''):
	if node is not None:
		path, id, cls = str(node.tag), node.get('id'), node.get('class')
		if id and not re.search('\d{2,}', id):
			return '%s#%s' % (path, id)
		if cls and not re.search('\d{2,}', cls):
			path = '%s.%s' % (path, '.'.join(cls.split()))
		if node.getparent() is not None:
			return '%s > %s' % (selector(node.getparent()), path)
		return path
	return default


def link_text(node):
	if node.tag == 'a':
		return node.text_content().strip()
	else:
		return (node.text or '').strip()


def tags(node, *tag_names):
	xpath = ' | '.join('.//%s' % x for x in tag_names)
	for e in node.xpath(xpath):
		yield e


def reverse_tags(node, *tag_names):
	xpath = ' | '.join('.//%s' % x for x in tag_names)
	for e in reversed(node.xpath(xpath)):
		yield e