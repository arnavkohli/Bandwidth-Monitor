import json
import urllib.request
import time
import requests

from urllib.request import Request, urlopen


''' 
	
	---> EXTRACTS INFO USING PSUTIL
		---> UPDATES DATA IN ONLINE JSON 

'''

class jsonFile:

	def __init__(self, url):
		self.url = url
		self.v = 1052

	def url(self):
		return self.url

	def contents(self, *args):
		'''
			If no argument is given, 
			returns the data of the
			current instance of the 
			json file.

			If a file path is passed in as
			an arg, returns the data of that
			json file.
		'''
		# headers={'User-Agent': 'Mozilla/5.0'}
		# req = Request(args[0], headers=headers)
		# webpage = urlopen(req)


		if len(args) > 0: 

			# with webpage as url: #urllib.request.urlopen(args[0])
			#     data = json.loads(url.read().decode())
			#     return data

			req = requests.get(args[0])
			return req.json()

		else:
			with urlopen(Request(self.url, headers=headers)) as url:
			    data = json.loads(url.read().decode())
			    return data


	def getValsFrom(self, url, attr):

		''' 
			Takes in a url as 
			param. Specify the details 
			to be extarcted in the attr param. 
			Will fetch the keys along with their
			values and update them in our local
			json file.
		'''

		contents = dict(self.contents(url + str(self.v)))
		print (contents)
		with open(self.url, 'r+') as url:
			url.seek(0)
			updated_data = {}
			for key in attr:

				try:
					updated_data[key] = contents[key]
				except ValueError:
					print ('Cannot find %s in JSON file at: %s' % key, url)

			print ('Adding new data to local file...')
			# print(updated_data)
			json.dump(updated_data, url)
			self.v += 1

			url.truncate()
			print ('Successfully updated data!')

	def link(self, url, attr, delay = 1):

		while True:

			try:
				self.getValsFrom(url, attr)
				time.sleep(delay)

			except KeyboardInterrupt:
				print ('Delinked json files')
				return

if __name__ == '__main__':
	BIN_ID = "5c968b4c9c83133c027be999/"
	PRE = "https://api.jsonbin.io/b/" 
	ONLINE_JSON_URL = PRE + BIN_ID

	LOCAL_JSON_PATH = "data.json"


	onlineJSON = jsonFile(ONLINE_JSON_URL)
	localJSON = jsonFile(LOCAL_JSON_PATH)

	localJSON.link(onlineJSON.url, attr = ['total', 'speed', 'version'])







		