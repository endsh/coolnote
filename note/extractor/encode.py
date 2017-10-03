# coding: utf-8
import re
import chardet
import urllib
from ._file import load_json

__all__ = [
	"get_encode", "coding",
]

CHINESES = re.compile(load_json('chineses.json'))
MIN_LEN = 300


def get_encode(text):
	det = chardet.detect(text)
	if det['encoding']:
		if det['encoding'].lower() == 'iso-8859-2':
			return 'gb2312'
		return det['encoding'].lower()


def coding(text, output='utf-8'):
	encodings = ['utf-8', 'gb2312', 'gbk', 'gb18030', 'big5', 'ascii']
	for enc in encodings:
		try:
			return text.decode(enc).encode(output)
		except UnicodeDecodeError, UnicodeEncodeError:
			pass

	for enc in encodings:
		res = text.decode(enc, 'ignore')
		if len(CHINESES.findall(res)) > MIN_LEN:
			return res.encode(output, 'ignore')

	enc = get_encode(text)
	if not enc:
		return text

	try:
		return text.decode(enc).encode(output)
	except UnicodeDecodeError, UnicodeEncodeError:
		pass

	try:
		res = text.decode(enc, 'ignore')
		if len(CHINESES.findall(res)) > MIN_LEN:
			return res.encode(output, 'ignore')
	except (LookupError, TypeError):
		pass

	return text