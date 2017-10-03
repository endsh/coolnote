# coding: utf-8
from chiki.contrib.common import Item
from datetime import datetime
from note.base import db, um
from note.extractor.html import html2doc

db.abstract(um.models.User)


@um.add_model
class User(um.models.User):
    """ 用户模型 """

    @property
    def answers(self):
        return Answer.objects(user=self).count()

    @property
    def questions(self):
        return Question.objects(user=self).count()


class Tag(db.Document):
    """ 标签 """

    id = db.IntField(primary_key=True, verbose_name='ID')
    user = db.ReferenceField('User', verbose_name='用户')
    name = db.StringField(verbose_name='名称')
    desc = db.StringField(verbose_name='简介')
    icon = db.XImageField(verbose_name='图标')
    parents = db.ListField(db.ReferenceField('Tag'), verbose_name='父标签')
    weight = db.IntField(default=0, verbose_name='权重')
    modified = db.DateTimeField(default=datetime.now, verbose_name='修改时间')
    created = db.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __unicode__(self):
        return self.name

    def create(self):
        """ 创建渠道 """
        if not self.id:
            self.id = Item.inc('tag_index', 10000)
            self.save()
        return self.id


class Question(db.Document):
    """ 问题 """

    id = db.IntField(primary_key=True, verbose_name='ID')
    user = db.ReferenceField('User', verbose_name='用户')
    title = db.StringField(verbose_name='标题')
    desc = db.StringField(verbose_name='简介')
    markdown = db.StringField(verbose_name='MarkDown')
    content = db.StringField(verbose_name='内容')
    tags = db.ListField(db.ReferenceField('Tag'), verbose_name='标签')
    file = db.XFileField(verbose_name='附件')
    source = db.StringField(verbose_name='来源')
    answer = db.ReferenceField('Answer', verbose_name='回答')
    answers = db.IntField(default=0, verbose_name='回答数')
    views = db.IntField(default=0, verbose_name='浏览数')
    weight = db.IntField(default=0, verbose_name='权重')
    week_weight = db.IntField(default=0, verbose_name='本周热门')
    modified = db.DateTimeField(default=datetime.now, verbose_name='修改时间')
    created = db.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __unicode__(self):
        return '%d - %s' % (self.id, self.title)

    def create(self):
        """ 创建渠道 """
        if not self.id:
            self.id = Item.inc('question_index', 10000)
            self.save()
        return self.id

    def create_desc(self):
        children = html2doc(self.content).getchildren()
        lines = [node.text_content() for node in children]
        for line in lines:
            if len(line) > 10:
                self.desc = line
                break


class Answer(db.Document):
    """ 回答 """

    id = db.IntField(primary_key=True, verbose_name='名称')
    user = db.ReferenceField('User', verbose_name='用户')
    question = db.ReferenceField('Question', verbose_name='问题')
    markdown = db.StringField(verbose_name='MarkDown')
    content = db.StringField(verbose_name='内容')
    weight = db.IntField(default=0, verbose_name='权重')
    modified = db.DateTimeField(default=datetime.now, verbose_name='修改时间')
    created = db.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __unicode__(self):
        return str(self.id)

    def create(self):
        """ 创建渠道 """
        if not self.id:
            self.id = Item.inc('answer_index', 10000)
            self.save()
        return self.id
