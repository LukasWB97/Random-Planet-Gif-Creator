from PIL import Image
from random import random
import numpy as np
import colorsys
import time
import numpy as np
import imageio
from biome import create_map




camera = [0,0,0,0,0] #x,y,z, theta, phi
c_range = [180,180] #theta, phi



#Canvas dims
height = 350
width  = 350


canvas_front = [(255,255,255)] * height * width #blank canvas
canvas_back = [(255,255,255)] * height * width #blank canvas


radius = 150
lthickness = 500
img_front = Image.new(mode='RGBA', size=(width, height))


#maps = create_map(10)
maps = [Image.open('earthtest.png')]


rotation_res = 360

for j,map_i in enumerate(maps):
	map = map_i.convert('RGB')




	res = map_i.size[0]/360




	for offset in range(rotation_res):
		for theta in range(int(180 * res)):
			for phi in range(int(180 * res)):
				tr = theta/res * np.pi/180.0
				#theta = np.pi/2
				
				pr = phi/res  * np.pi/180.0
				

				#phi = np.pi / 2
				x = int(radius*np.cos(tr))
				xy = int(np.sin(tr) * 1)
				y = int(radius*np.cos(pr))
				yy = np.sin(pr)
				

				
				
				if x**2 + y**2  <= radius**2:
					mapcolor = map.getpixel(((theta + offset * res * 360 / rotation_res) % map_i.size[0], phi))
					#mapcolor = (255, 255, 255)
					final_color = tuple([int(mc * yy) for mc in mapcolor])
				
					canvas_front[int((x + width/2)+ (y + height/2)*width)] =  final_color
		print('\r{0}/{1} Completed '.format(offset+1, rotation_res), end="", flush=True)
		
				
			
			
		img_front.putdata(canvas_front)
		#img_front.show()
		img_front.save("Rotating/sphere{0}.png".format(offset))
		
	print()

	images = []
	for i in range(rotation_res):
		images.append(imageio.imread("Rotating/sphere{0}.png".format(i)))
	imageio.mimsave('rotating{0}.gif'.format(j), images, duration=0.005)
	print('Finished rotating gif {0}'.format(j))
	print()
