from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from os import getcwd as cwd
import json
from kivymd_extensions.akivymd.uix.badgelayout import AKBadgeLayout
from kivymd_extensions.akivymd.uix.charts import AKBarChart
from libs.Widget.sqrCard import Icons

#default data for graph of records screen.
#unit_one_marks = [1,2,1,2,1]
#unit_two_marks = [1,2,1,2,1]
#unit_three_marks = [1,2,1,2,1]
#total_school_working_day = 88
##### This whole code convert the string values to integer..(values extracted from db)   ########
with open(r"{0}/Modules/loginfo.json".format(cwd()),"r+") as f:
	logged = json.loads(f.read())
	student_attendance = logged["userAttendence"]
	UTOmarks =logged["userMarks"]["UnitOneMarks"]
	UTTmarks =logged["userMarks"]["UnitTwoMarks"]
	UTThmarks =logged["userMarks"]["UnitThreeMarks"]
	total_school_working_day = 125
	###############
	if UTOmarks == [0 for x in range(5)]:	
		unit_one_marks = [1,2,3,4,5]
	else:
		unit_one_marks =UTOmarks
	if  UTTmarks == [0 for x in range(5)]:	
		unit_two_marks = [1,2,3,4,5]
	else:
		unit_two_marks = UTTmarks
	if  UTTmarks == [0 for x in range(5)]:	
		unit_three_marks = [1,2,3,4,5]
	else:
		unit_three_marks = UTThmarks	
#############	#############     ####################

def label_creator(data):
	"""creating y labels for bargraph"""
	label = []
	for i in data:
		b = str(i)+"/20"
		label.append(b)
	return label	
	
class RecordArea(Screen):
	stud_attend = student_attendance
	print("from record ", stud_attend)
	total_school_working_dy = total_school_working_day
	user_attendence_percentage = f"{(int(stud_attend)//total_school_working_dy)*100}"
	user_Result_analysis = "A+"
	Xvalues = [1,2,3,4,5]	
	Barlabel = ["Math","Cs","Physic","Chemistry","English"]
	ylabel = label_creator(unit_one_marks)
	Yvalues = unit_one_marks
	def on_enter(self):
		chart_bar = self.ids.chart
		chart_bar.update()
	def menu_box(self):
		self.a = self.ids.drop_btn
		marksMenuLabel = ["Unit one","Unit two","Unit three","Half yearly"]
		self.menu_items = [
			{
			"text": f"{marksMenuLabel[i]} marks",
			"viewclass": "OneLineListItem",
			"on_release": lambda x=f"{marksMenuLabel[i]} marks": self.menu_callback(x),
			} for i in range(0,4)
			]
		self.menu = MDDropdownMenu(
			caller=self.a,
			items=self.menu_items,
			position="auto",
			background_color=(1,1,1,1),
			opening_time=0,
			width_mult=4,
			)	
	def menu_callback(self, text_item):	
		def label_creator(data):
			"""creating y labels for bargraph"""
			label = []
			for i in data:
				b = str(i)+"/20"
				label.append(b)
			return label	
		self.menu.dismiss()
		self.ids.graph_title.text = f"{text_item}"
		list_text_item = text_item.split()
		chart_bar = self.ids.chart
		if list_text_item[1] == "Unit one marks":
			chart_bar.y_labels = label_creator(unit_one_marks)
			chart_bar.y_values = unit_one_marks
		elif list_text_item[1] == "Unit two marks":
			chart_bar.y_labels = label_creator(unit_two_marks)
			chart_bar.y_values = unit_two_marks	
		elif list_text_item[1] == "Unit three marks":
			chart_bar.y_labels = label_creator(unit_three_marks)
			chart_bar.y_values = unit_three_marks
		else:
			pass
		chart_bar.update()