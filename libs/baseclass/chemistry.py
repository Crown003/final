#pylint:disable=E0402
from kivy.uix.screenmanager import Screen
from Modules.db import c
from ..Widget.Listitem import ListItemWithIcon


list_color= "white" 
class Chemistry_notes(Screen):
	def check_file_exist(self,file):
			#this method check the file existance"""
			from os.path import exists
			from os import getcwd as cwd
			a = exists(cwd()+"/Notes/"+ file + ".pdf")
			return a

	def add_list_items(self):
		for i in range(len(c)):
			if c[i]:
				icon="file-pdf-box"
				color= 1,0,0,1
				if self.check_file_exist(c[i]) == True:
					icon="check-underline"
					color = 0,1,0,1
				self.ids.Mathlist.add_widget(ListItemWithIcon(text=c[i],iconLeft=icon,theme_text_color="Custom",text_color=color))

	def clearList(self):
		self.ids.Mathlist.clear_widgets()