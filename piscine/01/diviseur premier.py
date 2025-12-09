# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 08:33:15 2025

@author: samya.taqi
"""

#nombre premier 
n=int(input("entrez un nombre n : "))
nb_diviseur=0
for i in range(2,n):
    if n%i==0:
        nb_diviseur=nb_diviseur+1
        print(i)
        
if nb_diviseur==0:
    print("premier")
else:
    print("pas premier")
        