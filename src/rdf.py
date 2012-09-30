# simple flat file rdf database

import logging

_rdf = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
_xsd = 'http://www.w3.org/2001/XMLSchema#'
type = _rdf + 'type'
lit_float = _xsd + 'float'


def aqcuire_lock(f):
    """http://rcrowley.org/2010/01/06/things-unix-can-do-atomically.html"""
    pass
def release_lock():
    pass

def rm(file_, subj, pred, obj):
    aqcuire_lock(file_)

    f = open(file_, 'r')
    lines = f.readlines()
    f.close()

    test = subj +' '+pred+' '+obj+'\n'
    lines.remove(test)

    f = open(file_, 'w')
    f.writelines(lines)
    f.close()
    
    release_lock()

def add(file_, subj, pred, obj):
    aqcuire_lock(file_)

    f = open(file_, 'r')
    lines = f.readlines()
    f.close()

    test = subj +' '+pred+' '+obj+'\n'
    lines.append(test)
    lines.sort()
    #logging.info(lines)

    f = open(file_, 'w')
    f.writelines(lines)
    f.close()
    
    release_lock()

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

