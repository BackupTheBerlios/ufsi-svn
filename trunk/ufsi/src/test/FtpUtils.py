"""
Util functions for testing Ftp implementations.

"""

import ftplib
import re


def size(ftp,d,f):
    ftp.cwd(d)
    s=ftp.size(f)
    if s==None:
        (sock,s)=ftp.ntransfercmd('RETR '+f)
        sock.close()
        ftp.abort()
    return s


def createFile(ftp,d,f,c):
    ftp.cwd(d)
    sock=ftp.transfercmd('STOR '+f)
    sock.sendall(c)
    sock.close()
    ftp.voidresp()

def isFile(ftp,d,f):
    fs=getDirList(ftp,d)
    for i in fs:
        if i['fileName']==f:
            return True
    return False

def readFile(ftp,d,f):
    ftp.cwd(d)
    sock=ftp.transfercmd('RETR '+f)
    f=sock.makefile('r')
    s=f.read()
    f.close()
    sock.close()
    ftp.voidresp()

    return s

def deleteFile(ftp,d,f):
    ftp.cwd(d)
    if isFile(ftp,d,f):
        ftp.delete(f)
    


def createDir(ftp,d):
    try:
        ftp.cwd(d)
    except ftplib.error_perm,e:
        if str(e).startswith('550'):
            ftp.mkd(d)
        else:
            raise e

def getDirList(ftp,d):
    ftp.cwd(d)
    sock=ftp.transfercmd('LIST')
    f=sock.makefile('r')
    s=f.read()
    f.close()
    sock.close()
    ftp.voidresp()

    unixListItem='(?P<permissions>[a-z\\-]+)\s+'\
                 '(?P<hardLinks>[0-9]+)\s+'\
                 '(?P<user>[A-Za-z\\-]+)\s+'\
                 '(?P<group>[A-Za-z\\-]+)\s+'\
                 '(?P<size>[0-9]+)\s+'\
                 '(?P<date>[A-Za-z]+\s+[0-9]+\s+[0-9:]+)\s+'\
                 '(?P<fileName>.+)'
    unixListItemRe=re.compile(unixListItem)
    items=[]
    for l in s.splitlines():
        mo=unixListItemRe.match(l)
        assert mo is not None
        d=mo.groupdict()
        if d['fileName'] in ('.','..'):
            continue
        items.append(d)
        
    return items
