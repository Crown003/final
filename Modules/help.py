import json
from kivymd.toast import toast
class helper():
	def get_userdata(self):
		try:
			#opening file containing userlogin informations.
			with open("./Modules/loginfo.json","r+") as f:
				userdata = json.loads(f.read())
				return userdata
		except Exception as e:
			print(e)
			toast("unable to fetch user's data.")
			return 404
		
	def push_userdata(self,*args):
		try:
			print(args[0])
			#opening file containing userlogin informations.
			with open("./Modules/loginfo.json","w+") as f:
				json.dumps(f.write(args[0]))
		except Exception as e:
			print(e)
			toast("unable to update user's data.")
			return 404