import datetime
import os
import sys
import csv

def port():
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
        ''' #START OF mute file output
        for a in ls:
            if not a in l:
                if 'bgm' in loc.lower():
                    if int(os.path.splitext(a)[0].split('(')[0]) in val1:
                        fop.write('%s- %s: %s\n' % ((depth+1)*2*' ', a,
                                                    desc1[val1.index(int(os.path.splitext(a)[0]))]))
                        mop.write('- %s: %s\n' % (os.path.join(loc.replace(z, ''), a), desc1[val1.index(int(os.path.splitext(a)[0]))]))
                    elif int(os.path.splitext(a)[0].split('(')[0])-100 in val1:
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
                    if int(os.path.splitext(a)[0].split('(')[0]) in val1:
                        fop.write('%s- %s: %s\n' % ((depth+1)*2*' ', a,
                                                    desc1[val1.index(int(os.path.splitext(a)[0]))]))
                    elif int(os.path.splitext(a)[0].split('(')[0])-100 in val1:
                        fop.write('%s- %s: %s (Instrumental)\n' % ((depth+1)*2*' ', a,
                                                    desc1[val1.index(int(os.path.splitext(a)[0])-100)]))
                    else:
                        fop.write('%s- %s\n' % ((depth+1)*2*' ', a))
                else:
                    fop.write('%s- %s\n' % ((depth+1)*2*' ', a))
        ''' #END OF mute file output
        for b in nf:
            # fop.write('%s- %s\n'%((depth+1)*4*' ',b))
            folwalk(os.path.join(loc, b), depth+1)

    f1 = open('pyfile'+os.path.sep+'musicval.csv', 'r',encoding='utf-8')
    fr=csv.reader(f1)
    val1 = []
    desc1 = []
    for i in fr:
        if not i[0].isdigit():
            continue
        val1.append(int(i[0]))
        desc1.append(i[1])
    
    #Pending CSV conversion
    f2 = open('pyfile'+os.path.sep+'folname.csv', 'r',encoding='utf-8')
    fr2=csv.reader(f2)
    val2 = []
    desc2 = []
    for i in fr2:
        val2.append(i[0])
        desc2.append(i[1])

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

if __name__ == '__main__':
    port()