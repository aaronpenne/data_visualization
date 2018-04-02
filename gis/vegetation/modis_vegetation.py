# -*- coding: utf-8 -*-
"""
Author: Aaron Penne
Created: 2018-03-29

Developed with:
    Python 3.6
    macOS 13.3
"""

import numpy as np

from PIL import Image, ImageDraw, ImageFont
import imageio

from datetime import datetime
import os

from multiprocessing.dummy import Pool
import itertools

from lxml import html
import requests


# DEBUG
DEBUG = 1

# Params
fps = 5
legend_bounding_box = [3400, 2500, 3800, 2900]

def init_dir(dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    return dir_name
    
dir_output = init_dir(os.path.relpath('output'))
dir_raw = init_dir(os.path.join('output', '_raw'))
dir_small = init_dir(os.path.join('output', '_small'))
dir_large = init_dir(os.path.join('output', '_large'))

# FIXME do dynamically
dir_na = init_dir(os.path.join('output', '_north_america'))

def get_vegetation_images(args):
    try:
        root_url = args[0]
        image_date = args[1]
        image_date_clean = image_date.replace('.', '')

        image_files = [f for f in os.listdir(dir_raw) if image_date_clean in f and f.endswith('jpg')]
        if image_files:
            return

        image_dir_url = root_url + image_date
        image_dir_page = requests.get(image_dir_url)
        image_dir_contents = html.fromstring(image_dir_page.content)
        links = image_dir_contents.xpath('//a/@href')
        evi = links[7]
        ndvi = links[8]

        evi_url = image_dir_url + '/' + evi
        evi_out = 'mod13ci_006_evi_' + image_date_clean + '.jpg'
        download_image(evi_url, evi_out)

        ndvi_url = image_dir_url + '/' + ndvi
        ndvi_out = 'mod13ci_006_ndvi_' + image_date_clean + '.jpg'
        download_image(ndvi_url, ndvi_out)
    except:
        print('Download: {}'.format(image_dir_url))

def download_image(img_url, img_out):
    image = requests.get(img_url).content
    with open(os.path.join(dir_raw, img_out), 'wb') as f:
        f.write(image)

def annotate_image(image_file):
    try:
#        image_files = [f for f in os.listdir(dir_large) if image_file in f and f.endswith('jpg')]
#        if image_files:
#            return

        image = Image.open(os.path.join(dir_raw, image_file))

        # Make the ocean black \m/
        image_rgba = image.convert('RGBA')
        data = np.array(image_rgba)
        r, g, b, a = data.T
        ocean = (r<50) & (b<160) & (b>50)
        data[..., :-1][ocean.T] = (33, 33, 33)
        image = Image.fromarray(data)
        image = image.convert('RGB')

        draw = ImageDraw.Draw(image)

        # Add title (pad first)
        if veg_index == 'evi':
            title = 'Enhanced Vegetation Index (EVI)\nCollected by MODIS on NASA\'s Terra Satellite'
        elif veg_index == 'ndvi':
            title = 'Normalized Difference Vegetation Index (NDVI)\nCollected by MODIS on NASA\'s Terra Satellite'
        consolas_centered(draw, title, [0, 3100, 7200, 3350], 117, spacing=60)

        # Add dates (add circle, etc)
        box = legend_bounding_box
        image_date = datetime.strptime(image_file[-12:-4], '%Y%m%d').date()
        doy = int(image_date.strftime('%j'))
        theta = (doy / 365 * 360) - 90
        draw.pieslice(box, 270, theta, fill=(50,50,50))
        draw.ellipse(box, outline=(100,100,100))
        
        # Months
        font = ImageFont.truetype('Consolas.ttf', 50)
        pad = 20
        x1, y1, x2, y2 = box
        fill = (200,200,200)
        
        month = 'JAN'
        w, h = draw.textsize(month, font=font)
        draw.text((int((x2-x1-w)/2+x1), y1-h-pad), month, fill, font=font)
        
        month = 'APR'
        w, h = draw.textsize(month, font=font)
        draw.text((x2+pad, int((y2-y1-h)/2+y1)), month, fill, font=font)
        
        month = 'JUL'
        w, h = draw.textsize(month, font=font)
        draw.text((int((x2-x1-w)/2+x1), y2+pad), month, fill, font=font)
        
        month = 'OCT'
        w, h = draw.textsize(month, font=font)
        draw.text((x1-w-pad, int((y2-y1-h)/2+y1)), month, fill, font=font)
        
                
        image_date = datetime.strptime(image_file[-12:-4], '%Y%m%d').date()
        date_string = image_date.strftime('%Y')
        consolas_centered(draw, date_string, legend_bounding_box, 100, (200,200,200))

        # Add notes
        if veg_index == 'evi':
            annotation = '\"EVI improves on NDVI\'s spatial resolution, is more\nsensitive to differences in heavily vegetated areas,\nand better corrects for atmospheric haze as well as\nthe land surface beneath the vegetation.\" - NASA'
            font = ImageFont.truetype('Consolas.ttf', 50)
            draw.text((100, 3150), annotation, (177,177,177), font=font, spacing=20, align='left')

        # Add name and source
        annotation = 'Imagery Products: MODIS Science Team\nData: NASA MODIS Vegetation Indices (MOD13C1)\nSource Code: www.github.com/aaronpenne\nGIF: Aaron Penne © 2018'
        w, h = draw.textsize(annotation, font=font)
        font = ImageFont.truetype('Consolas.ttf', 50)
        draw.text((7100-w, 3150), annotation, (177,177,177), font=font, spacing=20, align='right')

        image.save(os.path.join(dir_large, 'text_' + image_file),)
    except:
        print('Annotate: {}'.format(image_file))

def resize_image(image_file):
    try:
#        image_files = [f for f in os.listdir(dir_small) if image_file in f and f.endswith('jpg')]
#        if image_files:
#            return
        
        image = Image.open(os.path.join(dir_large, image_file))
        image.size
        image = image.resize((1903, 978), Image.ANTIALIAS)
        image.save(os.path.join(dir_small, 'small_' + image_file))
    except:
        print('Resize: {}'.format(image_file))
        
def crop_image(args):
    image_dir = args[0]
    image_file = args[1]
    coords = args[2]
    
    image = Image.open(os.path.join(image_dir, image_file))
    image = image.crop(coords)
    image.save(os.path.join(dir_na, 'na_' + image_file))

def consolas_centered(draw, text, box=[0, 0, 1000, 1000], size=17, color=(255,255,255), spacing=0):
    font = ImageFont.truetype('Consolas.ttf', size)
    w, h = draw.textsize(text, font=font)
    x = (box[2] - box[0])/2 + box[0] - w/2
    y = (box[3] - box[1])/2 + box[1] - h/2
    draw.text((x, y), text, color, font=font, spacing=spacing, align='center')
    
def get_image_files(image_dir, text='', shortened=0):
    image_files = [f for f in os.listdir(image_dir) if f.endswith('jpg') and text in f]
    image_files.sort()
    
    # Reduce number of files for debugging purposes
    if shortened:
        image_files = image_files[364:410]
    return image_files
    
if __name__ == '__main__':
    
    for veg_index in ['ndvi']:
        
        root_url = 'https://e4ftl01.cr.usgs.gov/MOLT/MOD13C1.006/'
        root_page = requests.get(root_url)
        root_contents = html.fromstring(root_page.content)
        links = root_contents.xpath('//a/@href')
    
        print('Downloading images from {}'.format(root_url))
        image_dates = [i[:-1] for i in links[7:]]
        with Pool(10) as p:
            p.map(get_vegetation_images, zip(itertools.repeat(root_url), image_dates))
    
        print('Annotating images...')
        image_files = get_image_files(dir_raw, veg_index, DEBUG)
        with Pool(10) as p:
            p.map(annotate_image, image_files)
    
        print('Shrinking images...')
        image_files = get_image_files(dir_large, veg_index)
        with Pool(10) as p:
            p.map(resize_image, image_files)
    
        # Create downsized gif
        image_files = get_image_files(dir_small, veg_index)
        image_list = []
        for f in image_files:
            image = imageio.imread(os.path.join(dir_small, f))
            image_list.append(image)
        imageio.mimsave(os.path.join(dir_output, 'animation_' + veg_index + '.gif'), image_list, format='GIF', duration=1/fps)
    
        # Create full size movie
#        image_files = get_image_files(dir_large)
#        image_list = []
#        for f in image_files:
#            image = imageio.imread(os.path.join(dir_large, f))
#            image_list.append(image)
#        imageio.mimsave(os.path.join(dir_output, 'animation_' + veg_index + '.mp4'), image_list, format='MP4', fps=fps)
#    
        # Create North America zoom
#        image_files = get_image_files(dir_large)
#        with Pool(10) as p:
#            p.map(crop_image, zip(itertools.repeat(dir_large), image_files, itertools.repeat((150, 150, 2635, 1690))))
#            
#        image_files = get_image_files(dir_na)
#        image_list = []   
#        for f in image_files:      
#            image = imageio.imread(os.path.join(dir_na, f))
#            image_list.append(image)
#        imageio.mimsave(os.path.join(dir_output, 'animation_' + veg_index + '_na.mp4'), image_list, format='MP4', fps=fps)
#    
