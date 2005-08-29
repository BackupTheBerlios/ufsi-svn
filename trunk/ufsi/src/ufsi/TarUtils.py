import ufsi

import tarfile

def getMembers(tarFilePath):
    tf=tarFilePath.getFile()
    tf.open('r')
    tar=tarfile.TarFile('','r',tf)
    ms=tar.getmembers()
    tar.close()
    tf.close()
    return ms
    

def getTarInfo(tarFilePath,tarPath):
    tf=tarFilePath.getFile()
    tf.open('r')
    tar=tarfile.TarFile('','r',tf)
    try:
        ti=tar.getmember(tarPath)
    except KeyError,e:
        raise ufsi.PathNotFoundError('"%s" in "%s" not found'
                                     %(tarFilePath,tarPath))
    tar.close()
    tf.close()
    return ti


def tarInfoToDict(ti):
    d={}
    d['size']=ti.size
    d['modificationTime']=ti.mtime
    d['permissions']=ti.mode
    d['userId']=ti.uid
    d['groupId']=ti.gid
    return d

