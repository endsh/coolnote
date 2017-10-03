# coding: utf-8
from chiki import json_success, json_error
from chiki.contrib.common import Item, UserImage
from datetime import datetime
from flask import Blueprint, render_template, request, url_for
from flask.ext.login import login_required, current_user
from flask.ext.likedown import get_markdown
from note.forms import QuestionForm, EditAnswerForm
from note.models import Tag, Question, Answer

bp = Blueprint('home', __name__)
TAGS = '基础算法|数据结构|图论算法|动态规划|搜索算法|数学|计算几何学'

markdown = get_markdown()


def get_tags():
    tags = Item.list('editor_tags', TAGS, coerce=str)
    data = []
    for tag in tags:
        subs = []
        t = Tag.objects(name=tag).first()
        if t:
            subs = list(Tag.objects(parents=t).order_by('-weight').limit(30))
        data.append(dict(tag=tag, subs=subs))
    return data


@bp.route('/questions/new')
@login_required
def new_question():
    form = QuestionForm()
    return render_template(
        'home/new-question.html', form=form, tags=get_tags())


@bp.route('/questions/<id>/edit')
@login_required
def edit_question(id):
    question = Question.objects(id=id, user=current_user.id).get_or_404()
    form = QuestionForm(obj=question)
    return render_template(
        'home/edit-question.html', form=form, question=question,
        tags=get_tags())


@bp.route('/questions/post', methods=['POST'])
@login_required
def post_question():
    id = request.form.get('id')
    title = request.form.get('title')
    content = request.form.get('content')
    tags = request.form.getlist('tags[]', int)
    tags = list(Tag.objects(id__in=tags).limit(5))
    if not title:
        return json_error(msg='标题不能为空！')
    if len(content) < 20:
        return json_error(msg='正文不能少于20个字符！')
    if not tags:
        return json_error(msg='标签不能为空！')
    if id:
        question = Question.objects(id=id, user=current_user.id).first()
        if not question:
            return json_error(msg='问题不存在！')
    else:
        if Question.objects(title=title, user=current_user.id).count() > 0:
            return json_error(msg='你已提交过相同的问题！')
        question = Question(user=current_user.id)
        question.create()
    question.title = title
    question.markdown = content
    question.content = markdown.convert(content)
    question.modified = datetime.now()
    question.create_desc()
    question.tags = tags
    question.save()
    return json_success(next=url_for('common.question', id=question.id))


@bp.route('/questions/<qid>/answers/<id>/edit')
@login_required
def edit_answer(qid, id):
    answer = Answer.objects(id=id, user=current_user.id).get_or_404()
    form = EditAnswerForm(data=dict(
        title=answer.question.title, markdown=answer.markdown))
    return render_template(
        'home/edit-answer.html', form=form, answer=answer)


@bp.route('/questions/<qid>/answer', methods=['POST'])
@login_required
def post_answer(qid):
    id = request.form.get('id')
    content = request.form.get('content')
    if len(content) < 10:
        return json_error(msg='正文不能少于10个字符！')

    question = Question.objects(id=qid).first()
    if not question:
        return json_error(msg='问题不存在！')

    if id:
        answer = Answer.objects(id=id).first()
        if not answer:
            return json_error(msg='回答不存在！')
    else:
        query = dict(question=question, markdown=content, user=current_user.id)
        if Answer.objects(**query).count() > 0:
            return json_error(msg='你已提交过相同的回答！')
        question.update(inc__answers=1, modified=datetime.now())
        answer = Answer(question=question, user=current_user.id)
        answer.create()
    answer.markdown = content
    answer.content = markdown.convert(content)
    answer.modified = datetime.now()
    answer.save()
    return json_success(next=url_for('common.question', id=question.id))


@bp.route('/images/upload', methods=['POST'])
@login_required
def upload_image():
    proxy = request.files.get('file')
    image = UserImage(user=current_user.id, image=proxy)
    if image.image:
        image.save()
        return json_success(url=image.image.link)
    return json_error(msg='上传错误')
