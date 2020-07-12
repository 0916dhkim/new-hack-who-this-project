# New Hack, Who This : Discord Bot
Music AI

## How to Run

1. Create a virtual environment & install dependencies.
```bash
python -m venv venv

# Windows
venv/Scripts/activate
# MacOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

2. Put required environment variables in `.env` file.
```
BOT_PREFIX="!"
BOT_TOKEN="XXXXXXXXXXXXXX"
SPOTIFY_CLIENT_ID="XXXXXXXXXXXXXX"
SPOTIFY_CLIENT_SECRET="XXXXXXXXXXXXXX"
LASTFM_API_KEY="XXXXXXXXXXXXXX"
LASTFM_API_SECRET="XXXXXXXXXXXXXX"
```

3. Start discord bot server.
```bash
python __main__.py
```

## How to Scrape Music Metadata
```bash
python scrape.py
```

## Using the Jupyter Notebook 
1. `jupyter notebook`
2. In the browser window opened after above command, select the 'Data Labelling.ipynb' file
3. Run all the cells in the notebook to see the result.

## Copyright/Reference
Music playback functionality is taken from this gist:
<https://gist.github.com/vbe0201/ade9b80f2d3b64643d854938d40a0a2d>

