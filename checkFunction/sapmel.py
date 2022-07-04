from dis import pretty_flags
from prettytable import PrettyTable
import PySimpleGUI as sg
import prettytable
import subprocess
import netifaces
import re

lst = []

for i in range(3):
    lst.append([])
    for j in range(3):
        lst[i].append(j)

print(lst)
