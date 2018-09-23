import json
import requests
from flask_babel import _
from app import app
import random
from hashlib import md5


def translate(text, source_language, dest_language):
    if 'BD_TRANSLATOR_KEY' not in app.config or \
            not app.config['BD_TRANSLATOR_KEY']:
        return _('ERROR: the translation service is not configed.')
    if 'BD_TRANSLATOR_APPID' not in app.config or \
            not app.config['BD_TRANSLATOR_APPID']:
        return _('ERROR: the translation service is not configed.')

    appid = app.config['BD_TRANSLATOR_APPID']
    secretKey = app.config['BD_TRANSLATOR_KEY']
    salt = random.randint(32768, 65536)

    sign = appid + text + str(salt) + secretKey
    m1 = md5()
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()

    r = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate? '
                     'q={}&from={}&to={}&appid={}&'
                     'salt={}&sign={}'.format(
        text, source_language, dest_language, appid, salt, sign))

    if r.status_code != 200:
        return _('Error: the translation service failed.')

    return json.loads(r.content.decode('utf-8-sig'))['trans_result'][0]['dst']