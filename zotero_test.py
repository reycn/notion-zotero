#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test for zotero.py functions"""

from configparser import ConfigParser
from rich.console import Console
from sys import path as syspath

from zotero import extrtact_data, fetch_zotero_items

## GET CONFIGURATION ###############################################################################
# GLOBAL VARS #
CONSOLE = Console()
CLIENT, PAGE, CV = None, None, None


try:
    cfg = ConfigParser()
    cfg.read(syspath[0] + '/config.ini')
    PAGE_URL = cfg.get('notion', 'PAGE_URL')
    CV_URL = cfg.get('notion', 'CV_URL')
    TOKEN_V2 = cfg.get('notion', 'TOKEN_V2')
    LIBRARY_ID = int(cfg.get('zotero', 'LIBRARY_ID'))
    LIBRARY_TYPE = cfg.get('zotero', 'LIBRARY_TYPE')
    API_KEY = cfg.get('zotero', 'API_KEY')

except Exception as e:
    CONSOLE.print('Config file error, exit...', style='bold red')
    exit()

try:
    print('Start running...')
    df = fetch_zotero_items(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
    # print(df)
    print(list(df.columns))

    data = extrtact_data(df)
    print(data)
    # for item in data.items():
    #     print(item[1]['title'])
except KeyboardInterrupt as k:
    print('\nKey pressed to interrupt...')
