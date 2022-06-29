import discord
import os

bot = discord.Client()

@bot.event
async def on_ready():
  print('Bot ON: {0.user}'.format(bot))
  await bot.change_presence(activity=discord.Game(name='"DUNG help"'))

@bot.event
async def on_message(msg):
  if msg.author == bot.user:
    return

  if msg.content.startswith('DUNG'):
    cmd = msg.content[5:]
    
    if cmd == 'help':
      await msg.channel.send(embed = bhelp())
      
    elif cmd.startswith('produce'):
      pars = cmd[8:].split(" ")
      if len(pars) != 2:
        await msg.channel.send('Wrong number of parameters!')
        return
      await msg.channel.send(embed = calcPoop(int(pars[0]), int(pars[1])))

    elif cmd.startswith('fts'):
      await msg.channel.send(embed = fertToScrap(int(cmd[4:])))

    elif cmd.startswith('stf'):
      await msg.channel.send(embed = scrapToFert(int(cmd[4:])))
    
    else: await msg.channel.send('Command not recognized!')
      

# Functions
def bhelp():
  output = discord.Embed(
    title = 'Horse Dung Bot',
    description = 'A simple bot that calculates horse dung value and produce & sell time.',
    color = discord.Color.dark_green())
  output.add_field(name = 'help', value = 'The page you are on.', inline = False)
  output.add_field(name = 'produce [scrap amount] [# of horses]', value = 'Calculates the amount of dung required to produce that scrap, the amount of time it will compost, and how long it will take to sell the fertilizer.', inline = False)
  output.add_field(name = 'fts [# of fertilizer]', value = '(Fertilizer to scrap) - Calculates the amount of scrap you will get for a given amount of fertilizer.', inline = False)
  output.add_field(name = 'stf [# of scrap]', value = '(Scrap to fertilizer) - Calculates the amount of fertilizer you will need for a given amount of scrap', inline = False)
  return output

def calcPoop(scrap, horses):
  fert = (scrap / 3) * 2
  poop = fert / 10
  if poop > 11: fert_time_m = ((poop / 11) * 170) / 60
  else: fert_time_m = 170 / 60
  fert_time_h = fert_time_m / 60
  poop_time_m = (poop * 70 / horses) / 60
  poop_time_h = poop_time_m / 60
  if fert > 68: sell_time_m = ((fert - 68) / 27)
  else:  sell_time_m = 0
  sell_time_h = sell_time_m / 60

  output = discord.Embed(
    title = f'Calculation complete! [{scrap} scrap] [{horses} horses]',
    description = f'Total time: **{round((fert_time_m + poop_time_m + sell_time_m), 2)} minutes** ({round((fert_time_h + poop_time_h + sell_time_h), 2)} hours)\nTotal time (no sell cap): **{round((fert_time_m + poop_time_m), 2)} minutes** ({round((fert_time_h + poop_time_h), 2)} hours)',
    color = discord.Color.dark_green())
  output.add_field(name = f'{round(fert, 2)} fertilizer\n{round(poop, 2)} poop\n{round(poop_time_m, 2)} minutes to poop ({round(poop_time_h, 2)} hours)\n{round(fert_time_m, 2)} minutes to fertilize ({round(fert_time_h, 2)} hours)\n{round(sell_time_m, 2)} minutes to sell ({round(sell_time_h, 2)} hours)\n', value = 'Good luck in poop farming!', inline = False)
  return output

def fertToScrap(fert):
  output = discord.Embed(
    title = f'{(fert / 2) * 3} scrap!',
    description = f'On a no sale cap server, this will take {round((fert - 68) / 27, 2)} minutes to sell.',
    color = discord.Color.dark_green())
  return output

def scrapToFert(scrap):
  output = discord.Embed(
    title = f'{(scrap / 3) * 2} fertilizer!',
    description = f'On a no sale cap server, this will take {round((((scrap / 3) * 2) - 68) / 27, 2)} minutes to sell.',
    color = discord.Color.dark_green())
  return output

      
# Auth
bot.run(os.environ['authKey'])