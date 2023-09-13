#!/usr/bin/env python3.11
#coding=utf-8

from tkinter import *
import tkinter
import platform
import os
import sys
import hashlib
from sys import version_info
import tkinter.messagebox as mb
from tkinter import filedialog

class Application(Frame):
	def openfile_ddi(self):
		self.file_opt = {}
		self.file_opt ['defaultextension'] = '.ddi'  
		self.file_opt ['filetypes'] = [("VOCALOID DDI","*.ddi")]  
		self.file_opt ['parent'] = self 
		self.file_opt ['title'] = 'Select DDI File'  
		fname = filedialog.askopenfilename(**self.file_opt)
		return fname

	def openfile_dvqm(self):
		self.file_opt = {}
		self.file_opt ['defaultextension'] = '.dat'  
		self.file_opt ['filetypes'] = [("dvqm.dat","*.dat")]  
		self.file_opt ['parent'] = self 
		self.file_opt ['title'] = 'Select dvqm.dat File'  
		fname = filedialog.askopenfilename(**self.file_opt)
		return fname
	
	def doCmd(self,cmdline):
		print("cmdline")
		print(cmdline)
		var = os.popen(cmdline).read()
		return var

	def doCmd_Plist(self,cmd,plistfile):
		return self.doCmd('/usr/libexec/PlistBuddy -c "'+cmd+'" "'+plistfile+'"')

	def decCOMPID(self,compid):
		bdir=os.path.split(os.path.realpath(__file__))[0]
		self.doCmd('chmod +x \"'+bdir+'/date2drp2\"')
		dec = self.doCmd('\"'+bdir+'/date2drp2\" '+compid+' 2>&1').replace('\x00','');
		return dec

	def anaCOMPID(self,compid):
		bdir=os.path.split(os.path.realpath(__file__))[0]
		self.doCmd('chmod +x \"'+bdir+'/date2drp2\"')
		dec = self.doCmd('\"'+bdir+'/date2drp2\" '+compid+' 2>&1').replace('\x00','');
		lendec=len(dec)
		self.DB_Success=0
		if(lendec==14):
			self.DB_Success=1
			self.DB_Decode=dec
			self.DB_Ver=dec[9]
			self.DB_Drp=""+dec[1]+dec[2]+"00"+dec[5]+dec[6]
			self.DB_Key=hashlib.md5(self.DB_Decode.encode('utf-8')).hexdigest()

	def debug(self):
		if(self.DB_Success==1):
			print(self.DB_Decode)
			print(self.DB_Ver)
			print(self.DB_Drp)
			print(self.DB_Key)
			print(self.DB_Type)
			print(self.DB_Name)
			print(self.DB_Path)
			print(self.DB_CompID)

	def getPathNodeName(self,path):
		arr=path.split('.')
		if(len(arr)>0):
			return arr[0]
		else:
			return ""

	def getCurName(self,path):
		return os.path.basename(path)

	def getParentPath(self,path):
		return os.path.abspath(os.path.dirname(path)+os.path.sep+".")

	def anaPath(self,path):
		return ""
	def getPLRoot(self):
		if(self.DB_Ver=='3'):
			self.PL_Root="DATABASE:VOICE3"
		elif(self.DB_Ver=='4'):
			self.PL_Root="DATABASE41"
		elif(self.DB_Ver=='5'):
			self.PL_Root="Voice:Components"

	def doAction(self):
		if(self.DB_Success==1):
			self.PL_File="/Library/Preferences/com.yamaha.VOCALOID"+self.DB_Ver+".system.plist"
			if(self.DB_Ver=='5'):
				self.PL_File="/Library/Preferences/com.yamaha.VOCALOID5.plist"

			if(self.DB_Type=="VOCALOID DVQM"):
				print("DVQM")
				self.PL_Root=""
				if(self.DB_Ver=='5'):
					self.PL_Root="AttackReleaseLib:Components"
					ppid=self.PL_Root+":"+self.DB_CompID
					pDel="Delete "+ppid+":"
					pAdd="Add "+ppid+":"
					pTh=self.DB_Path.replace('\"','\\\"')
					pTh=pTh.replace('\'','\\\'')
					pTh=pTh.replace('\\','\\\\')
					pTh=pTh.replace("(","\(")
					pTh=pTh.replace(")","\)")
					pTh=pTh.replace('[','\[')
					pTh=pTh.replace(']','\]')
					pTh=pTh.replace('{','\{')
					pTh=pTh.replace('}','\}')
					pTh=pTh.replace(' ','\ ')
					
					arr_cmp=[]
					arr_pt=self.DB_Path.split("/")
					for arrp in arr_pt:
						if(len(arrp)==16):
							if(arrp[0]=='B'):
								srs=self.decCOMPID(arrp)
								if(len(srs)==14 and srs[9]=='5'):
									arr_cmp.append(arrp)

					self.doCmd_Plist(pDel+':Path',self.PL_File)
					self.doCmd_Plist(pDel+':Version:Major',self.PL_File)                                        
					self.doCmd_Plist(pDel+':Version:Minor',self.PL_File)                                        
					self.doCmd_Plist(pDel+':Version:Revision',self.PL_File)
					for voicesp in arr_cmp:
						self.doCmd_Plist(pDel+':Voices:'+voicesp,self.PL_File)
						self.doCmd_Plist(pAdd+':Voices:'+voicesp+' integer 1',self.PL_File)
					self.doCmd_Plist(pAdd+':Path string \"'+pTh+'\"',self.PL_File)
					self.doCmd_Plist(pAdd+':Version:Major integer 5',self.PL_File)
					self.doCmd_Plist(pAdd+':Version:Minor integer 0',self.PL_File)
					self.doCmd_Plist(pAdd+':Version:Revision integer 1',self.PL_File)
					mb.showinfo('Status','Success!')

			else:
				print("VDB")
				self.PL_Root=""
				self.getPLRoot()
				if(self.PL_Root==""):
					return
				if self.DB_Ver=='5' :
					ppid=self.PL_Root+":"+self.DB_CompID
					pDel="Delete "+ppid+":"
					pAdd="Add "+ppid+":"
					pTh=self.DB_Path.replace('\"','\\\"')
					pTh=pTh.replace('\'','\\\'')
					pTh=pTh.replace('\\','\\\\')
					pTh=pTh.replace("(","\(")
					pTh=pTh.replace(")","\)")
					pTh=pTh.replace('[','\[')
					pTh=pTh.replace(']','\]')
					pTh=pTh.replace('{','\{')
					pTh=pTh.replace('}','\}')
					pTh=pTh.replace(' ','\ ')

					self.doCmd_Plist(pDel+"BankName",self.PL_File)
					self.doCmd_Plist(pDel+'DRP',self.PL_File)
					self.doCmd_Plist(pDel+'Name',self.PL_File)
					self.doCmd_Plist(pDel+'Date',self.PL_File)
					self.doCmd_Plist(pDel+'Key',self.PL_File)

					self.doCmd_Plist(pAdd+'BankName string \"'+self.DB_Name+'\"',self.PL_File)
					self.doCmd_Plist(pAdd+'DRP string \"'+self.DB_Drp+'\"',self.PL_File)
					self.doCmd_Plist(pAdd+'Name string \"'+self.DB_Name+'\"',self.PL_File)
					self.doCmd_Plist(pAdd+'Date string \"BHMN74F9ED86FKAB\"',self.PL_File)
					self.doCmd_Plist(pAdd+'Key string \"'+self.DB_Key+'\"',self.PL_File)

					self.doCmd_Plist(pDel+':Path',self.PL_File)
					self.doCmd_Plist(pDel+':Version:Major',self.PL_File)
					self.doCmd_Plist(pDel+':Version:Minor',self.PL_File)
					self.doCmd_Plist(pDel+':Version:Revision',self.PL_File)

					self.doCmd_Plist(pAdd+':Path string \"'+pTh+'\"',self.PL_File)
					self.doCmd_Plist(pAdd+':Version:Major integer 5',self.PL_File)
					self.doCmd_Plist(pAdd+':Version:Minor integer 0',self.PL_File)
					self.doCmd_Plist(pAdd+':Version:Revision integer 1',self.PL_File)
					mb.showinfo('Status','Success!')
				else:
					ppid=self.PL_Root+":"+self.DB_CompID
					pDel="Delete "+ppid+":"
					pAdd="Add "+ppid+":"
					pTh=self.DB_Path.replace('\"','\\\"')
					pTh=pTh.replace('\'','\\\'')
					pTh=pTh.replace('\\','\\\\')
					pTh=pTh.replace("(","\(")
					pTh=pTh.replace(")","\)")
					pTh=pTh.replace('[','\[')
					pTh=pTh.replace(']','\]')
					pTh=pTh.replace('{','\{')
					pTh=pTh.replace('}','\}')
					pTh=pTh.replace(' ','\ ')

					self.doCmd_Plist(pDel+'DRP',self.PL_File)
					self.doCmd_Plist(pDel+'INSTALLED',self.PL_File)
					self.doCmd_Plist(pDel+'NAME',self.PL_File)
					self.doCmd_Plist(pDel+'PATH',self.PL_File)
					self.doCmd_Plist(pDel+'TIME',self.PL_File)
					self.doCmd_Plist(pDel+'KEYS:default',self.PL_File)

					self.doCmd_Plist(pAdd+'DRP string \"'+self.DB_Drp+'\"',self.PL_File)
					self.doCmd_Plist(pAdd+'INSTALLED integer 1',self.PL_File)
					self.doCmd_Plist(pAdd+'NAME string \"'+self.DB_Name+'\"',self.PL_File)
					self.doCmd_Plist(pAdd+'PATH string \"'+pTh+'\"',self.PL_File)
					self.doCmd_Plist(pAdd+'TIME string \"BHMN74F9ED86FKAB\"',self.PL_File)
					self.doCmd_Plist(pAdd+'KEYS:default string \"'+self.DB_Key+'\"',self.PL_File)
					mb.showinfo('Status','Success!')

		
	def returnBack(self):
                self.label_dbtype = Label(self, text="          Unknown          ").grid(row=1,column=1)
                self.label_dbcompid = Label(self, text="          Unknown          ").grid(row=2,column=1)

	def doSelDDI(self):
		self.returnBack()
		ddi=self.openfile_ddi()
		if(len(ddi)>0):
			par=self.getParentPath(ddi)
			dirid=self.getCurName(par)
			if(len(dirid)==16):
				self.DB_CompID=dirid
				self.DB_Path=self.getParentPath(par)
				self.DB_Name=self.getPathNodeName(self.getCurName(ddi))
				self.DB_Type="VocaloidDB "+self.DB_Name
				self.anaCOMPID(self.DB_CompID)
				self.label_dbtype=Label(self, text=self.DB_Type).grid(row=1,column=1)
				self.label_dbcompid=Label(self, text=self.DB_CompID).grid(row=2,column=1)
	
	def doSelDVQM(self):
		self.returnBack()
		dvqm=self.openfile_dvqm()
		if(len(dvqm)>0):
			self.DB_Success=0
			dva=self.getPathNodeName(self.getCurName(dvqm)).lower()
			if(dva=="dvqm"):
				par=self.getParentPath(dvqm)
				dirid=self.getCurName(par)
				if(len(dirid)==16):
					self.DB_CompID=dirid
					self.DB_Ver='5'
					self.DB_Path=self.getParentPath(par)
					self.DB_Type="VOCALOID DVQM"
					self.DB_Success=1
					self.label_dbtype=Label(self, text=self.DB_Type).grid(row=1,column=1)
					self.label_dbcompid=Label(self, text=self.DB_CompID).grid(row=2,column=1)
	def sudoRun(self):
		supwd=self.su_pwd.get()
		supwd=supwd.replace('\"','\\\"')
		supwd=supwd.replace('\'','\\\'')
		supwd=supwd.replace('\\','\\\\')
		ret=self.doCmd('echo \"'+supwd+'\"|sudo -S echo ALLISRIGHT')
		if 'ALLISRIGHT' in ret:
			#cmd='/usr/bin/env python'+str(version_info.major)+'.'+str(version_info.minor)
			bdir=os.path.split(os.path.realpath(__file__))[0]
			cmd=bdir+'/python'
			cmd=cmd.replace(' ','\ ')
			cmdstr=cmd+' '+os.path.realpath(__file__).replace(' ','\ ')
			self.mainWindow.geometry("+99999+99999")
			self.update()
			self.doCmd('echo \"'+supwd+'\"|sudo -S '+cmdstr)
			sys.exit(0)
		else:
			mb.showinfo('Sudo','Sudo Error, check password!')

	def createWidgets(self):
		if(self.os=="Mac"):	
			if(os.geteuid()==0):
				if version_info.major != 3:
					self.labelM=Label(self,text="Error:This Script is based on Python 3!").grid(row=1,columnspan=2)
				else:
					self.labelOS=Label(self,text="CurOS:").grid(row=0,column=0)
					self.labelOS2=Label(self,text=self.os).grid(row=0,column=1)
					self.label1 = Label(self, text="DBType:").grid(row=1,column=0)
					self.label_dbtype = Label(self, text="Unknown").grid(row=1,column=1)
					self.label2 = Label(self, text="DBCompID:").grid(row=2,column=0)
					self.label_dbcompid = Label(self, text="Unknown").grid(row=2,column=1)
		
					self.SelDDI = Button(self, text="Find VOCALOID DB",command=self.doSelDDI)
					self.SelDDI.grid(row=3,column=0)
			
					self.btn2 = Button(self, text="Find AttackReleaseLib",command=self.doSelDVQM)
					self.btn2.grid(row=3,column=1)
			
					self.btnX = Button(self, text="Install Select Components",command=self.doAction)
					self.btnX.grid(row=4,columnspan=2)
			else:
				self.labelM=Label(self,text="Script need root privilege to work").grid(row=0,columnspan=2)
				self.labelR=Label(self,text="Sudo Password:").grid(row=1,column=0)
				self.su_pwd=tkinter.StringVar()
				self.su_entry=Entry(self,textvariable=self.su_pwd,show="*").grid(row=1,column=1)
				self.button=Button(self,text="Run",command=self.sudoRun).grid(row=2,columnspan=2)
				
		else:
			self.labelM=Label(self,text="Error:This Script is Only For MacOSX").grid(row=1,columnspan=2)


	def __init__(self,master=None):
		if(platform.system()=="Windows"):
			self.os="Win"
		elif(platform.system()=="Darwin"):
			self.os="Mac"
		else:
			self.os="Other"
		Frame.__init__(self,master)
		master.title('VOCALOID DB Installer')

		master.wm_attributes('-topmost',1)
		nScreenWid, nScreenHei = master.maxsize()
		nCurWid = 400
		nCurHeight = 150
		master.geometry("{}x{}+{}+{}".format(nCurWid, nCurHeight, 655, 415))
		self.mainWindow=master
		self.pack()
		self.createWidgets()
def main():
	root = Tk()
	app = Application(master=root)
	app.mainloop()

main()

