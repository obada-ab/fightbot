# FightBot

A discord bot that simulates a battle royale game.

## Self hosing

This bot is uses the [discord.py](https://discordpy.readthedocs.io/en/latest/) library and a [mongodb](https://www.mongodb.com/) database.

* Place your discord bot token and mongodb connection url inside `credentials.py`

* Install dependencies :
```python3 -m pip install dill pillow pymongo discord.py```
    ([pymongo might require additional authentication dependencies](https://pymongo.readthedocs.io/en/stable/installation.html))

* Run the bot:
    ```python3 src/bot.py```