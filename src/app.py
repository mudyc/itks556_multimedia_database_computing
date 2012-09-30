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

import rdf

import random, json
from StringIO import StringIO

class Vocab:
    Img = 'http://vocab/Image'
    impression_ = 'http://vocab/impression/'
    color_ = 'http://vocab/color'
    answer = 'http://vocab/answer'
    yes = 'http://vocab/correct#yes'
    no = 'http://vocab/correct#no'

def ctx(req):
    ret = req.script_name
    if ret == '/': ret = ''
    return ret

PALETTE = []

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
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/imageloader.js"></script>
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

@route('/query.html')
def query():
    return '''<!DOCTYPE html>
<html>
  <head>
    <title>Title of the document</title>
    <meta name="context" content="%(ctx)s" />
    <link rel="stylesheet" type="text/css" href="%(ctx)s/css/style.css" /> 
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/jquery.min.js"></script>
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/jquery.cookie.js"></script>
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/imageloader.js"></script>
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/query.js"></script>
  </head>
  <body>
    <div id="container">
      <h1>Psychometric impression query</h1>
      <p>You will be shown five random images. </p>
      <p>Then you are being asked if given impression matches to the image. <p>
      <p>Click yes or no.
      </p>

      <noscript>Unfortunately your javascript is not activated. Please activate it to continue.</noscript>
      <div id="content">
        <a id="continue" href="#">Continue</a>
      </div>
    </div>
  </body>
</html>'''%{'ctx':ctx(request) }

@route('/thanks.html')
def thanks():
    return '''<!DOCTYPE html>
<html>
  <head>
    <title>Title of the document</title>
    <meta name="context" content="%(ctx)s" />
    <link rel="stylesheet" type="text/css" href="%(ctx)s/css/style.css" /> 
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/jquery.min.js"></script>
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/jquery.cookie.js"></script>
  </head>
  <body>
    <div id="container">
      <h1>Thank you for participating to the test</h1>
      <p>All tests are now done, thank you.</p>
      <p>Images seen in the page have been from flicker.com from their responsible authors.<p>
      </p>
      <a href="%(ctx)s/munsell.html">Munsell colors</a>
      <noscript>Unfortunately your javascript is not activated. Please activate it to continue.</noscript>
    </div>
  </body>
</html>'''%{'ctx':ctx(request) }

@route('/munsell.html')
def munsell():
    return '''<!DOCTYPE html>
<html>
  <head>
    <title>Title of the document</title>
    <meta name="context" content="%(ctx)s" />
    <link rel="stylesheet" type="text/css" href="%(ctx)s/css/style.css" /> 
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/jquery.min.js"></script>
    <script type="text/javascript" charset="utf-8" src="%(ctx)s/js/jquery.cookie.js"></script>
  </head>
  <body>
    <div id="container">
      <h1>Here is munsell color tables</h1>
      <p>These tables show the used colors in the psychometric color table.
      </p>

      %(munsell)s
      <noscript>Unfortunately your javascript is not activated. Please activate it to continue.</noscript>
    </div>
  </body>
</html>'''%{'ctx':ctx(request), 'munsell':getmunsell() }

def getmunsell():
    f = open('src/real_sRGB.csv')
    lines = f.readlines()
    f.close()

    def rgb(lines, H,C,V):
        C,V = str(C), str(V)
        for line in lines:
            parts = line[:-1].split(',')
            h,c,v,r,g,b = parts[1], parts[2], parts[3], parts[16], parts[17],parts[18]

            if H==h and C==c and V==v:
                return (r,g,b)
        return (255,255,255)
                        
    ret = """<table>
      <caption>Munsell colors in rgb</caption>
      <thead>
        <tr>
          <th>Chroma</th>
          <th>V</th>"""
    for h in 'R,RP,P,PB,B,BG,G,GY,Y,YR'.split(','):
        #for H in '10,7.5,5,2.5'.split(','):
        for H in '7.5'.split(','):
            ret += """<th>%s</th>""" % (H+h)
    ret += """
        </tr>
      </thead>
      <tbody>"""
    count = 0
    for c in range(2,10):
        for v in range(2, 27, 4):
            ret += '<tr>'
            ret += '<th>'+str(c)+'</th>'
            ret += '<td>'+str(v)+'</td>'
            for h in 'R,RP,P,PB,B,BG,G,GY,Y,YR'.split(','):
                #for H in '10,7.5,5,2.5'.split(','):
                for H in '7.5'.split(','):
                    colors = rgb(lines, H+h, c, v)
                    if colors != (255,255,255):
                        count +=1
                    ret += '<td style="height:20px;width:40px;background-color:rgb(%s,%s,%s);" />' % colors
            ret += '</tr>'
            
    ret += '''
     </tbody>
     </table>'''
    logging.info("count "+str(count))
    return ret


def getcolors():
    ret = ''
    def dec(r,g,b):
        return r*256 + g*256 + b
    def item(r,g,b, idx):
        ret = ''
        ret += '<li>'
        ret += '<a style="width: 90px; height:20px; background: rgb(%s,%s,%s);">' % (r,g,b)
        ret += '</a>'
        ret += impression_for_color(Vocab.color_ + str(idx))
        ret += '</li>'
        return ret
    


