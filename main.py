from kivymd.app import MDApp
from kivy.core.window import Window 
Window.softinput_mode = 'below_target'
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.toast import toast
from Modules.help import helper
from libs.root import Root
from kivymd.uix.dialog import MDDialog
from libs.Widget.sqrCard import Icons
import io
import multitasking
from kivy import platform
from PIL import Image
import json
import gridfs
from os import getcwd as cwd


#this thread for making process in background.
multitasking.set_max_threads(10)


if  platform == "android":
	from Modules.pdfview import PdfView


class Main(MDApp):
		data_updated = False
		isdownloading = False
		fees_month = ""
		profile_flag = "0"
		image = r"assets/vidiya.png"	
		Username = f""
		User_profile = f""
		if User_profile == "":
			User_profile = r"assets/noprofile.png"
		else:
			pass
		UserClass = f""
		UserEmail = f""
		UserPhone = f""
		Cursor = helper()
		
		def build(self):
			self.theme_cls.primary_palette = "Pink"
			self.root = Root()
			self.root.load_screen("LoginPage")
			self.root.load_screen("Home")
			self.root.load_screen("Profile")
			self.root.load_screen("Teachers_interface")
			
		def on_start(self):
			try:	
				logged = self.Cursor.get_userdata()
				#checking the validation of user.
				if logged["status"] == "loggedout" :
					self.root.set_current("LoginPage")
								
				elif logged["status"] == "logged":
					if logged["role"].upper() == "STUDENT":
						self.root.set_current("Home")
						self.data_update()
						self.data_updated = True
					elif logged["role"].upper() == "TEACHER":
						self.root.set_current("Teachers_interface")
										
			except Exception as e:
				if e == FileNotFoundError:
					with open("./Modules/loginfo.json","x") as f:
						pass
				self.root.set_current("LoginPage")
		
		def data_update(self):
			"""This method update the user data according to their  profile."""
			check = self.Cursor.get_userdata()
			try:	
				a = self.get_Profile_image(check["userEnrollNum"],"./profile.png")
				User_profile = r"assets/noprofile.png"
				if a == "exist":
					User_profile ="./profile.png"
				self.root.get_screen("Profile").ids.profile_image.source = User_profile
				self.root.get_screen("Home").ids.main_page_profile.source = User_profile
				self.reload_home_image()
			except Exception as e:
				print("error from main data_update: ",e)
			try:
				self.root.get_screen("Home").ids.Nlabel.text = check["userName"].split()[0]
				self.root.get_screen("Home").ids.Clabel.text = check["userClass"] + check["userSection"]
				#below changing the profile details in profile screen.
				self.root.get_screen("Profile").ids.name_field.text = check["userName"]
				self.root.get_screen("Profile").ids.class_field.text = check["userClass"]
				self.root.get_screen("Profile").ids.contact_field.text = check["userPhone"]
				self.root.get_screen("Profile").ids.email_field.text = check["userEmail"]		
				self.data_updated = True
			except Exception as e:
				print("from main",e)
		def show_dialog(self,*args):
			"""this method popup the logout dialog box"""
			self.a = MDDialog(title="Logout of svm app ?",elevation=0,size_hint=(.9,.7),type="confirmation",buttons=[MDFlatButton(text="CANCEL",on_release=self.close_dialog_logout), MDRaisedButton(text="Log out",on_release=self.logout)])
			self.a.open()
			
		def close_dialog_logout(self,*args):
			"""this method popup the logout dialog box"""
			self.a.dismiss()

		def show_user_profile(self,hit_from):
			"""this method is created to access the profile from record & home both screens"""
			if hit_from == "account":
				self.root.set_current("Profile")
				self.profile_flag = "RecordArea"
			elif hit_from == "settings":
				self.root.set_current("Profile")
				self.profile_flag = "Settings"
			elif hit_from == "account-circle":
				self.profile_flag = "nav"
				self.root.set_current("Profile")
			else:
				pass
			
		def back(self):
			"""this method is for getting back from profile screen to previous screen. i.e"record or home."""
			if self.profile_flag == "nav":
				self.root.transition.direction = "right"
				self.root.current = "Home"
			elif self.profile_flag == "RecordArea":
				self.root.transition.direction = "right"
				self.root.current = "RecordArea"
			elif self.profile_flag == "Settings":
				self.root.transition.direction = "right"
				self.root.current = "Settings"
			else:
				pass
				
		def payFees(self,*args):
			from kivymd.uix.bottomsheet import MDCustomBottomSheet
			from kivymd.factory_registers import Factory
			self.fees_month = f"{args[0]}"
			self.custom_sheet = MDCustomBottomSheet(screen=Factory.ContentCustomSheet())
			self.custom_sheet.open()
		def closePayFees(self,*args):
			self.custom_sheet.dismiss()
				
		def reload_home_image(self):
			"""this method reload the profile image in home & profile screen"""
			self.root.get_screen("Home").ids.main_page_profile.reload()
			self.root.get_screen("Profile").ids.profile_image.reload()
		
		def get_Profile_image(self,enrollment_no,path):
			from Modules.db import collection
			"""this method downloads the profile image of user"""
			try:
				image = collection.find_one({"Enrollment":enrollment_no})
				pil_img = Image.open(io.BytesIO(image['ProfileImage']))
				profile_path = path
				pil_img.save(profile_path)
				return "exist"
			except Exception as e:
				print(e)
			
		def check_file_exist(self,file):
			"""this method check the file existance"""
			from os.path import exists
			from os import getcwd as cwd
			import os
			if exists(cwd()+"/Notes/"):
				a = exists(cwd()+"/Notes/"+ file + ".pdf")
				return a
			else:
				os.mkdir("Notes")
				a = exists(cwd()+"/Notes/"+ file + ".pdf")
				return a
				
		@multitasking.task		
		def downloadProgressStart(self,screen):
				self.root.get_screen(screen).ids.progressdownloadlabel.text = "downloading."
				
		def download_file(self,name_of_file):
			from Modules.db import db
			fs = gridfs.GridFS(db)		
			data = db.fs.files.find_one({"filename":name_of_file+".pdf"})
			my_id = data["_id"]
			outputdata = fs.get(my_id).read()
			if platform != "android":
				download_location = cwd()+"\\Notes\\" + name_of_file + ".pdf"
			else:
				download_location = cwd()+"/Notes/"+ name_of_file + ".pdf"	
			output = open(download_location,"wb+")
			output.write(outputdata)
			output.close()
				
		def checking_pdf_exist(self,a,name_of_file):
			from os import getcwd as cwd
			a = cwd()+"/Notes/"+ name_of_file + ".pdf" 
			toast("file already exist! Opening file.")
			if platform == "android":
				PdfView(a)
			else:
				import webbrowser as webb
				webb.open_new(a)
				
		@multitasking.task			 
		def main_down_file(self,name_of_file,screen):
			"""method to download the notes pdf"""
			a = self.check_file_exist(name_of_file)
			if a:
				self.checking_pdf_exist(a,name_of_file)
			else:
				toast("Dowloading "+name_of_file.lower()+".pdf")	
				self.downloadProgressStart(screen) # circular indicator of downloading.	
				self.isdownloading = True
				self.download_file(name_of_file)
				self.root.get_screen(screen).ids.progressdownloadlabel.text = ""	
				toast(name_of_file.lower()+".pdf"" successfully.")
	
						
		def logout(self,*args):
			"""method to logout the user"""
			self.data_updated = False
			with open("./Modules/loginfo.json","w") as f:
				json.dumps(f.write('{"status": "loggedout"}'))
			self.root.set_current("LoginPage")
			self.close_dialog_logout()
	
if __name__ == "__main__":
	Main().run()