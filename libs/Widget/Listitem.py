from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.app import MDApp
from kivy.lang import Builder
app = MDApp.get_running_app()
kv = """
<ListItemWithIcon>
	on_release:
		app.main_down_file(self.text,self.parent.name)
    IconLeftWidget:
        icon:root.iconLeft
        theme_text_color:"Custom"
        text_color:1,0,0,1
        on_release:
        	app.main_down_file(self.text,self.parent.name)
	IconRightWidget:
		icon:root.iconRight
		theme_text_color:"Custom"
        text_color:get_color_from_hex("#4467c4")
        on_release:
        	app.main_down_file(self.text,self.parent.name)
"""

from kivy.properties import (
StringProperty,
)
class ListItemWithIcon(OneLineAvatarIconListItem):
	Builder.load_string(kv)
	text = StringProperty()
	iconLeft = StringProperty("file-pdf-box")
	iconRight = StringProperty("download")