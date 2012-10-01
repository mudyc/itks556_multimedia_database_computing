# simple flat file rdf database

import logging, os, time

_rdf = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
_xsd = 'http://www.w3.org/2001/XMLSchema#'
type = _rdf + 'type'
lit_float = _xsd + 'float'


def aqcuire_lock(f):
    """http://rcrowley.org/2010/01/06/things-unix-can-do-atomically.html"""
    #logging.info("aqcuire")
    t = 0.002
    while True:
        try:
            os.link(f, f+'.lock')
            #logging.info("aqcuired")
            break
        except:
            time.sleep(t)
            if t < 1.0:
                t *= 2

def release_lock(f):
    os.unlink(f+'.lock')

def rm(file_, subj, pred, obj):
    aqcuire_lock(file_)

    f = open(file_, 'r')
    lines = f.readlines()
    f.close()

    test = subj +' '+pred+' '+obj+'\n'
    lines.remove(test)

    new = os.tempnam(os.getcwd())
    f = open(new, 'w')
    f.writelines(lines)
    f.close()
    os.rename(new, file_)
    
    release_lock(file_)

def add(file_, subj, pred, obj):
    aqcuire_lock(file_)

    f = open(file_, 'r')
    lines = f.readlines()
    f.close()

    test = subj +' '+pred+' '+obj+'\n'
    lines.append(test)
    lines.sort()
    #logging.info(lines)

    new = os.tempnam(os.getcwd())
    #logging.info(new)
    f = open(new, 'w')
    f.writelines(lines)
    f.close()
    os.rename(new, file_)
    
    release_lock(file_)

def has(file_, subj, pred, obj):
    f = open(file_, 'r')
    lines = f.readlines()
    f.close()
    test = subj +' '+pred+' '+obj+'\n'
    for line in lines:
        if line == test:
            return True
    return False

def fetch_1xa(file_, subj):
    f = open(file_, 'r')
    lines = f.readlines()
    f.close()
    ret = []
    test = subj+' '
    for line in lines:
        if line.startswith(test):
            ret.append(line.split(' ')[1])
    return ret

def fetch_11x(file_, subj, pred):
    f = open(file_, 'r')
    lines = f.readlines()
    f.close()
    ret = []
    test = subj+' '+pred+' '
    for line in lines:
        if line.startswith(test):
            ret.append(line[:-1].split(' ')[2])
    return ret

