# coding: utf-8
import os

ROOT = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
LOG_FOLDER = os.path.join(ROOT, 'logs')
STATIC_FOLDER = os.path.join(ROOT, 'media/api/dist')

LOGGING = {
    'SMTP': {
        'HOST': 'smtp.mxhichina.com',
        'TOADDRS': ['438985635@qq.com'],
        'SUBJECT': u'note api 出错了 :-(',
        'USER': 'pms@haoku.net',
        'PASSWORD': 'xiaoku8.com',
    },
    'FILE': {
        'PATH': os.path.join(LOG_FOLDER, 'api.log'),
        'MAX_BYTES': 1024 * 1024 * 10,
        'BACKUP_COUNT': 5,
    }
}
