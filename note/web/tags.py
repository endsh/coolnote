# coding: utf-8
from chiki import json_success, json_error
from flask import Blueprint, request
from flask.ext.login import login_required, current_user
from note.models import Tag

bp = Blueprint('tags', __name__)


def tag2json(word, t):
    return dict(id=t.id, name=t.name, suffix=t.name[len(word):])


@bp.route('/search', methods=['POST'])
def search():
    word = request.form.get('word')
    tag = Tag.objects(name=word).first()
    tags = Tag.objects(
        name__istartswith=word, name__ne=word).order_by('-weight').limit(10)
    if tag:
        res = [tag2json(word, t) for t in ([tag] + list(tags))]
    else:
        res = [dict(id='', name=word)]
        res += [tag2json(word, t) for t in tags]
    return json_success(word=word, tags=res)


@bp.route('/create', methods=['POST'])
@login_required
def create():
    name = request.form.get('name')
    desc = request.form.get('desc')
    if len(name) > 40 or len(name) == 0:
        return json_error(msg='无效的标签')
    tag = Tag.objects(name=name).first()
    if not tag:
        tag = Tag(user=current_user.id, name=name, desc=desc)
        tag.create()
    return json_success(id=tag.id, name=tag.name)
