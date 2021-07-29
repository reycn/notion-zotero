# Zotero-Notion

![GitHub top language](https://img.shields.io/github/languages/top/reycn/notion-zotero)
![License](https://img.shields.io/badge/license-MIT-000000.svg)  
[![zotero-to-notion](https://github.com/magicgh/zotero-notion/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/magicgh/zotero-notion/actions/workflows/main.yml)
Create a Notion collection, synced with Zotero **automatically by GitHub Actions**.

## Get Started

Setting up secrets below:

```
PAGE_URL = Target Notion Page Address
CV_URL = Target Notion CV (Collection View)
TOKEN_V2 = Notion Access Token (the second version)
LIBRARY_ID = Library ID of Target Zotero Library
LIBRARY_TYPE = Type of Target Zotero Library, user or group
API_KEY= Zotero API Key
```

- Find Notion [`TOKEN_V2`](https://www.google.com/search?q=get+notion+tokenv2)  
- Get Zotero [`API_KEY`](https://www.zotero.org/settings/keys)
- Create GitHub [`Secrets`](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository)

Customize a cron schedule  
`.github/workflows/main.yml`

```yaml
  schedule:
    - cron: "0 */12 * * *"
```

## Requirements

- Python >= 3.7
- Pyzotero
- notion_py (**ATTENTION: only use [this fork version](https://github.com/arturtamborski/notion-py), plz**)
- pandas
- notion
- rich

## Todo

- Robustness improvements
