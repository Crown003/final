from kivy.uix.screenmanager import Screen
from ..Widget.PayFeesList import PayFees
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from Modules.help import helper
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from Modules.db import collection
from main import helper
import json
class Pay_Fees(Screen):
	Cursour = helper()
	iconLeft="cash-clock"
	def addwid(self):
		data = self.Cursour.get_userdata()
		import calendar as cal
		a = [cal.month_name[i] for i in range(1,13)]#+ [cal.month_name[i] for i in range(1,4)]
		print(a)
		for k,i in enumerate(a,start=0):
			print(k," ",i)
			if data["FeesStructure"][k] != 0:
				self.ids.Fees.add_widget(PayFees(
					text=i,iconLeft="clock-check",iconRight="credit-card-check",iconRightColor="#00ff00",callback=self.callback))
			else:
				self.ids.Fees.add_widget(PayFees(
				text=i,iconLeft="clock-check",iconRight="credit-card-check",iconRightColor ="#0000ff",callback=self.callback))
	
	def callback(self,*args):
		return args[0]
		
	def on_enter(self):
		self.addwid()
	def on_leave(self):
		self.ids.Fees.clear_widgets()
		

class ContentCustomSheet(MDBoxLayout):
	pass
	
class ItemForCustomBottomSheet(MDCard):
	Cursour = helper()
	data = Cursour.get_userdata()
	fees_str = {"7":1000,"8":1000,"9":1500,"10":1500,"11":2000,"12":2000,}
	amount = fees_str[data["userClass"]]
	stuname = data["userName"]
	stuclass = data["userClass"]
	main_obj = Pay_Fees()
	def get_payment(self,amount,month_name):
		from datetime import datetime
		import json
		self.data["FeesStructure"][datetime.strptime(month_name, '%B').month-1] = 1
		print(self.data["FeesStructure"])
		query = {"Enrollment":self.data["userEnrollNum"]}
		update_values = {"$set" : {"FeesStructure":self.data["FeesStructure"]}}
		try:
			self.Cursour.push_userdata(str(json.dumps(self.data)))
			collection.update_one(query,update_values)
			donepayment = MDRaisedButton(text="Ok",on_release=self.closePayment)
			self.paymentScreen = MDDialog(
			title="PAYEMENT SUCCESSFUL !",
			text="this is just a sample.",
			buttons =[donepayment] )
			self.paymentScreen.open()
		except Exception as e:
			print(e)
	def closePayment(self,*args):
		self.paymentScreen.dismiss()
			