import ufsi


p=ufsi.Path('http://www.google.com.au')

print p.split()

f=p.getFile()

s=f.getStat()


for i in s.keys():
    print "%r: %r, "%(i,s[i])

f.open()
for l in f.readLines():
    print l
f.close()
