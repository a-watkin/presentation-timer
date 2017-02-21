#!/usr/bin/python3
# setup file for presentation timer for use with py2exe by Adam Watkin 
# 2017

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup_dict = dict(
    data_files = [('', ['pt_icon.ico', 'whisky_ding_short2.wav'])],
    options = {'py2exe': 
                        {'bundle_files': 2, 
                        'compressed': True}},
    windows = [{'script': "presentation_timer_10012017.py",
                'icon_resources': [(1, 'pt_icon.ico')],
                'dest_base': 'presentation timer'}],

    zipfile = None,
)
# does this twice to set the icon for the .exe
# this is because of a bug with py2exe
setup(**setup_dict)
setup(**setup_dict)