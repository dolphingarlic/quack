import os, sys
import discord
import re
from discord.ext import commands
import io
import asyncio
import time
import pickle

tech_id = 659440262422069269
ace_id = 463225414534430721
emotes_id = 750971097054445648

yak_id = 133270838605643776
slav_id = 193701039633989632
admin_ids = [yak_id, slav_id]

ready = """print('Logged in as')
print(bot.user.name)
print(bot.user.id)
print(" ".join(sys.argv))
print('------')"""

def restart_func(user_id):
    if user_id in admin_ids:
        os.execl(sys.executable, sys.executable, *sys.argv)

token = open("maintoken.txt", "r").read()

pref_file = "preferences.pickle"

class QuackPrefs:
    def __init__(self, save_filename):
        self.save_filename = save_filename 
        self.guilds = {}
        self.save()

    def set_prefs(self, guild_id, pref_val_dict):
        if guild_id not in self.guilds:
            self.guilds[guild_id] = {}
        self.guilds[guild_id].update(pref_val_dict)
        self.save()

    def save(self):
        pickle.dump(self, open(self.save_filename, "wb"))

try:
    prefs = pickle.load(open(pref_file, "rb"))
except FileNotFoundError:
    prefs = QuackPrefs(pref_file)
