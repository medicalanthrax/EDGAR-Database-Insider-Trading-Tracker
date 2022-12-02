#import PySimpleGUI as sg
from collectLinks import collectLinks
from getDoc import getDoc
from read_data import read_data

links = collectLinks()
for link in links:
    print(link)
    print(read_data(getDoc(link)))
