# coding: utf-8
from flask import current_app
from note.models import Question


def run():
    for key in current_app.redis.keys('qv_*'):
        views = current_app.redis.scard(key)
        current_app.redis.delete(key)
        Question.objects(id=int(key[3:])).update(inc__views=views)