# REST API
# ========

@route('/rest/impression/<impression>', method='POST')
def img_impression(impression):
    logging.info('give impression: '+impression)
    imgdata = simplejson.JSONDecoder().decode(request.body.getvalue())
    logging.info(imgdata)
    url = "http://farm%(farm)s.staticflickr.com/%(server)s/%(id)s_%(secret)s_z.jpg" % imgdata 

    mark_img_histogram(url, imgdata)

    for color in rdf.fetch_1xa('data.triple', url):
        if color.startswith(Vocab.color_):
            count = rdf.fetch_11x('data.triple', url, color)[0]
            rdf.add('data.triple', color, Vocab.impression_+impression, count)
    
    return 'ok'

@route('/rest/top/impression', method='POST')
def top_impression():
    imgdata = simplejson.JSONDecoder().decode(request.body.getvalue())
    logging.info(imgdata)
    url = "http://farm%(farm)s.staticflickr.com/%(server)s/%(id)s_%(secret)s_z.jpg" % imgdata

    mark_img_histogram(url, imgdata)

    impressions = {}
    maxcc = (0,0)
    for color in rdf.fetch_1xa('data.triple', url):
        if color.startswith(Vocab.color_):
            count = rdf.fetch_11x('data.triple', url, color)[0]
            if maxcc[1] < int(count):
                maxcc = (color, count)
    for impression in rdf.fetch_1xa('data.triple', maxcc[0]): 
        for impcount in rdf.fetch_11x('data.triple', maxcc[0], impression):
            if impression not in impressions:
                impressions[impression] = long(impcount)
            else:
                impressions[impression] += long(impcount)

    maximp = (0,0)
    for imp, count in impressions.items():
        if maximp[1] < count:
            maximp = (imp, count)
    logging.info(maximp)
    return maximp[0][len(Vocab.impression_):]

@route('/rest/match/<answer>', method='POST')
def impression_answer(answer):
    imgdata = simplejson.JSONDecoder().decode(request.body.getvalue())
    logging.info(imgdata)
    url = "http://farm%(farm)s.staticflickr.com/%(server)s/%(id)s_%(secret)s_z.jpg" % imgdata

    if answer == 'yes':
        rdf.add('data.triple', url, Vocab.answer, Vocab.yes)
    else:
        rdf.add('data.triple', url, Vocab.answer, Vocab.no)

def mark_img_histogram(url, imgdata):
    if not rdf.has('data.triple', url, rdf.type, Vocab.Img):
        rdf.add('data.triple', url, rdf.type, Vocab.Img)
        color_histogram = compute_img(url, imgdata)
        for count, color in color_histogram:
            rdf.add('data.triple', url, Vocab.color_ + str(color), str(count))

def impression_for_color(color):
    impressions = {}
    for impression in rdf.fetch_1xa('data.triple', color): 
        for impcount in rdf.fetch_11x('data.triple', color, impression):
            if impression not in impressions:
                impressions[impression] = long(impcount)
            else:
                impressions[impression] += long(impcount)

    maximp = (Vocab.impression_,0)
    for imp, count in impressions.items():
        if maximp[1] < count:
            maximp = (imp, count)
    logging.info(maximp)
    return maximp[0][len(Vocab.impression_):]

def getMunsellPalette():
    f = open('src/real_sRGB.csv')
    lines = f.readlines()
    f.close()

    def rgb(lines, H,C,V):
        C,V = str(C), str(V)
        for line in lines:
            parts = line[:-1].split(',')
            h,c,v,r,g,b = parts[1], parts[2], parts[3], parts[16], parts[17],parts[18]

            if H==h and C==c and V==v:
                return (int(r),int(g),int(b))
        return (255,255,255)

    ret = []
    for i in [0, 64, 128,192,255]:
        ret.extend([i,i,i])
    for c in range(2,10):
        for v in range(2, 27, 4):
            for h in 'R,RP,P,PB,B,BG,G,GY,Y,YR'.split(','):
                r,g,b = rgb(lines, '7.5'+h, c, v)
                if r != 255 and g != 255 and b != 255:
                    ret.extend([r,g,b])
    return ret

def compute_img(url, data):
    import urllib2 as urllib
    from PIL import Image
    from cStringIO import StringIO

    img_file = urllib.urlopen(url)
    im = StringIO(img_file.read())
    im = Image.open(im)
    img_file.close()

    global PALETTE
    if PALETTE == []:
        PALETTE = getMunsellPalette()

    while len(PALETTE) < 256*3:
        PALETTE.extend([0,0,0])

    # a palette image to use for quant
    pimage = Image.new("P", (1, 1), 0)
    pimage.putpalette(PALETTE)

    # quantize it using our palette image
    imagep = im.quantize(palette=pimage)
    #imagep.save('/tmp/cga.png')
    return imagep.getcolors()

@route('/js/<file:path>')
def static_js(file):
    return static_file(file, root='./src/js')

@route('/img/<file:path>')
def static_img(file):
    #logging.info('wd: '+os.getcwd())
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
