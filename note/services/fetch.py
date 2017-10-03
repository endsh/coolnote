# coding: utf-8
import HTMLParser
from flask.ext.likedown import get_markdown
from html2text import html2text
from note.base import um
from note.models import Question
from note.extractor import url2article

html_parser = HTMLParser.HTMLParser()
markdown = get_markdown()


def content2text(content):
    c = html2text(content)
    res = []
    labels = ['描述', '题目描述', '输入', '输出', '样例输入', '提示', '样例输出', '来源', '上传者']
    bad = False
    pre = False
    start = False
    for line in c.splitlines():
        s = line.replace('#', '')
        s = s.strip()
        if not s:
            continue
        if s in labels:
            if s in ['描述', '题目描述']:
                start = True
                if s == '题目描述':
                    s = '描述'
            if not start:
                continue
            if s in ['来源', '上传者']:
                bad = True
            else:
                bad = False
                res.append('')

                if s in ['样例输入', '样例输出']:
                    pre = True
                else:
                    pre = False

                res.append('### ' + s)
                res.append('')
            continue
        elif not bad:
            if not start:
                continue
            if pre:
                res.append('    ' + s)
            else:
                res.append(s)

    if len(res) < 2:
        return ''

    if not res[-2] == '### 提示':
        res.append('')
    else:
        res = res[:-2]

    return html_parser.unescape('\n'.join(res))


def down(url, title, content, user, handle=lambda x: x):
    art = url2article(
        url,
        title_selector=title,
        content_selector=content)

    question = Question.objects(source=url).first()
    if not question:
        question = Question(user=user.id)
    question.source = url
    question.title = handle(art['title'])
    question.markdown = content2text(art['content'])
    if not question.markdown:
        print 'error: ', url
        return
    question.content = markdown.convert(question.markdown)
    question.create_desc()
    question.create()


def run():
    user = um.models.User.objects(id=100000).first()
    # tpl = 'http://acm.hnust.edu.cn/JudgeOnline/problem.php?id='
    # for i in range(1001, 1823):
    #     down(tpl + str(i), '#main h2', '#main', user, lambda x: x.strip()[5:])

    tpl = 'http://acm.nyist.net/JudgeOnline/problem.php?pid='
    for i in range(1, 1329):
        down(tpl + str(i), 'div.problem-display h2', 'dl.problem-display', user)
