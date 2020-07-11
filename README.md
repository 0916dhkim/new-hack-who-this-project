# New Hack, Who This : Discord Bot
Music AI

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
