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
    PAGE_URL = sys.argv[1]
    CV_URL = sys.argv[2]
    TOKEN_V2 = sys.argv[3]
    LIBRARY_ID = int(sys.argv[4])
    LIBRARY_TYPE = sys.argv[5]
    API_KEY = sys.argv[6]

except Exception as e:
    CONSOLE.print('No arguments detected, exit...', style='bold red')
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


def set_row_props(row, title: str, authors: str, year: list, url: str, key: str, version: int) -> None:
    # row = cv.collection.get_rows(search=key)[0]
    try:
        row.title = title
        row.authors = ', '.join(authors) if len(authors) > 0 else authors
        row.year = year
        row.url = url
        row.key = key
        row.version = str(version)
        CONSOLE.print(f'Row {str(row)} edited', style="bold green")
    except Exception as e:
        CONSOLE.print(f'Row {str(row)} edit failed:\n{e}', style="bold red")


def add_notion_row(cv: NotionClient, title: str, authors: str,
                   year: list, url: str, key: str, version: int) -> None:
    if not isinstance(title, str):
        return
    if len(cv.collection.get_rows(search=key)) > 0:
        try:
            row = cv.collection.get_rows(search=key)[0]
            if int(row.version) >= version:
                pass
            else:
                set_row_props(row, title, authors, year, url, key, version)
                
        except:
            CONSOLE.print(
                'Errors occurred when getting specific row, adding inseead...',
                style="bold red")
            row = cv.collection.add_row()
            set_row_props(row, title, authors, year, url, key, version)
    else:
        row = cv.collection.add_row()
        set_row_props(row, title, authors, year, url, key, version)


# MAIN #
def main() -> None:
    init()
    df = fetch_zotero_items(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
    data = extrtact_data(df)
    for item in data.items():
        add_notion_row(CV, item[1]['title'], item[1]['authors'], item[1]['year'], item[1]['url'], item[1]['key'], item[1]['version'])


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
