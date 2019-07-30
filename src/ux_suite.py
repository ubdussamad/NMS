# UX Suite for NMS
# Ref: Jul 30th , 2019
# Author: ubdussamad <[name][at][google's email]>
from api_applet import yahoo_api
import math,time , json
import pandas as pd

STATION = yahoo_api('kf.pyc')

class suite (object):
	def integrate_functionality(self):
		self.pushButton_5.clicked.connect(self.refresh)
		self.lineEdit.setPlaceholderText("Karnataka")
	def dummy(self):
		print("I am a dummy!")
	def refresh(self):
		location = self.lineEdit.text()
		data = STATION.query_(location if location else "Karnataka")

		#df = pd.DataFrame(data=data)
		try:
			temp = data['current_observation']['condition']['temperature']
			wind_speed = data['current_observation']['wind']['speed']
			wind_dirn = data['current_observation']['wind']['direction']
		except:
			self.statusbar.showMessage("Invalid Location Input!",4000)
			temp = "-- "
			wind_speed = "<i>N.A </i>"
			wind_dirn = "<i>N.A </i>"

		self.label_3.setText("<b>Wind</b>: %sKm/hr | <b>Dir</b>: %s°N"%(str(wind_speed),
			str(wind_dirn)))
		self.lcdNumber.display("%sC"%str(temp))
		self.textBrowser.setHtml(json.dumps(data['location'])+"<br/><br/><br/><br/>"+json.dumps(data['current_observation']))


if __name__ == "__main__":
	print("Hi this is a text text to see if all imports pass!")
	print("This message implies all the imports work fine!")