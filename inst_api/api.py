import requests
import json
import os

JSON_DIR = "./json"

class API:

	_ACCESS_TOKEN = '3657796690.e029fea.9e40d79b56004ec5968b94ac28b4896b'
	
	def __init__(self, lat, lng, dist):
		#initialize params
		self.lat = lat
		self.lng = lng
		self.dist = dist
		self.loc_list = []

#--------------------------------------------------------------------------------------------------		
		
	def get_raw_json(self):			
		#Get Request
		r = requests.get('https://api.instagram.com/v1/media/search?lat=' + str(self.lat) 
		+'&lng=' + str(self.lng) 
		+'&access_token=' + self._ACCESS_TOKEN 
		+'&distance=' + str(self.dist))
		
		#Write raw JSON data
		if not os.path.exists(JSON_DIR):
			os.makedirs(JSON_DIR)
		f = open(os.path.join(JSON_DIR, "raw_data.json"), "w")
		f.write(r.text)
		f.close()
		
		json_object = r.json()
		
		#Store info in list of dictionaries
		for item in json_object['data']:
			dict = {}		
			dict['media_type'] = item['type']
			dict['location'] = item['location']
			self.loc_list.append(dict)
			
#------------------------------------------------------------------------------------------------

	def write_filtered_json(self):
		#Open JSON file	
		if not os.path.exists(JSON_DIR):
			os.makedirs(JSON_DIR)

		f = open(os.path.join(JSON_DIR, "filtered_data.json"), "w")

		filename = "filtered_data.json"

		if not os.access(filename, os.W_OK):
			print "Write access not permitted on %s" % filename
		
		#Convert list of dicts to JSON
		json_string = json.dumps(self.loc_list)
		
		#Write JSON file
		f.write(json_string)
		f.close()

	
	def get_data(self):
		self.get_raw_json()
		self.write_filtered_json()

		

if __name__ == '__main__':
	new_api = API(35.775445, -78.687043, 1000)
	new_api.get_data()

