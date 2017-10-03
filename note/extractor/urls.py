# coding: utf-8
import re
import tldextract
import urllib
import urlparse

__all__ = [
	'url2scheme', 'url2host', 'url2domain', 'url2subdomain',
	'url2path', 'url2format', 'url2index', 'url2subindex',
	'resolve_url', 'is_abs_url',
]


def url2scheme(url):
	return urlparse.urlparse(url, **kwargs).scheme if url else ''


def url2host(url, **kwargs):
	return urlparse.urlparse(url, **kwargs).netloc if url else ''


def url2domain(url, **kwargs):
	if not url:
		return ''
	ext = tldextract.extract(url, **kwargs)
	return ('%s.%s' % (ext.domain, ext.suffix)).lower()


def url2subdomain(url, **kwargs):
	if not url:
		return []
	return list(reversed(tldextract.extract(url, **kwargs).subdomain.split('.')))


def url2path(url, **kwargs):
	return urlparse.urlparse(url, **kwargs).path if url else ''


def url2format(url):
	path = url2path(url)
	if not path:
		return ''
	path = path[:-1] if path.endswith('/') else path
	chunks = [x for x in path.split('/') if len(x) > 0]
	last = chunks[-1].split('.') if chunks else []
	return last[-1] if len(last) >= 2 else ''


def url2index(url):
	return 'http://www.%s' % url2domain(url)


def url2subindex(url):
	return 'http://%s' % url2host(url)


def resolve_url(url, **kwargs):
	if not url:
		return ''

	res = urlparse.urlparse(url, **kwargs)
	url = '%s://%s%s' % (res.scheme, res.netloc, res.path)
	if res.query and '.htm' not in url:
		params = {}
		for key, value in urlparse.parse_qs(res.query).iteritems():
			if re.match('^[\w\-_=]*$', value[0]):
				params[key] = value[0]
		if params:
			url += '?%s' % '&'.join(['%s=%s' % x for x in params.iteritems()])
	return url[:-1] if url and url[-1] == '/' else url


def is_abs_url(url):
	regex = re.compile(
		r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
		r'localhost|' # localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
		r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	return regex.search(url) != None