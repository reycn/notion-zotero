from pyzotero import zotero
import pandas as pd
import re

def list_strip(lst: list) -> list:
    for i in range(len(lst)):
        lst[i] = lst[i].strip().replace('   ',' ').replace('  ',' ')
    return lst

def creators_to_names(names_lst: list) -> list:
    if type(names_lst) != float:
        tmp = pd.DataFrame(names_lst).fillna('')
        for col in ['name', 'firstName', 'middleName', 'lastName']:
            if col not in tmp.columns:
                tmp[col] = ''
        tmp['author'] = tmp['name'] + ' ' + tmp['firstName'] + ' ' + tmp['middleName'] + ' ' +  tmp['lastName']
        tmp.apply(lambda x: list_strip(x))
        return tmp.author.to_list()
    else:
        return ['Anonymous']

def extrtact_data(df: pd.DataFrame) -> pd.DataFrame:
    # df = df[df['itemType'] != 'attachment'].copy()
    df['authors'] = [ creators_to_names(i) for i in df.creators]
    df['year'] = df.date.apply( lambda x: re.search(r'([0-9]{4})', str(x)).group(1) if re.search(r'([0-9]{4})', str(x)) else '*' )
    data = df[df['itemType'] != 'attachment'][['title', 'authors', 'year', 'url', 'key', 'version']].T.to_dict()
    return data

def fetch_zotero_items(LIBRARY_ID: int, LIBRARY_TYPE: str, API_KEY: str) -> pd.DataFrame:
    lib = zotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
    items = lib.items()
    try:
        df = pd.DataFrame(pd.DataFrame(items)['data'].to_list())
    except Exception as e:
        print('Error:' + str(e))
    return df


# if __name__ == '__main__':
    
#     try:
#         print('Start running...')
#         df = fetch_zotero_items(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
#         data = extrtact_data(df)
#         for item in data.items():
#             print(item[1]['title'])
#     except KeyboardInterrupt as k:
#         print('\nKey pressed to interrupt...')

