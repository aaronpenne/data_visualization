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


output_dir = os.path.relpath('output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
output_dir_raw = os.path.join('output', '_raw')
if not os.path.isdir(output_dir_raw):
    os.mkdir(output_dir_raw)

output_dir_gif = os.path.join('output', '_gif')
if not os.path.isdir(output_dir_gif):
    os.mkdir(output_dir_gif)

output_dir_mp4 = os.path.join('output', '_mp4')
if not os.path.isdir(output_dir_mp4):
    os.mkdir(output_dir_mp4)

def bulk_download(args):
    try:
        root_url = args[0]
        image_date = args[1]
        image_date_clean = image_date.replace('.', '')
        
        image_files = [f for f in os.listdir(output_dir_raw) if image_date_clean in f and f.endswith('jpg')]
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
        image_download(evi_url, evi_out)
        
        ndvi_url = image_dir_url + '/' + ndvi
        ndvi_out = 'mod13ci_006_ndvi_' + image_date_clean + '.jpg'
        image_download(ndvi_url, ndvi_out)
    except:
        print('Download: {}'.format(image_dir_url))

def image_download(img_url, img_out):
    image = requests.get(img_url).content
    with open(os.path.join(output_dir_raw, img_out), 'wb') as f:
        f.write(image)
        
def bulk_annotate(image_file):
    try:
        image_files = [f for f in os.listdir(output_dir_mp4) if image_file in f and f.endswith('jpg')]
        if image_files:
            return
        
        image = Image.open(os.path.join(output_dir_raw, image_file))
        
        # Make the ocean black \m/
        image_rgba = image.convert('RGBA')
        data = np.array(image_rgba)
        r, g, b, a = data.T
        ocean = (r<50) & (b<160) & (b>50)
        data[..., :-1][ocean.T] = (0, 0, 0)
        image = Image.fromarray(data)
        image = image.convert('RGB')
        
        draw = ImageDraw.Draw(image)
        
        # Add title
        title = 'Enhanced Vegetation Index (EVI) from 2000-2018'
        consolas_centered(draw, title, (7200, 3150), 117)      
        
        # Add dates
        image_date = datetime.strptime(image_file[-12:-4], '%Y%m%d').date()
        date_string = image_date.strftime('%m/%Y')
        consolas_centered(draw, date_string, (7200, 3300), 117)
        
        # Add name and source
        annotation = 'GIF by Aaron Penne © 2018\nData: NASA MODIS/Terra Vegetation Indices (MOD13C1)\nSource Code: github.com/aaronpenne'
        font = ImageFont.truetype('Consolas.ttf', 50)
        draw.text((200, 3300), annotation, (177,177,177), font=font)
#        
        # Add slider/text to images
        image.save(os.path.join(output_dir_mp4, 'text_' + image_file),)
    except:
        print('Annotate: {}'.format(image_file))

def bulk_resize(image_file):
    try:
        image_files = [f for f in os.listdir(output_dir_gif) if image_file in f and f.endswith('jpg')]
        if image_files:
            return
        image = Image.open(os.path.join(output_dir_mp4, image_file))
        image.size
        image = image.resize((1903, 978), Image.ANTIALIAS)
        image.save(os.path.join(output_dir_gif, 'small_' + image_file))    
    except:
        print('Resize: {}'.format(image_file))

def consolas_centered(draw, text, coords=(0,0), size=17):
    font = ImageFont.truetype('Consolas.ttf', size)
    W, H = coords
    w, h = draw.textsize(text, font=font)
    x = (W-w)/2
    y = H
    draw.text((x, y), text, (255,255,255), font=font)

if __name__ == '__main__':
    
    root_url = 'https://e4ftl01.cr.usgs.gov/MOLT/MOD13C1.006/' 
    root_page = requests.get(root_url)
    root_contents = html.fromstring(root_page.content)
    links = root_contents.xpath('//a/@href')
    
    # Download all images from each image dir in the root dir on the remote server
    image_dates = [i[:-1] for i in links[7:]]
    with Pool(10) as p:
        p.map(bulk_download, zip(itertools.repeat(root_url), image_dates))
    
    # Annotate images
    image_files = [f for f in os.listdir(output_dir_raw) if 'evi' in f and f.endswith('jpg')]
    image_files.sort()
    with Pool(10) as p:
        p.map(bulk_annotate, image_files)
#    bulk_annotate(image_files[0])

    # Create downsampled copies of images
    image_files = [f for f in os.listdir(output_dir_mp4) if 'evi' in f and f.endswith('jpg')]
    image_files.sort()
    with Pool(10) as p:
        p.map(bulk_resize, image_files)
    
    # Create downsized gif
    image_files = [f for f in os.listdir(output_dir_gif) if 'small' in f and f.endswith('jpg')]
    image_files.sort()
    image_list = []
    for f in image_files:
        image = imageio.imread(os.path.join(output_dir_gif, f))
        image_list.append(image)
    imageio.mimsave(os.path.join(output_dir, 'animation_evi.gif'), image_list, format='GIF', duration=0.2)
    
    # Create full size movie
    image_files = [f for f in os.listdir(output_dir_mp4) if 'text' in f and f.endswith('jpg')]
    image_files.sort()
    image_list = []
    for f in image_files:
        image = imageio.imread(os.path.join(output_dir_mp4, f))
        image_list.append(image)
    imageio.mimsave(os.path.join(output_dir, 'animation_evi.mp4'), image_list, format='MP4', fps=5)
    


    
    # FIXME:
    # Replace blue in ocean with black
    # DO it all again for NDVI for comparison
    # Do zoom continents/countries
    # Do do all Dec and Jul for YOY comparison
