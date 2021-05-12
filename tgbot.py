import json
from urllib.request import urlopen
from urllib.parse import quote
import time
import Token


# this python script is a code that controls an echo telegram bot
# request format : https://api.telegram.org/bot<your-bot-token>/<command>

# function for decoding html content to utf-8


def aux_dec2utf8(resp):
    decoded = ''
    for line in resp:
        decoded += line.decode('utf-8')
    return decoded


token = Token.T                                        # define the access token
url = 'https://api.telegram.org/bot{}/'.format(token)  # telegram botAPIurl+ token

cmd = 'getme'

resp = urlopen(url + cmd)
line = aux_dec2utf8(resp)
gtm = json.loads(line)

status = True
while status:

    cmd = 'getupdates'

    resp = urlopen(url + cmd)
    line = aux_dec2utf8(resp)
    upds = json.loads(line)

    nom = len(upds['result'])

    if nom != 0:
        msg = upds['result'][0]['message']
        chid = str(msg['chat']['id'])

        if 'text' in msg:
            txt = quote(msg['text'].encode('utf-8'))

            cmd = 'sendMessage'

            resp = urlopen(url + cmd + '?chat_id={}&text={}'.format(chid, txt))
            line = aux_dec2utf8(resp)
            chck = json.loads(line)

            if chck['ok']:

                uid = upds['result'][0]['update_id']
                cmd = 'getUpdates'
                urlopen(url + cmd + '?offset={}'.format(uid + 1))

        else:

            uid = upds['result'][0]['update_id']
            cmd = 'getUpdates'
            urlopen(url + cmd + '?offset={}'.format(uid + 1))

    print('waiting!')
    time.sleep(5)
