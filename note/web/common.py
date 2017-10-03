# coding: utf-8
from chiki.contrib.common import Item
from chiki.utils import get_ip
from flask import Blueprint, render_template, current_app
from note.models import Tag, Question, Answer
from note.forms import AnswerForm

bp = Blueprint('common', __name__)
TAGS = '基础算法|数据结构|图论算法|动态规划|搜索算法|数学|计算几何学'


@bp.route('/')
def index():
    tags = Item.list('algorithm_tags', TAGS, coerce=str)
    data = []
    for tag in tags:
        subs = []
        t = Tag.objects(name=tag).first()
        if t:
            subs = list(Tag.objects(parents=t).order_by('-weight').limit(20))
        questions = Question.objects(
            tags__in=subs + [t]).order_by('-weight').limit(9)
        if questions:
            data.append(dict(tag=tag, subs=subs[:8], questions=questions))
    return render_template('common/index.html', data=data)


@bp.route('/questions/<id>')
def question(id):
    form = AnswerForm()
    q = Question.objects(id=id).get_or_404()
    related = Question.objects(
        id__ne=id, tags__in=q.tags).order_by('-week_weight').limit(8)
    query = Answer.objects(question=q).order_by('-created')
    current_app.redis.sadd('qv_%s' % q.id, get_ip())
    return query.paginate(id=id).render(
        'common/question.html', question=q, related=related, form=form)


@bp.route('/tags/<name>')
def tag(name):
    t = Tag.objects(name=name).get_or_404()
    subs = list(Tag.objects(parents=t).order_by('-weight').limit(20))
    hottest = Question.objects.order_by('-week_weight').limit(8)
    newest = Question.objects.order_by('-created').limit(8)
    query = Question.objects(tags__in=subs + [t]).order_by('-weight')
    return query.paginate(per_page=15, name=name).render(
        'common/tag.html', tag=t, subs=subs, hottest=hottest, newest=newest)


@bp.route('/tools')
def tools():
    return render_template('dev.html')


@bp.route('/interflow')
def interflow():
    return render_template('common/interflow.html')
