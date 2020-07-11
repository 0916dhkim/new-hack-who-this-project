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
```

3. Start discord bot server.
```bash
python __main__.py
```

## How to Create a New Command
Let's assume the name of your new command is **foo**.
1. Create `commands/foo.py` file and copy the following into the file.
```python
from discord_client import client
from discord.ext.commands import Context


@client.command()
async def foo(ctx: Context, *args: str):
    pass

```
2. Modify `commands/__init__.py`
    - Add "`from .foo import foo`" to the imports.
    - Add `"foo"` inside `__all__` variable.

3. Implement `foo` function inside `commands/foo.py`

4. Push changes to this GitHub repo.
