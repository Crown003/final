from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton


class FeesArea(Screen):
	def feesRecipt(self,*args):
		from kivymd.uix.bottomsheet import MDCustomBottomSheet
		from kivymd.factory_registers import Factory
		self.custom_sheet = MDCustomBottomSheet(screen=Factory.ContentSheet())
		self.custom_sheet.open()
	
		
class ContentSheet(MDBoxLayout):
	def sendUserMail(self,monthName):
		done_btn = MDRaisedButton(text="OK",md_bg_color=[1,0,.5,1],on_release=self.closeDialog)
		if monthName != "":
			self.dialog = MDDialog(title="SUCCESSFUL ",text="Recipt Transfered ! please check your email",
			buttons=[done_btn],size_hint=[.8,None])
			self.dialog.open()
		else:
			toast(f"Please provide some data.")
	def closeDialog(self,*args):
			self.dialog.dismiss()
			