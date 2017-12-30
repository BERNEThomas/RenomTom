#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable
import os
import string
import sys
import codecs
from Classes import *
from Fenetre import *

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
renomTom = Executable("RenomTom.py", 
	base="Win32GUI",
	targetName="RenomTom v2.0.exe")
setup(
	name = "RenomTom",
	version = "2.0",
	author = "Thomas BERNE",
	author_email = "contact@bernethomas.net",
	description = "Application de renommage de répertoires.",
	options = {"build_exe": {"packages":["sys", "codecs", "tkinter", "datetime"],
		'include_files':[
			os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
			os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
				"Fenetre.py", "Classes.py", "RenomTom_sauvegarde.ini"
			]}},
	executables = [renomTom],
	icon = os.path.join("gui", ""))

Fenetre().mainloop()
