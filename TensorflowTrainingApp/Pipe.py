from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import * 
from wired_module import * 
#	Generated By WiredQT for Python: by Rocky Nuarin, 2021 Phils
import sys
from subprocess import PIPE, Popen
from threading  import Thread
from queue import Queue, Empty

class Handler(QtWidgets.QWidget,usercontrol):
	#WiredEvent def finishExecuting()#
	#WiredEvent def on_messagePipe(msg)
	def __init__(self, *param):    
		super(Handler, self).__init__(None)
		initUI(self,param,w=400,h=400,title="WiredQTv5.0",controlbox=True,startpos=(0,30),timeoutdestroy=-1)
		self.GTKForms()
		self.timer=QtCore.QTimer()
		self.timer.timeout.connect(self.loop)
		self.timer.start(10)   
		self.sch=Scheduler(500)#500 ms
		self.sch.Start()
		self.process=None
	
	def connect(self,ev,evusr):
		self.wiredevents.update({ev:evusr})
	def activeXcreated(self,*args):
		pass
	
	def loop(self):
		if self.process!=None:
			self.CheckTraceError()
		if self.process!=None and self.process.poll()!=None:
			for a in range(3):
				refreshGTK()
				self.CheckTraceError()			
						
			self.process=None
			print('Process terminated')
			if self.caller!=None and 'finishExecuting' in self.wiredevents:self.wiredevents['finishExecuting']()
		if self.form_load==False:
			self.form_load=True
		if self.sch.Event():#timer routine
			#code here
			if self.timeoutdestroy!=-1:
				self.timeoutdestroy-=1
				if self.timeoutdestroy==0:
					self.unload(None)
			self.sch.Start()#restart scheduler
		return True	#return true so that main_loop can call it again 	
	def createwidget(self,prop,control,parent,event=[]):
		createWidget(self,prop,control,parent,event)
	def GTKForms(self):		pass	def Widget(self):
		return self
	def CheckTraceError(self):
		def getLine():
			try:  line = self.queue.get_nowait()
			except Empty:
				return ""
			else: # got line
				#...do something with line
				return line.decode()
		def getLine2():
			try:  line = self.queue2.get_nowait()
			except Empty:
				return ""
			else: # got line
				#...do something with line
				return line.decode()
		
		buf=getLine()
		buf2=getLine2()
		if (buf2!=''):
			if self.caller!=None and 'on_messagePipe' in self.wiredevents:self.wiredevents['on_messagePipe'](buf2)
			
		line=''
		while(buf!=''):
			line+=buf
			buf=getLine()
		if line!='':
			if self.caller!=None and 'on_messagePipe' in self.wiredevents:self.wiredevents['on_messagePipe']("stderr:" + line)
			

	def ExecCommand(self,cmdlst):
		ON_POSIX = 'posix' in sys.builtin_module_names	

		def enqueue_output(out, queue):
			for line in iter(out.readline, b''):
				queue.put(line)
			out.close()
		def enqueue_output2(out, queue):
			for line in iter(out.readline, b''):
				queue.put(line)
			out.close()
		self.process = Popen(cmdlst, stderr=PIPE,stdout=PIPE ,stdin=PIPE, bufsize=1, close_fds=ON_POSIX)
		self.queue = Queue()
		self.queue2 = Queue()
		t = Thread(target=enqueue_output, args=(self.process.stderr, self.queue))
		t.daemon = True # thread dies with the program
		t.start()
					
		t = Thread(target=enqueue_output2, args=(self.process.stdout, self.queue2))
		t.daemon = True # thread dies with the program
		t.start()	
		pass
	def AbortExecution(self):
		if self.process!=None:
			self.process.terminate()
		pass
	
	def SendPipe(self,cmd):
		if self.process!=None:
			self.process.stdin.write(cmd.encode())
			self.process.stdin.flush()
		pass
if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	w = Handler()
	w.show()
	sys.exit(app.exec_())
