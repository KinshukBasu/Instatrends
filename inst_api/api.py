import requests
import json
import os
import geopy
from geopy.distance import VincentyDistance

JSON_DIR = "./json"

class API:

	_ACCESS_TOKEN = '3657796690.e029fea.9e40d79b56004ec5968b94ac28b4896b'
	
	def __init__(self, lat, lng, dist):
		#initialize params
		self.lat = lat
		self.lng = lng
		self.dist = dist
		self.loc_list = []
		
	def get_raw_json(self):			
		#Get Request
		r = requests.get('https://api.instagram.com/v1/media/search?lat=' + str(self.lat) 
		+'&lng=' + str(self.lng) 
		+'&access_token=' + self._ACCESS_TOKEN 
		+'&distance=' + str(self.dist))
		
		#Write raw JSON data
		if not os.path.exists(JSON_DIR):
			os.makedirs(JSON_DIR)
		f = open(os.path.join(JSON_DIR, "raw_data.json"), "a")
		f.write(r.text)
		f.close()
		
		json_object = r.json()
		
		#Store info in list of dictionaries
		for item in json_object['data']:
			dict = {}		
			dict['media_type'] = item['type']
			dict['location'] = item['location']
			dict['tags'] = item['tags']
			temp = item['caption']

			if(temp is not None):
				dict['caption_text'] = temp['text']
			self.loc_list.append(dict)
			

	def write_filtered_json(self):
		#Open JSON file	
		if not os.path.exists(JSON_DIR):
			os.makedirs(JSON_DIR)
		f = open(os.path.join(JSON_DIR, "filtered_data.json"), "a")
		
		#Convert list of dicts to JSON
		json_string = json.dumps(self.loc_list)
		
		#Write JSON file
		f.write(json_string)
		f.close()
	
	def run(self):
		self.get_raw_json()
		self.write_filtered_json()



def extendRange():
	#Radius is measured in kilometres here

	lat1 = 35.775445
	lon1 = -78.687043



	new_api = API(lat1, lon1, 5000)
	new_api.run()


	d=5 						#Distance for Vincenty function
	
	for bearing in range(0,360,45):
		origin = geopy.Point(lat1, lon1)
		destination = VincentyDistance(kilometers=d).destination(origin, bearing)

		lat2, lon2 = destination.latitude, destination.longitude

		print lat2, lon2
		new_API = API(lat2, lon2, 5000)
		new_api.run()
		lat1 = lat2
		lon1 = lon2		

	return

if __name__ == '__main__':
	extendRange()		


