from noise import pnoise3
from PIL import Image
from random import random
import numpy as np
import colorsys



tile_size_x = 1
tile_size_y = 1



x_length = 1028
y_length = 1028
freqx = 1028
freqy = 1028
octaves = 10
lacunarity = 2.0
persistence = 0.5
seed = 0

mode = 0

def create_map(num_maps, save=False):
	maps = []
	for r in range(num_maps):
		
		seedh = random() * freqx
		seedoff = random() * freqx
		seedhumid = random()*freqx
		seedt = random() * freqx
		
		seedhmn = random() * freqx
		seedhmx = random() * freqx
		
		offset = [[int((pnoise3(i / freqx, j / freqy, seedoff, 2, repeatx=1, repeaty=1, lacunarity=5.0)+1)/2 * 32) for i in range(x_length)] for j in range(y_length)]
		
		
		hmax = [[int((pnoise3(i / freqx, j / freqy, seedhmx, 1, repeatx=1, repeaty=1, persistence=0.25)+1)/2 * 128 + 128) for i in range(x_length)] for j in range(y_length)]
		hmin = [[int((pnoise3(i / freqx, j / freqy, seedhmn, 1, repeatx=1, repeaty=1, persistence=0.25)+1)/2 * 128) for i in range(x_length)] for j in range(y_length)]
		
		#print(lac[0])

		
		humidity = [[round((pnoise3(i / freqx, j / freqy, seedhumid, 3, repeatx=1, repeaty=1, lacunarity=2.0)+1)/2,4) for i in range(x_length)] for j in range(y_length)]
		temperature = [[round((pnoise3(i / freqx, j / freqy, seedt, 4, repeatx=1, repeaty=1, lacunarity=2.0)+1)/2, 4) for i in range(x_length)] for j in range(y_length)]
		
		
		
		ht_list = [[temperature[j][i] *humidity[j][i] for i in range(x_length)] for j in range(y_length)]
				
		
		
		ht_min = min(map(min, ht_list))
		ht_max = max(map(max, ht_list))
		
		
		tmin = min(map(min, temperature))
		tmax = max(map(max, temperature))
		
		hummin = min(map(min, humidity))
		hummax = max(map(max, humidity))


		
		
		heightmap = [[int(256 * ((pnoise3(i / freqx, j / freqy, seedh, octaves, repeatx=1, repeaty=1, lacunarity=3.0, persistence=0.5)+1)/2 * 256 - hmin[j][i])/(hmax[j][i] - hmin[j][i]) - offset[j][i]) for i in range(x_length)] for j in range(y_length)]


		height_min = min(map(min, heightmap))
		height_max = max(map(max, heightmap))
		
		print("Heights: ", height_min, height_max)
		print("Humidity: ", hummin, hummax)
		print("Temperature: ", tmin, tmax)
		
		htmap = []
		satelite = []
		
		mins = 0
		for hy in range(y_length):
			for hx in range(x_length):
			
			
				v = heightmap[hy][hx] 
				t = (np.log(temperature[hy][hx]) - np.log(tmin))/(np.log(tmax) - np.log(tmin))
				hd = (np.log(humidity[hy][hx]) - np.log(hummin))/(np.log(hummax)-np.log(hummin))
				ht = (np.log(ht_list[hy][hx]) - np.log(ht_min))/(np.log(ht_max)-np.log(ht_min))
				#ht = ht_list[hy][hx]
				s = hd
				h = 1/3
			
				#if v > 150:
				#	s = 0
				
				#print(h, ht)
				
				if v <= 100 and v > 98: 
					ht = 1
					s = 0
					v = 0
				elif v <= 98:
					h = 2/3
					s = 1
					t = 1/3
				if v % 16 == 0:
					s = 0
					v = 0
				colorht = (int(256 * t), int(256 * hd), 0)
				colorv = colorsys.hsv_to_rgb(0, 1, v)
				
				colorfinal = [(colorht[i] + colorv[i])/2 for i in range(3)]
			
				


				
				if v > 100:
					h = 1/3
				elif v <= 100 and v > 98: 
					h = 0
					s = 0
					v = 0
				elif v <= 98:
					h = 2/3
					
					
				if v % 16 == 0:
					h = 0
					s = 0
					v = 0
				
				# if round(t * 100,1) % 5 == 0:
					# h = 0
					# s = 1 * (t - tmin)/(tmax-tmin)
					# v = 255
				# if round(hd * 100,1) % 5 == 0:
					# h = 2/3
					# s = 1 
					# v = 255 * (hd-hummin)/(hummax-hummin)
				colors = colorsys.hsv_to_rgb(h, s, v)
				
				htmap.append(tuple([int(i) for i in colorfinal]))
				satelite.append(tuple([int(i) for i in colors]))
		#print(mins)
	
		imght = Image.new(mode='RGBA', size=(x_length, y_length))
		imght.putdata(htmap)
		imght = imght.transform((x_length * tile_size_x, y_length * tile_size_y), Image.EXTENT, data=(0,0,x_length , y_length ))
		
		
		imgs = Image.new(mode='RGBA', size=(x_length, y_length))
		imgs.putdata(satelite)
		imgs = imgs.transform((x_length * tile_size_x, y_length * tile_size_y), Image.EXTENT, data=(0,0,x_length , y_length ))
		if save:
			imght.save('Landscapes/{0} - landscapeht.png'.format(r))
			imgs.save('Landscapes/{0} - landscape.png'.format(r))
		print("Round {0} completed".format(r + 1))
		maps.append(imgs)
	return maps
