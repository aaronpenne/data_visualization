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

# Reads in text file containing list of prime numbers, one per line
with open('primes.txt') as file_in:
    primes = file_in.read().splitlines()

# Reshapes primes into square list of lists with one char per entry
for ii in range(rows):
    for jj in range(cols):
        # FIXME

# Print svg metadata
file_out = open('primes.svg', 'w')
file_out.write("<?xml version=\"1.1\" encoding=\"utf-8\"?>\n")
file_out.write("<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n")
file_out.write("<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:space=\"preserve\">\n")

# Prints colors in CSS style block
file_out.write("<style type=\"text/css\" id=\"style_css_sheet\">\n")
for index, color in enumerate(colors):
    file_out.write('\t.class_{0:d} {{fill:#{1:s}}}\n'.format(index, color))
file_out.write("</style>\n")


# Prints one line per digit

file_out.write("</svg>\n")
file_out.close()