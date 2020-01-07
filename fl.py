import datetime
import os
import sys

def folwalk(loc, depth):
    if os.path.basename(loc) in val2:
        fop.write('%s- %s: %s\n' % (depth*2*' ', os.path.basename(loc),desc2[val2.index(os.path.basename(loc))]))
    else:
        fop.write('%s- %s\n' % (depth*2*' ', os.path.basename(loc)))
    ls = []
    nf = []
    for fs in os.listdir(loc):
        if os.path.isfile(os.path.join(loc, fs)) and os.path.splitext(os.path.join(loc, fs))[1].lower() == '.wav':
            ls.append(fs)
        elif os.path.isdir(os.path.join(loc, fs)):
            nf.append(fs)
    ls.sort()
    nf.sort()
    for a in ls:
        if not a in l:
            if 'bgm' in loc.lower():
                if int(os.path.splitext(a)[0]) in val1:
                    fop.write('%s- %s: %s\n' % ((depth+1)*2*' ', a,
                                                desc1[val1.index(int(os.path.splitext(a)[0]))]))
                    mop.write('- %s: %s\n' % (os.path.join(loc.replace(z, ''), a), desc1[val1.index(int(os.path.splitext(a)[0]))]))
                elif int(os.path.splitext(a)[0])-100 in val1:
                    fop.write('%s- %s: %s (Instrumental)\n' % ((depth+1)*2*' ', a,
                                                desc1[val1.index(int(os.path.splitext(a)[0])-100)]))
                    mop.write('- %s: %s\n' % (os.path.join(loc.replace(z, ''), a), desc1[val1.index(int(os.path.splitext(a)[0])-100)]))
                else:
                    fop.write('%s- %s\n' % ((depth+1)*2*' ', a))
                    mop.write('- %s\n' %
                              os.path.join(loc.replace(z, ''), a))
            else:
                fop.write('%s- %s\n' % ((depth+1)*2*' ', a))
                mop.write('- %s\n' % os.path.join(loc.replace(z, ''), a))
        else:
            if 'bgm' in loc.lower():
                if int(os.path.splitext(a)[0]) in val1:
                    fop.write('%s- %s: %s\n' % ((depth+1)*2*' ', a,
                                                desc1[val1.index(int(os.path.splitext(a)[0]))]))
                elif int(os.path.splitext(a)[0])-100 in val1:
                    fop.write('%s- %s: %s (Instrumental)\n' % ((depth+1)*2*' ', a,
                                                desc1[val1.index(int(os.path.splitext(a)[0])-100)]))
                else:
                    fop.write('%s- %s\n' % ((depth+1)*2*' ', a))
            else:
                fop.write('%s- %s\n' % ((depth+1)*2*' ', a))

    for b in nf:
        # fop.write('%s- %s\n'%((depth+1)*4*' ',b))
        folwalk(os.path.join(loc, b), depth+1)

f1 = open('pyfile'+os.path.sep+'musicval.txt', 'r',encoding='utf-8')
r1 = f1.readlines()
val1 = []
desc1 = []
for i in r1:
    val1.append(int(i.split()[0]))
    desc1.append(' '.join(i.strip('\n').split()[1:]))

f2 = open('pyfile'+os.path.sep+'folname.txt', 'r',encoding='utf-8')
r2 = f2.readlines()
val2 = []
desc2 = []
for i in r2:
    val2.append(i.split()[0])
    desc2.append(' '.join(i.strip('\n').split()[1:]))


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
z=os.getcwd()

if os.path.exists(os.path.join(dname,'filelist.md')):
    fop = open('filelist.md', 'r',encoding='utf-8')
    l = fop.readlines()
    l = [s.strip('\n').strip().strip('-').strip().split()[0].split(':')[0] for s in l if s != '\n']
    fop.close()
    fop = open('filelist.md', 'w',encoding='utf-8')
else:
    fop = open('filelist.md', 'w',encoding='utf-8')
    l=[]
mop = open('changelog.md', 'w',encoding='utf-8')

fop.write('# CUE Audio ')
mop.write('# CUE Audio: Updated %s\n\n' % datetime.date.today().strftime("%d-%b-%Y"))

folwalk(os.path.join(os.getcwd(), 'Extracted'), 0)

fop.flush()
fop.close()
mop.flush()
mop.close()

