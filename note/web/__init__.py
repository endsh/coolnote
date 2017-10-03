# coding: utf-8
from chiki import register_web, MediaManager, init_uploads
from note.base import db, um, wapi, WebConfig
from . import common, home, tags

media = MediaManager(
    editor=dict(
        js=[
            'js/editor.min.js',
        ],
        jsx=[
            'bower_components/select2/dist/js/select2.full.js',
            'bower_components/select2/dist/js/i18n/zh-CN.js',
            'libs/likedown/js/flowchart-1.4.0.js',
            'libs/raphael.js',
            'bower_components/underscore/underscore-min.js',
            'bower_components/js-sequence-diagrams/build/sequence-diagram-min.js',
            'bower_components/MathJax/MathJax.js',
            'bower_components/MathJax/config/TeX-AMS_HTML.js',
            'libs/likedown/js/likedown-ext.js',
            'dist/js/editor.js',
        ],
    ),
    css=['css/web.min.css'],
    cssx=[
        'libs/bootstrap/css/bootstrap.css',
        'libs/highlight/styles/github.css',
        'bower_components/select2/dist/css/select2.min.css',
        'libs/likedown/css/likedown.css',
        'dist/css/web.css'
    ],
    js=['js/web.min.js'],
    jsx=[
        'bower_components/jquery/dist/jquery.min.js',
        'bower_components/jquery-form/jquery.form.js',
        'bower_components/jquery-tmpl/jquery.tmpl.js',
        'libs/bootstrap/js/bootstrap.min.js',
        'libs/highlight/highlight.pack.js',
        'libs/area.js',
        'dist/js/web.js'
    ],
)


def init_routes(app):
    app.register_blueprint(common.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(tags.bp, url_prefix='/tags')


def init_um(app):
    um.init_app(app)
    um.init_wapis(wapi)
    um.init_web()


@register_web(config=WebConfig)
def init(app):
    db.init_app(app)
    media.init_app(app)
    init_um(app)
    init_routes(app)
    init_uploads(app)
    wapi.init_app(app)
