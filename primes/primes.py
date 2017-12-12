# -*- coding: utf-8 -*-

# Sets up array and circles
rows = 11
cols = 11
radius = 10

# Reference" https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
colors = ['ffffff',  # 0 white
          '3cb44b',  # 1 green
          'ffe119',  # 2 yellow          
          '0082c8',  # 3 blue
          'f58231',  # 4 purple
          '46f0f0',  # 5 cyan
          'f032e6',  # 6 magenta
          'd2f53c',  # 7 lime
          'fabebe',  # 8 pink
          'e6194b'   # 9 red
          ]

# Print svg metadata
output = open('primes.svg', 'w')
output.write("<?xml version=\"1.1\" encoding=\"utf-8\"?>\n")
output.write("<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n")
output.write("<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:space=\"preserve\">\n")

# Prints colors in CSS
output.write("<style type=\"text/css\" id=\"style_css_sheet\">\n")
for color in colors:
    output.write() # FIXME

output.write("</style>\n")


# Prints one line per digit

output.write("</svg>\n")
output.close()