import ufsi


p=ufsi.Path('/usr/local/lib/python2.4/site-packages')
print 'Path: '+str(p)
print 'Is Dir: '+str(p.isDir())
print 'Path split: '+str(p.split())

print '======================='
print
d=p.getDir()
print 'Dir path: '+str(d.getPath())

print 'Dir list:'
for dlp in d.getDirList():
    print str(dlp)
print 'Dir stat: '+str(d.getStat())

print '======================='
print
fp=p.join('README')
print 'File path: '+str(fp)
print 'Is File: '+str(fp.isFile())
print 'File split: '+str(fp.split())

f=fp.getFile()
print 'File stat: '+str(f.getStat())
print 'File ("%s") contents:'%str(f)
f.open()
print f.read()
f.close()


