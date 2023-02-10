from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.app import MDApp
from kivy.lang import Builder
app = MDApp.get_running_app()

kv = """
<PayFees>
	id:feestext
	on_release:
		app.payFees(self.text)
    IconLeftWidget:
        icon:root.iconLeft
        theme_text_color:"Custom"
        text_color:1,0,0,1
	IconRightWidget:
		icon:root.iconRight
		theme_text_color:"Custom"
        text_color:root.iconRightColor
        on_release:
        	app.payFees(feestext.text)
"""

from kivy.properties import (
StringProperty,
ObjectProperty,
ColorProperty,
)
class PayFees(OneLineAvatarIconListItem):
	Builder.load_string(kv)
	text = StringProperty()
	iconLeft = StringProperty("file-pdf-box")
	iconRight = StringProperty("download")
	callback = ObjectProperty()
	iconRightColor= ColorProperty("#0000ff")