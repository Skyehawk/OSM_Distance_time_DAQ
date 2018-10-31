import simplejson
import time
import urllib.request, urllib.parse, urllib.error
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('output')
args = parser.parse_args()
with open(args.filename) as file:
	team_loc = pd.read_csv(file)
	team_loc.columns = ['team', 'lat', 'lon']
	print(team_loc.head())

	df_log = pd.DataFrame(columns=['team_number', 'orgin_lat', 'orgin_lon', 'dest_lat', 'dest_lon', 'dist_m', 'time_s'])
	dest_coord = "-83.045833,42.331389"															# {longitude,latitude}

for index, row in team_loc.iterrows():
	attp = 0
	while attp <= 4:																			# Take 5 attempts at this URL
		try:
			time.sleep(np.random.randint(4, size=1) + 1.5)										# Don't hit the server too fast, be nice
			url = "http://router.project-osrm.org/route/v1/driving/{0};{1}?overview=false".format(str(row['lon']) + "," + str(row['lat']),str(dest_coord))
			print("url:", url)
			opener = urllib.request.build_opener()
			opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
			result = simplejson.load(opener.open(url))
			df_log.loc[-1] = [row['team'], row['lat'], row['lon'], 42.331389,-83.045833, result['routes'][0]['distance'], result['routes'][0]['duration']]
			print ('Info:', df_log.loc[[-1]],'\n<---------->')
			df_log.index = df_log.index + 1
			pass
		except Exception as e:
			print(e)
			attp += 1																			# index +1 on our 5 attempts at this URL
			time.sleep(10)
			continue
		break
	
print('LOG:', df_log)
df_log.to_csv(args.output)
