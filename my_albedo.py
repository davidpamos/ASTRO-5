#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 20:42:06 2022

@author: Astro5
"""

import imageio
import numpy as np
import os
import pandas as pd



path = './images_albedo/'

def analyse_image(image):
    pic = imageio.imread(image)
    #plt.figure(figsize = (5,5))
    #plt.imshow(pic)
    
    cropped_pic = pic[300:1700,750:1750]
    #plt.imshow(cropped_pic)
    
    red_pixels = cropped_pic[:, :, 0] > 220
    green_pixels = cropped_pic[:, :, 1] > 220
    blue_pixels = cropped_pic[:, :, 2] > 220
    
    mask_ocean_red = np.logical_and(cropped_pic[:, :, 0]> 0, cropped_pic[:, :, 0] <100)
    mask_ocean_green = np.logical_and(cropped_pic[:, :, 1]> 0, cropped_pic[:, :, 1] <100)
    mask_ocean_blue = np.logical_and(cropped_pic[:, :, 2]> 0, cropped_pic[:, :, 2] <100)
    
    mask_land_red = np.logical_and(cropped_pic[:, :, 0]>100, cropped_pic[:, :, 0] <220)
    mask_land_green = np.logical_and(cropped_pic[:, :, 1]> 100, cropped_pic[:, :, 1] <220)
    mask_land_blue = np.logical_and(cropped_pic[:, :, 2]> 100, cropped_pic[:, :, 2] <220)
    
    mask_final_sky = np.logical_and(red_pixels, green_pixels, blue_pixels)
    mask_final_sea = np.logical_and(mask_ocean_red, mask_ocean_green, mask_ocean_blue)
    mask_final_land = np.logical_and(mask_land_red, mask_land_green, mask_land_blue)
    
    cropped_pic[mask_final_land] = [0, 255, 0]
    cropped_pic[mask_final_sea] = [0, 0, 255]
    cropped_pic[mask_final_sky] = [255, 0, 0]
    
    #plt.imshow(cropped_pic)
    
    total = cropped_pic.shape[0] * cropped_pic.shape[1]
    
    percentage_sea = (np.sum(mask_final_sea)/total)*100
    percentage_sky = (np.sum(mask_final_sky)/total)*100
    percentage_land = (np.sum(mask_final_land)/total)*100
    #print(percentage_sea,percentage_sky,percentage_land)
    
    albedo = percentage_sea*0.10+percentage_land*0.25+percentage_sky*0.70
    albedo = (albedo/100)
    #print(albedo)
    
    return albedo, cropped_pic

def ext(image):
    extension = os.path.splitext(image)
    return extension[0]

all_files = os.listdir()
all_images = []


for file in all_files:
    extension = os.path.splitext(file)
    if extension[1] == ".jpg":
        all_images.append(file)
print(len(all_images))

albedos = []  
images = []
means = []


for image in all_images:
    albe = analyse_image(image)[0]
    treated_image = analyse_image(image)[1]
    albedos.append(albe)
    medium_albedo = np.sum(albedos)/len(albedos)
    means.append(medium_albedo)
    filename = ext(image)
    images.append(filename)
    imageio.imsave(path+filename+'.png',treated_image)

all_albedos = {'Images':images,'Albedos':albedos, 'Mean_Albedo':means}    
all_albedos = pd.DataFrame(all_albedos)
all_albedos = all_albedos.sort_values('Images')
all_albedos.to_csv('results_albedo', sep=' ', index = False)

