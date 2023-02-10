#pylint:disable=E0402
from kivy.uix.screenmanager import Screen
from Modules.db import cs
from ..Widget.Listitem import ListItemWithIcon


list_color= "white" #color of  text in notes screens .
class Cs_notes(Screen):
	
	def check_file_exist(self,file):
			#this method check the file existance"""
			from os.path import exists
			from os import getcwd as cwd
			a = exists(cwd()+"/Notes/"+ file + ".pdf")
			return a

	def add_list_items(self):
		for i in range(len(cs)):
			if cs[i]:
				icon="file-pdf-box"
				color= 1,0,0,1
				if self.check_file_exist(cs[i]) == True:
					icon="check-underline"
					color = 0,1,0,1
				self.ids.Mathlist.add_widget(ListItemWithIcon(text=cs[i],iconLeft=icon,theme_text_color="Custom",text_color=color))

	def clearList(self):
		self.ids.Mathlist.clear_widgets()
