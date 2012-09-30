# -*- coding: utf-8
import sys, os,	os.path
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))) 
import random, string
from bottle import route, run, static_file, debug, request
import logging
import simplejson

logging.basicConfig(level=logging.DEBUG)
logging.info('Started')
debug(mode=True)



import random, json
from StringIO import StringIO

class Vocab:
    Client = 'http://vocabulary/clientId'
    game = 'http://vocabulary/game'
    gameId = 'http://vocabulary/gameId'
    currentLevel = 'http://vocabulary/level'


def ctx(req):
    ret = req.script_name
    if ret == '/': ret = ''
    return ret

@route('/')
@route('/index.html')
def index():
    return '''<!DOCTYPE html>
<html>
  <head>
    <title>Title of the document</title>
    <meta name="context" content="%(ctx)s" />
    <link rel="stylesheet" type="text/css" href="%(ctx)s/css/style.css" /> 
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/jquery.min.js"></script>
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/jquery.cookie.js"></script>
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/script.js"></script>
  </head>
  <body>
    <div id="container">
      <h1>Psychometric color test</h1>
      <p>Click one or more floating impressions that describe the image.
         There are around 20 images in the query.
      </p>    
      <noscript>Unfortunately your javascript is not activated. Please activate it to continue.</noscript>
      <div id="content"/>
    </div>
  </body>
</html>'''%{'ctx':ctx(request) }


# REST API
# ========

@route('/rest/impression/<impression>', method='POST')
def img_impression(impression):
    imgdata = simplejson.JSONDecoder().decode(request.body.getvalue())
    logging.info(imgdata)
    url = "http://farm%(farm)s.staticflickr.com/%(server)s/%(id)s_%(secret)s_z.jpg" % imgdata 
    compute_img(url, imgdata)

    #rdf.add('data.triple', clientid, rdf.type, Vocab.Client)
    return 'ok'

def compute_img(url, data):
    import urllib2 as urllib
    from PIL import Image
    from cStringIO import StringIO

    img_file = urllib.urlopen(url)
    im = StringIO(img_file.read())
    im = Image.open(im)
    img_file.close()

    PALETTE = [ 0,   0,   0]
    for i in [128,192,255]:
        PALETTE.extend([i,i,i])
        PALETTE.extend([i,0,0])
        PALETTE.extend([i,i,0])
        PALETTE.extend([0,i,0])
        PALETTE.extend([0,i,i])
        PALETTE.extend([0,0,i])

    while len(PALETTE) < 256*3:
        PALETTE.extend([0,0,0])

    # a palette image to use for quant
    pimage = Image.new("P", (1, 1), 0)
    pimage.putpalette(PALETTE)

    # quantize it using our palette image
    imagep = im.quantize(palette=pimage)
    imagep.save('/tmp/cga.png')

    logging.info(imagep.getcolors())
    return

@route('/js/<file:path>')
def static_js(file):
    return static_file(file, root='./src/js')

@route('/img/<file:path>')
def static_img(file):
    logging.info('wd: '+os.getcwd())
    return static_file(file, root='./src/img')

@route('/snd/<file:path>')
def static_snd(file):
    return static_file(file, root='./src/snd')

@route('/css/<file:path>')
def static_css(file):
    return static_file(file, root='./src/css')

@route('/favicon.ico')
def icon():
    
    return static_img('favicon.ico')


if __name__ == '__main__':
    run(host='localhost', port=8080, reloader=True)
