#coding:utf-8
import os
import sys
import subprocess
import threading
import time
import signal
import re

music=[]
start=0
player=0
stop=0
page=10
cur_jl=0
padd="      "
def ff(s):
	if re.match(r'.*\.mp3',s)==None:
		return False;
	return True

def  loadmusic():
	global music
	if len(sys.argv)>1:
		dd=sys.argv[1]
		if not os.path.isdir(dd):
			print "path error"
			sys.exit()
	else:
		dd='/home/sujianwei/py-music'
	os.chdir(dd)
	music=filter(ff,os.listdir(dd))
	if len(music)==0:
		print "mp3 not found"
		sys.exit()

def subplayer(path):
	global player
	player=subprocess.Popen(['mpg123', path],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	player.wait()
	return 0

def fresh(left,right,index=-1):
	global cur_jl,page,padd
	os.system("clear")
	print "\n\033[1;34m"+padd+"* * * * * * * * * *  Welcome To Py Music!  * * * * * * * * * * \n"
	for v in enumerate(music[left:right+1]):
		if (v[0]+left)==index:
			print "\033[1;3%dm%s%4d      >> %s"%(v[0]%8,padd,left+v[0],v[1])
		else:
			print "\033[1;34m%s%4d         >> %s"%(padd,left+v[0],v[1])
	print '\033[1;37m'

def jump_j():
	global cur_jl,page
	if cur_jl==0:
		left=0
	else:
		cur_jl=cur_jl-1
		left=cur_jl*page
	fresh(left,left+page-1)

def jump_l():
	global cur_jl
	cur_jl=cur_jl+1
	if cur_jl*page+page-1>=(len(music)-1):
		if cur_jl*page>len(music)-1:
			cur_jl=cur_jl-1
		left=cur_jl*page
		right=len(music)-1
	else:
		left=cur_jl*page
		right=cur_jl*page+page-1
	fresh(left,right)
	
def mloop():
	global player,start,stop,cur_jl,page,padd
	fresh(0,page-1)
	while True:
		cli=raw_input(padd+">>")
		if cli=='q':
			if player!=0:
				player.kill()
			print '\033[0m'
			sys.exit()
			return 0
		if cli==' ' and start==1:
			if stop:
				os.kill(player.pid, signal.SIGSTOP)
				stop=0
			else:
				os.kill(player.pid, signal.SIGCONT)
				stop=1
			continue
		elif cli=='j':
			jump_j()
			continue
		elif cli=='l':
			jump_l()
			continue
		elif cli=='f':
			fresh(0,page)
			continue 
		if re.match(r'^[0-9]+$',cli)==None:
			continue
		index=int(cli)
		if index<0 or index>=len(music):
			print padd+"range out!"
			continue
		if start:
			player.kill()
		fresh(cur_jl*page,cur_jl*page+page-1,index)
		t=threading.Thread(target=subplayer,args=(music[index],))
		t.start()
		start=1
		stop=1

loadmusic()
mloop()



