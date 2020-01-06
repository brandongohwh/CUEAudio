import datetime
import os

def port():
    l=[]

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    z=os.getcwd()

    def folwalk(loc,depth):
        fop.write('%s- %s\n'%(depth*2*' ',os.path.basename(loc)))
        ls=[]
        nf=[]
        for fs in os.listdir(loc):
            if os.path.isfile(os.path.join(loc,fs)) and os.path.splitext(os.path.join(loc,fs))[1].lower()=='.wav':
                ls.append(fs)
            elif os.path.isdir(os.path.join(loc,fs)):
                nf.append(fs)
        ls.sort()
        nf.sort()
        for a in ls:
            if not a in l:
                #fop.write('%s- %s (Added: %s)\n'%((depth+1)*2*' ',a,datetime.date.today().strftime("%d-%b-%Y")))
                fop.write('%s- %s\n'%((depth+1)*2*' ',a))
                mop.write('- %s\n'%os.path.join(loc.replace(z,''),a))
            else:
                fop.write('%s- %s\n'%((depth+1)*2*' ',a))
        for b in nf:
            #fop.write('%s- %s\n'%((depth+1)*4*' ',b))
            folwalk(os.path.join(loc,b),depth+1)

    if os.path.exists('filelist.md'):
        fop=open('filelist.md','r')
        l=fop.readlines()
        l=[s.strip('\n').strip().strip('-').strip().split()[0] for s in l if s!='\n']
        print(l)
        fop.close()
        fop=open('filelist.md','w')
    else:
        fop=open('filelist.md','w')
    mop=open('changelog.md','w')

    fop.write('# CUE Audio ')
    mop.write('# CUE Audio: Updated %s\n\n'%datetime.date.today().strftime("%d-%b-%Y"))

    folwalk(os.path.join(os.getcwd(),'Extracted'),0)

    fop.flush()
    fop.close()
    mop.flush()
    mop.close()
