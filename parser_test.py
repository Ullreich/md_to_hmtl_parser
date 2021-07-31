#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 17:17:30 2021

@author: ferdinand
"""

import objects_for_parser as ofp

filename = "TODO.md"
file = open(filename, "r")


'''
while True:
    char  = file.read(1)
    
    if not char:
        break
    
    if char == "\n":
        print('newline')
    elif char == "\t":
        print('tab')
    elif char == " ":
        print('space')
    else:
        print(char)
    
    
file.close()
'''

charread = ofp.CharacterReader(file.read())
#charread._print()

tokens = ofp.Lexer(charread)
tokens.tokenize()
tokens._print()

parse = ofp.Parser("parse", tokens)
parse.parse()