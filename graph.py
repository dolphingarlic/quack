import discord
from discord.ext import commands
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
from sympy import *
import io
import numpy as np
import re
import sys
import os

description = ""

bot = commands.Bot(command_prefix='?', description=description)

transformations = (standard_transformations + (implicit_multiplication_application,))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(sys.argv)
    print('------')

@bot.command()
async def restart(ctx):
    if ctx.message.author.id == 133270838605643776:
        os.system("git pull")
        os.execl(sys.executable, sys.executable, *sys.argv)

@bot.command()
async def graph(ctx, *args):#x_bound:str, y_bound = "", *args):
    in_str = " ".join(args)
    bound_y = r"y ?= ?\(-?[0-9]+\.?[0-9]*, ?-?[0-9]+\.?[0-9]*\)"
    bound_x = r"x ?= ?\(-?[0-9]+\.?[0-9]*, ?-?[0-9]+\.?[0-9]*\)"
    y_bound = re.findall(bound_y, in_str)
    x_bound = re.findall(bound_x, in_str)
    if y_bound:
        in_str = re.sub(bound_y, lambda y: "", in_str)
        y_bounds = tuple(float(y) for y in y_bound[0].replace(" ", "")[3:-1].split(","))
    else:
        y_bounds = None
    if x_bound:
        in_str = re.sub(bound_x, lambda x: "", in_str)
        x_bounds = tuple(float(x) for x in x_bound[0].replace(" ", "")[3:-1].split(","))
    else:
        x_bounds = (-1, 1)
    expr = sympify(in_str.strip(", "))
    expr.subs(Symbol("e"), np.e)
    expr.subs(Symbol("pi"), np.pi)
    expr.subs(Symbol("π"), np.pi)
    f = np.vectorize(lambda x: expr.subs(Symbol("x"), x))
    x = np.linspace(*x_bounds, 1000)
    y = f(x)
    for i, y_elem in enumerate(y):
        try:
            y[i] = float(y[i])
        except:
            y[i] = np.NaN
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set(xlim=x_bounds)
    ax.spines['top'].set_visible(False)#.set_color('white') 
    ax.spines['right'].set_visible(False)#.set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.grid(True)
    #ax.axis("equal")
    if y_bounds is not None:
        ax.set(ylim=y_bounds)
    ax.plot(x, y)
    ax.spines['left'].set_position(('data', min(max(ax.xlim[0], 0), ax.xlim[1])))
    ax.spines['bottom'].set_position(('data', min(max(ax.ylim[0], 0), ax.ylim[1])))
    buf = io.BytesIO()
    buf.name = "graph.png"
    fig.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    await ctx.channel.send(file=discord.File(buf))

f = open("maintoken.txt", "r")
token = f.readlines()[0]
bot.run(token)
