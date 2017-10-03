# coding: utf-8
import os
import json

__all__ = [
	'load_file', 'save_file', 'remove_file', 'get_data_path',
	'load_data', 'save_data', 'remove_data', 'has_data',
	'append_data', 'load_json', 'save_json',
]

DATA_ROOT = os.path.abspath(os.path.dirname(__file__))


def load_file(path):
	if os.path.isfile(path):
		with open(path) as fd:
			return fd.read()


def save_file(path, content, mode='w+', force=True):
	folder = path[:path.rfind('/')]
	if not os.path.exists(folder):
		if not force:
			return
		os.makedirs(folder)
	with open(path, mode) as fd:
		return fd.write(content)


def remove_file(path):
	if os.path.isfile(path):
		os.remove(path)


def get_data_path(name):
	return os.path.join(DATA_ROOT, name)


def load_data(name):
	return load_file(get_data_path(name))


def save_data(name, content, mode='w+'):
	return save_file(get_data_path(name), content, mode)


def remove_data(name):
	return remove_file(get_data_path(name))


def has_data(name):
	return os.path.isfile(get_data_path(name))


def append_data(name, content):
	return save_data(name, content, 'a+')


def load_json(name):
	content = load_data(name)
	if content:
		return json.loads(content)


def save_json(name, obj):
	return save_data(name, json.dumps(obj))
