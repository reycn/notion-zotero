from pyzotero import zotero
import pandas as pd
import re

def list_strip(lst: list) -> list:
    for i in range(len(lst)):
        lst[i] = lst[i].strip().replace('   ',' ').replace('  ',' ')
    return lst

def creators_to_names(names_lst: list) -> list:
    if type(names_lst) == list:
        if len(names_lst) > 0:
            tmp = pd.DataFrame(names_lst).fillna('')
            for col in ['name', 'firstName', 'middleName', 'lastName']:
                if col not in tmp.columns:
                    tmp[col] = ''
            tmp['author'] = tmp['name'] + ' ' + tmp['firstName'] + ' ' + tmp['middleName'] + ' ' +  tmp['lastName']
            tmp.apply(lambda x: list_strip(x))
            return tmp.author.to_list()
        else:
            return ['NaN']
    else:
        return ['NaN']

def extrtact_data(df: pd.DataFrame) -> pd.DataFrame:
    # df = df[df['itemType'] != 'attachment'].copy()
    df['authors'] = [ creators_to_names(i) for i in df.creators]
    df['year'] = df.date.apply( lambda x: re.search(r'([0-9]{4})', str(x)).group(1) if re.search(r'([0-9]{4})', str(x)) else '*' )
    # df['author_year'] = df.authors.apply(lambda x: ', '.join(x) if len(x) <= 2 else ', '.join(x[:2]) + ' ...')
    # df['author_year'] = '(' + df['author_year']  + ', ' +  df['year']  + ')'
    data = df[df['itemType'] != 'attachment'][['title', 'authors', 'year', 'itemType', 'key', 'version']].T.to_dict()
    # data = df[['title', 'authors', 'year', 'itemType', 'key', 'version']]
    return data

def fetch_zotero_items(LIBRARY_ID: int, LIBRARY_TYPE: str, API_KEY: str) -> pd.DataFrame:
    lib = zotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
    items = lib.everything(lib.items())
    try:
        df = pd.DataFrame(pd.DataFrame(items)['data'].to_list())
        # print(df)
        return df
    except Exception as e:
        print('Error:' + str(e))
    
