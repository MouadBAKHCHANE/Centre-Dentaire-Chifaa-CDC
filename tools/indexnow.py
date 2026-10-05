# -*- coding: utf-8 -*-
"""Signale toutes les URL du sitemap à IndexNow (Bing, Yandex, Seznam...).
À lancer après un déploiement :  python tools/indexnow.py
La clé est servie à la racine du site : https://www.centredentairechifaa.ma/b3037fa5af3e93f2c3d2a492de534ea2.txt"""
import json, os, re, urllib.request

HOST = 'www.centredentairechifaa.ma'
KEY = 'b3037fa5af3e93f2c3d2a492de534ea2'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urls = re.findall(r'<loc>(.*?)</loc>', open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read())
body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': 'https://%s/%s.txt' % (HOST, KEY), 'urlList': urls}).encode('utf-8')
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body,
                             headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print('IndexNow :', r.status, '-', len(urls), 'URL envoyées')
except urllib.error.HTTPError as e:
    print('IndexNow : erreur', e.code, e.read()[:200])
