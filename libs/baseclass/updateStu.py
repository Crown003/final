from kivy.uix.screenmanager import Screen
from Modules.db import collection
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
import multitasking
multitasking.set_max_threads(10)

class Update_Student(Screen):
	data = None
	@multitasking.task
	def loadData(self,enrollnum):
		try:
			self.data = collection.find_one({"Enrollment":enrollnum})
			self.addWidget()
			self.ids.updateBtn.disabled = False
		except Exception as e:
			print(e)	
	def on_leave(self):
		self.ids.EnrollmentNumber.text = ""
		self.ids.base.clear_widgets()
		self.data = None
		self.list = []
	def updateStudentDetails(self,enrollnum,*args):
		dict={}
		for i in args[0]:
			dict[i.hint_text] = i.text
		query = {"Enrollment":enrollnum}
		update_values = {"$set" : dict}
		collection.update_one(query,update_values)
		self.ids.base.clear_widgets()
		self.ids.EnrollmentNumber.text = ""
		self.ids.updateBtn.disabled = True
		toast("Student details updated successfully.")
	def addWidget(self,*args):
		for i,field in enumerate(self.data):
			if i>0 and i<10:
				self.ids.base.add_widget(MDTextField(hint_text=field,text=self.data[field],size_hint=[.8,.1]))