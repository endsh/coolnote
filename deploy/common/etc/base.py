# coding: utf-8
import os

ROOT = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

DATA_FOLDER = os.path.join(ROOT, 'data')
ETC_FOLDER = os.path.join(ROOT, 'etc')
LOG_FOLDER = os.path.join(ROOT, 'logs')
RELEASE_STATIC_FOLDER = os.path.join(ROOT, 'media/web/dist')

UPLOADS = dict(
    host='oss-cn-shenzhen.aliyuncs.com',
    access_id='qrJVG3qB7KkfqQGA',
    secret_access_key='QMCG0mpxQhSwGDwsxLMr8rbwqrMEJy',
    link='http://oss.lesscool.cn/%s',
    bucket='lesscool',
    prefix='coolnote/',
    type='oss',
)
