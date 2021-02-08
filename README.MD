# Zotero-Notion

![GitHub top language](https://img.shields.io/github/languages/top/reycn/notion-zotero)
![License](https://img.shields.io/badge/license-MIT-000000.svg)  
Sync Zotero library to Notion and cite them.  
## Showcase
- Cite an item:
![](https://i.imgur.com/LnMNtxJ.png)
- Database (*A.K.A. collection*):
![](https://i.imgur.com/dUfrtmR.png)

## Necessary Configuration
```
[notion]
PAGE_URL = Target Notion Page Address
CV_URL = Target Notion CV (Collection View)
TOKEN_V2 = Notion Access Token (the second version)

[zotero]
LIBRARY_ID = Library ID of Target Zotero Library
LIBRARY_TYPE = Type of Target Zotero Library, user or group
API_KEY= Zotero API Key
```

- Find Notion [`TOKEN_V2`](https://www.google.com/search?q=get+notion+tokenv2)  
- Get Zotero [`API_KEY`](https://www.zotero.org/settings/keys)

## Requirements
- Python >= 3.7
- Pyzotero
- notion_py (**ATTENTION: only use [this fork version](https://github.com/arturtamborski/notion-py), plz**)
- pandas
- notion
- rich

## Run 
`python3 main.py`

## Todo
- Robustness improvements