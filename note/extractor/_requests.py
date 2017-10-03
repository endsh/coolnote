# coding: utf-8
import random
import requests
from ._file import load_json
from .encode import coding
from .urls import url2index

__all__ = [
	'get',
]

DEFAULT_AGENTS = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0']
AGENTS = load_json('user-agents.json') or DEFAULT_AGENTS


def patch_requests():
	prop = requests.models.Response.content

	def _text(self):
		_content = prop.fget(self)
		return coding(_content, 'utf-8')

	requests.models.Response._text = property(_text)

patch_requests()


def get(url, **options):
	max_len = options.get('max_len', 0)
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip,deflate,sdch',
		'User-Agent': random.choice(AGENTS),
	}
	if options.get('user_agent') == 'pc':
		headers['User-Agent'] = DEFAULT_AGENTS[0]
	if 'headers' in options:
		headers.update(options['headers'])
	if 'Referer' not in headers:
		headers['Referer'] = url2index(url)
	allow_types = options.get('allow_types', ['text/html','text/xml'])

	if options.get('debug'):
		for key, value in headers.iteritems():
			print key, value
	
	try:
		resp = requests.get(url, headers=headers, stream=True)
	except Exception, e:
		raise e
	else:
		if options.get('resp'):
			return resp
		if resp.status_code < 200 \
				or resp.status_code >= 400 \
				or resp.status_code >= 300 and not options.get('redirect'):
			resp.close()
			raise ValueError('requests get return status code [%d].' 
				% resp.status_code)

		if allow_types and not '*/*' in allow_types:
			content_type = resp.headers.get('content-type', '')
			if not filter(lambda x: content_type.find(x) >= 0, allow_types):
				resp.close()
				raise ValueError('Content-Type [%s] is not allowed.' % content_type)

		length = int(resp.headers.get('content-length', max_len))
		if max_len > 0 and length > max_len:
			resp.close()
			raise ValueError('Content-Length [%d] is too long.' % lenght)

		if options.get('stream'):
			return resp.content

		html = resp._text
		resp.close()
		return html