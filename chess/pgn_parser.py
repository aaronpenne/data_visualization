# -*- coding: utf-8 -*-
"""
Simple PGN parser which converts

Author: Aaron Penne
Created: 2018-03-07

Developed with:
    Python 3.6
    Windows 10
    
PGN game format
    [Event "New Orleans"]
    [Site "New Orleans"]
    [Date "1866.??.??"]
    [Round "?"]
    [White "Morphy, Paul "]
    [Black "Maurian, Charles Amedee"]
    [Result "1-0"]
    [WhiteElo ""]
    [BlackElo ""]
    [ECO "C37"]
    
    1.e4 e5 2.f4 exf4 3.Nf3 g5 4.Bc4 g4 5.d4 gxf3 6.Qxf3 d6 7.O-O Be6 8.d5 Bc8
    9.Bxf4 Qd7 10.e5 Qg4 11.Qe3 Be7 12.exd6 cxd6 13.Re1 h5 14.Bxd6 Qd7 15.Bxe7 Nxe7
    16.Bb5  1-0


Output format(ish)
    color | move_num | square | piece | event | site | date | match_round | player | result | elo | eco
    
"""

import os
import numpy as np
import re

input_dir = os.path.relpath('data')
output_dir = os.path.relpath('output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
    
# All possible chess squares
all_squares = []
for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
    for j in np.linspace(1, 8, 8):
        all_squares += ['{}{}'.format(i, int(j))]
    
    # Get list of all PGN files in data dir
all_pgn_files = [f for f in os.listdir(input_dir) if f.endswith('.pgn')]

for pgn_file in all_pgn_files:
    # Read single PGN file into a list
    with open(os.path.join(input_dir, pgn_file)) as f:
        content = f.readlines()
        
    # Remove leading and trailing whitespace
    content = [x.strip() for x in content]
    
    # Remove empty lines
    content = list(filter(None, content))
    
    for i, line in enumerate(content):
        
        # FIXME use regex instead 
        # FIXME deal with empty values
        # Get game metadata
        if 'Event ' in line:
            event = line[8:-2].strip()
        elif 'Site ' in line:
            site = line[7:-2].strip()
        elif 'Date ' in line:
            date = line[7:-2].strip()
        elif 'Round ' in line:
            match_round = line[8:-2].strip()
        elif 'White ' in line:
            white = line[8:-2].strip()
        elif 'Black ' in line:
            black = line[8:-2].strip()
        elif 'Result ' in line:
            result = line[9:-2].strip()
        elif 'WhiteElo ' in line:
            white_elo = line[11:-2].strip()
        elif 'BlackElo ' in line:
            black_elo = line[11:-2].strip()
        elif 'ECO' in line:
            eco = line[6:-2].strip()
        
        # If not game metadata, then it's most likely a line with moves
        elif '.' in line:
            line_moves = line.split()
            
            check = False
            mate = False
            # Loop through each move on this line
            for move in line_moves:
                if move.find('.') > 0:
                    move_num = move[0:move.find('.')]
                    move = move[move.find('.')+1:]
                    color = 'white'
                elif '-' not in move:
                    color = 'black'
                elif '-' in move:
                    break
                elif '+' in move:
                    check = True
                elif '#' in move:
                    mate = True
                    
                
                # FIXME better way to find square? regex?
                
