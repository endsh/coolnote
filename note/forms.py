# coding: utf-8
from chiki.forms import Form
from flask.ext.likedown import LikedownField
from wtforms.fields import TextField


class QuestionForm(Form):
    title = TextField("标题")
    markdown = LikedownField("正文", show_modals=False)


class AnswerForm(Form):
    markdown = LikedownField("回答", show_modals=False)


class EditAnswerForm(Form):
    title = TextField("标题")
    markdown = LikedownField("回答", show_modals=False)
