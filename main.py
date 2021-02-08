import sys
from configparser import ConfigParser
from sys import path as syspath

from notion.client import NotionClient
from rich.console import Console

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

## DEFINE FUNCTIONS ################################################################################
# INITIALIZE #
def init() -> None:
    try:
        global CLIENT, PAGE, CV 
        CLIENT = NotionClient(token_v2=TOKEN_V2)
        PAGE = CLIENT.get_block(PAGE_URL)
        CV = CLIENT.get_collection_view(CV_URL)
    except Exception as e:
        CONSOLE.print(f"Config not valid:\n{e}", style="bold red") 
        sys.exit()


# OPERATIONS #
# def props(cls):   # Check available attributes of a class object, only for testing
#   return [i for i in cls.__dict__.keys()]

def set_row_props(row, author_year:str, title: str, authors: list, year: str, item_type: str, key: str, version: int) -> None:
    # row = cv.collection.get_rows(search=key)[0]
    try:
        row.author_year = author_year
        row.title = title
        row.authors = ', '.join(authors) if len(authors) > 0 else authors
        row.year = year
        row.key = key
        row.item_type = item_type
        row.version = version
        CONSOLE.print(f'Row {str(row)} edited', style="bold green")
    except Exception as e:
        CONSOLE.print(f'Row {str(row)} edit failed:\n{e}', style="bold red")

def add_notion_row(cv: NotionClient, author_year:str, title: str, authors: list, year: str, item_type: str, key: str, version: int) -> None:
    if len(cv.collection.get_rows(search=key)) > 0:
        try:
            row = cv.collection.get_rows(search=key)[0]
            if row.version >= version:
                pass
            else:
                set_row_props(row, author_year, title, authors, year, item_type, key, version)
        except:
            CONSOLE.print('Errors occurred when getting specific row, adding inseead...', style="bold red")
            row = cv.collection.add_row()
            set_row_props(row, author_year, title, authors, year, item_type, key, version)
    else:
        row = cv.collection.add_row()
        set_row_props(row, author_year, title, authors, year, item_type, key, version)

# MAIN #
def main() -> None:
    init()
    df = fetch_zotero_items(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
    data = extrtact_data(df)
    for item in data.items():
        add_notion_row(CV, item[1]['author_year'], item[1]['title'], item[1]['authors'],\
            item[1]['year'], item[1]['itemType'], item[1]['key'], item[1]['version'])



## DEFINE MAIN PROCESS #############################################################################
if __name__ == '__main__':
    CONSOLE.print('Start running...', style="bold green")
    try:
        main()
        # init()
    except KeyboardInterrupt as k:
        CONSOLE.print('\nKey pressed to interrupt...', style="bold blue")
    except Exception as e:
        CONSOLE.print(f'\nUnknown error occurred:\n{e}', style="bold red")
