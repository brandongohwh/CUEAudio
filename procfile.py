import pyfile.fileenum as fie
import pyfile.folenum as foe
import os
import fl

#Files: Names of music
f=open('pullMaster'+os.path.sep+'MonoBehaviour'+os.path.sep+'HousingMusicMaster.txt','r',encoding="utf-8")
h=f.readlines()
for i in range(len(h)):
    if 'int id' in h[i]:
        fie.addpair(int(h[i].split('=')[1]),h[i+1].split('=')[1].strip().strip('"'))

#Folder: Main Chapter (メインストーリー)
f=open('pullMaster'+os.path.sep+'MonoBehaviour'+os.path.sep+'StoryMainChapterMaster.txt','r',encoding="utf-8")
h=f.readlines()
for i in range(len(h)):
    if 'int id' in h[i]:
        foe.addpair("Main_{0:0=2d}_{1:0=2d}".format(int(h[i].split('=')[1]),int(h[i+1].split('=')[1])),h[i+2].split('=')[1].strip().strip('"'))

#Folder: Main Chapter (メインストーリー) - Subchapter (サブストーリー)
f=open('pullMaster'+os.path.sep+'MonoBehaviour'+os.path.sep+'StoryMainMaster.txt','r',encoding="utf-8")
h=f.readlines()
for i in range(len(h)):
    if 'int id' in h[i]:
        foe.addpair("Main_{0:0=2d}_{1:0=2d}_{2:0=2d}".format(int(h[i].split('=')[1]),int(h[i+1].split('=')[1]),int(h[i+2].split('=')[1])),h[i+3].split('=')[1].strip().strip('"'))

#Folder: Event stories
f=open('pullMaster'+os.path.sep+'MonoBehaviour'+os.path.sep+'StoryEventManagerMaster.txt','r',encoding="utf-8")
g=open('pullMaster'+os.path.sep+'MonoBehaviour'+os.path.sep+'StoryEventMaster.txt','r',encoding="utf-8")
h=f.readlines()
x=g.readlines()
for i in range(len(h)):
    if 'int id' in h[i]:
        #CUE!ROOM - Broadcast (identified by digit 6)
        if h[i+1].split('=')[1].strip()[0]==str(6):
            for t in range(len(x)):
                if 'int id' in x[t]:
                    if x[t].split('=')[1].strip()==h[i].split('=')[1].strip():
                        foe.addpair("BroadCast_{0:0=4d}_{1:0=2d}".format(int(h[i+1].split('=')[1]),int(x[t+1].split('=')[1])),x[t+2].split('=')[1].strip().strip('"'))
        #All other events (digit 1 or 2)
        else:
            for t in range(len(x)):
                if 'int id' in x[t]:
                    if x[t].split('=')[1].strip()==h[i].split('=')[1].strip():
                        foe.addpair("Event_{0:0=3d}_{1:0=2d}".format(int(h[i].split('=')[1]),int(x[t+1].split('=')[1])),x[t+2].split('=')[1].strip().strip('"'))

#Folder: Recording names (収録)
f=open('pullMaster'+os.path.sep+'MonoBehaviour'+os.path.sep+'RecordingMaster.txt','r',encoding="utf-8")
g=open('pullMaster'+os.path.sep+'MonoBehaviour'+os.path.sep+'ProductMaster.txt','r',encoding="utf-8")
h=f.readlines()
x=g.readlines()
for i in range(len(h)):
    #Mapping of recording ids to detail ids
    if 'int id' in h[i]:
        for t in range(len(x)):
            if 'int locationId' in x[t]:
                if int(x[t].split('=')[1])==int(h[i].split('=')[1]):
                    for a in range(1,4):
                        foe.addpair("Voice_Anime_{0:0=2d}_{1:0=1d}".format(int(h[i].split('=')[1]),a),x[t+2].split('=')[1].strip().strip('"'))

#Folder: Character episodes (キャラクターエピソード)
f=open('pullMaster'+os.path.sep+'MonoBehaviour'+os.path.sep+'StoryCardMaster.txt','r',encoding="utf-8")
h=f.readlines()
for i in range(len(h)):
    if 'int cardMasterId' in h[i]:
        foe.addpair("Card_{0:0=7d}_{1:0=1d}".format(int(h[i].split('=')[1]),int(h[i+1].split('=')[1])),h[i+2].split('=')[1].strip().strip('"'))

#Folder: Gacha audio (4★)
#Folder: Special lines on home screen for (unlocked) pulled cards (3★ & 4★)
f=open('pullMaster'+os.path.sep+'MonoBehaviour'+os.path.sep+'CardMaster.txt','r',encoding="utf-8")
h=f.readlines()
for i in range(len(h)):
    if 'int id' in h[i]:
        if int(h[i].split('=')[1].strip()[0])==3:
            foe.addpair("Voice_CardHome_{0:0=7d}".format(int(h[i].split('=')[1])),h[i+2].split('=')[1].strip().strip('"'))
        elif int(h[i].split('=')[1].strip()[0])==4:
            foe.addpair("Voice_CardGacha_{0:0=7d}".format(int(h[i].split('=')[1])),h[i+2].split('=')[1].strip().strip('"'))
            foe.addpair("Voice_CardHome_{0:0=7d}".format(int(h[i].split('=')[1])),h[i+2].split('=')[1].strip().strip('"'))

#Folder: Character Voice
#Folder: General Gacha Lines
#Folder: General Home Lines
#Folder: Gift Lines
#Folder: General Voice Lines
#Folder: Start/End of Recording Lines
#Folder: NPC Lesson Lines
f=open('pullMaster'+os.path.sep+'MonoBehaviour'+os.path.sep+'HeroineMaster.txt','r',encoding="utf-8")
h=f.readlines()
for i in range(len(h)):
    if 'int id' in h[i] and int(h[i].split('=')[1])<=16:
        foe.addpair("Voice_Chara_{0:0=3d}".format(int(h[i].split('=')[1])),h[i+2].split('=')[1].strip().strip('"')+' '+h[i+3].split('=')[1].strip().strip('"'))
        foe.addpair("Voice_Gacha_{0:0=3d}".format(int(h[i].split('=')[1])),h[i+2].split('=')[1].strip().strip('"')+' '+h[i+3].split('=')[1].strip().strip('"'))
        foe.addpair("Voice_Home_{0:0=3d}".format(int(h[i].split('=')[1])),h[i+2].split('=')[1].strip().strip('"')+' '+h[i+3].split('=')[1].strip().strip('"'))
        foe.addpair("Voice_Portal_{0:0=3d}".format(int(h[i].split('=')[1])),h[i+2].split('=')[1].strip().strip('"')+' '+h[i+3].split('=')[1].strip().strip('"'))
        foe.addpair("Voice_Part_{0:0=3d}".format(int(h[i].split('=')[1])),h[i+2].split('=')[1].strip().strip('"')+' '+h[i+3].split('=')[1].strip().strip('"'))
        foe.addpair("Voice_Recording_{0:0=3d}".format(int(h[i].split('=')[1])),h[i+2].split('=')[1].strip().strip('"')+' '+h[i+3].split('=')[1].strip().strip('"'))
    elif 'int id' in h[i]:
        foe.addpair("Voice_Part_{0:0=3d}".format(int(h[i].split('=')[1])),h[i+2].split('=')[1].strip().strip('"')+' '+h[i+3].split('=')[1].strip().strip('"'))
        foe.addpair("Voice_LessonNPC_{0:0=3d}".format(int(h[i].split('=')[1])),h[i+2].split('=')[1].strip().strip('"')+' '+h[i+3].split('=')[1].strip().strip('"'))


fl.port()