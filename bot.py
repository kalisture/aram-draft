import discord
from discord.ext import commands
import random
import json

client = commands.Bot(command_prefix='%')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_command_error(ctx, error):
   await ctx.channel.send("Sorry, invalid command. Try %help")

@client.command(brief="Draft a custom \'Balanced\' aram game", usage="<team size> <champs per player>")
async def baram(ctx, teamS=3, idvPool=3):
    allChamps = getAllChamps()

    for i in getBanned():
        try:
            allChamps.pop(i)
        except:
            pass

    for i in getADCs():
        try:
            allChamps[i]['adc'] = True
        except:
            pass

    for i in getTanks():
        try:
            allChamps[i]['tank'] = True
        except:
            pass

    for i in getEnchanters():
        try:
            allChamps[i]['enchanter'] = True
        except:
            pass

    teamSize = int(teamS)
    idvPool = min(idvPool, 10)
    teamSize = min(teamSize, 5)
    embed = discord.Embed(
            title = "{name}\'s baram".format(name = ctx.author.display_name),
            description="{teamSize} vs. {teamSize}. Balanced mode. Pool is comprised of {idvPool} champs per player.".format(teamSize=teamSize, idvPool=idvPool),
            color = discord.Color.blurple()
    )

    teamL = []
    teamR = []
    
    rng = random.choice([i for i, j in allChamps.items() if j['adc'] == True])
    teamL.append(rng)
    allChamps.pop(rng)
    rng = random.choice([i for i, j in allChamps.items() if j['adc'] == True])
    teamR.append(rng)
    allChamps.pop(rng)

    count = 1
    if teamSize > count:
        rng = random.choice([i for i, j in allChamps.items() if j['tank'] == True])
        teamL.append(rng)
        allChamps.pop(rng)
        rng = random.choice([i for i, j in allChamps.items() if j['tank'] == True])
        teamR.append(rng)
        allChamps.pop(rng)
        count += 1

    if teamSize > count:
        rng = random.choice([i for i, j in allChamps.items() if j['enchanter'] == True])
        teamL.append(rng)
        allChamps.pop(rng)
        rng = random.choice([i for i, j in allChamps.items() if j['enchanter'] == True])
        teamR.append(rng)
        allChamps.pop(rng)
        count += 1

    for i in range (0, (teamSize * idvPool) - count):
        rng = random.choice(list(allChamps))
        teamL.append(rng)
        allChamps.pop(rng)
        rng = random.choice(list(allChamps))
        teamR.append(rng)
        allChamps.pop(rng)

    embed.add_field(name="Left Team", value=listFormat(teamL), inline=True)
    embed.add_field(name="Right Team", value=listFormat(teamR), inline=True)
    await ctx.channel.send(embed=embed)
    return

@client.command(hidden="true")
async def secret(ctx):
    await ctx.channel.send("tom stinks")



@client.command(brief="Draft a custom aram game", usage="<team size> <champs per player>")
async def aram(ctx, teamS=3, idvPool=3):

    allChamps = getAllChamps()
    teamSize = int(teamS)
    idvPool = min(idvPool, 10)
    teamSize = min(teamSize, 5)
    teamL = []
    teamR = []
    embed = discord.Embed(
        title = "{name}\'s Aram".format(name = ctx.author.display_name),
        description="{teamSize} vs. {teamSize}. Standard mode - Completely random. Pool is comprised of {idvPool} champs per player.".format(teamSize=teamSize, idvPool=idvPool),
        color = discord.Color.dark_blue()
    )

    for i in range (0, teamSize * idvPool):
        rng = random.choice(list(allChamps))
        teamL.append(rng)
        allChamps.pop(rng)
        rng = random.choice(list(allChamps))
        teamR.append(rng)
        allChamps.pop(rng)

    embed.add_field(name="Left Team", value=listFormat(teamL), inline=True)
    embed.add_field(name="Right Team", value=listFormat(teamR), inline=True)
    await ctx.channel.send(embed=embed)
    return

@client.event
async def on_guild_join(guild):

    with open("banlist.json", "r") as f:
        banlist = json.load(f)

    banlist[str(guild.id)] = getBanned()

    with open("banlist.json", "w") as f:
        json.dump(banlist, f)

# @client.command(brief="Display or edit the list of banned champions.", usage="add|remove|default <champion name>")
# async def banlist(ctx, p="list", champ=""):
#     champ = champ.title()
#     with open("banlist.json", "r") as f:
#         banlist = json.load(f)
#         match p:
#             case "list":       
#                 embed = discord.Embed(
#                     title="Banlist",
#                     color=discord.Color.red()
#                 )
#                 embed.add_field(name="Restricted from baram", value=listFormat(banlist[str(ctx.guild.id)]))
#                 await ctx.channel.send(embed=embed)
#                 return
#             case "add":
#                 if champ in banlist[str(ctx.guild.id)]:
#                     await ctx.channel.send(f"{champ} is already banned.")
#                 elif(champ in getAllChamps()):
#                     banlist[str(ctx.guild.id)].append(champ)
#                     await ctx.channel.send(f"{champ} was added to the banlist.")
#                 else:
#                     await ctx.channel.send(f"{champ} is not in the game. Check spelling.")

#             case "default":
#                 banlist[str(ctx.guild.id)] = getBanned()
#                 await ctx.channel.send("Banlist reset to default")
            
#             case "remove":
#                 if champ in banlist[str(ctx.guild.id)]:
#                     banlist[str(ctx.guild.id)].remove(champ)
#                     await ctx.channel.send(f"{champ} was removed from the banlist.")
#                 else:
#                     await ctx.channel.send(f"{champ} is not in the banlist. Check spelling")
#             case (default):
#                 await ctx.channel.send("Sorry, i didn't understand that.")

#     with open("banlist.json", "w") as f:
#         json.dump(banlist, f)

def listFormat(list):
    out = ""
    for i in list:
        out += i
        out += "\r"
    return out

def getAllChamps():
    allChamps = {"Aatrox": {},"Ahri": {},"Akali": {},"Akshan": {},"Alistar": {},"Amumu": {},"Anivia": {},"Annie": {},"Aphelios": {},"Ashe": {},"Aurelion Sol": {},"Azir": {},
        "Bard": {},"Blitzcrank": {},"Brand": {},"Braum": {},"Caitlyn": {},"Camille": {},"Cassiopeia": {},"Cho'Gath": {},"Corki": {},"Darius": {},"Diana": {},"Draven": {},"Dr, Mundo": {},
        "Ekko": {},"Elise": {},"Evelynn": {},"Ezreal": {},"Fiddlesticks": {},"Fiora": {},"Fizz": {},"Galio": {},"Gangplank": {},"Garen": {},"Gnar": {},"Gragas": {},"Graves": {},"Gwen": {},
        "Hecarim": {},"Heimerdinger": {},"Illaoi": {},"Irelia": {},"Ivern": {},"Janna": {},"Jarvan IV": {},"Jax": {},"Jayce": {},"Jhin": {},"Jinx": {},
        "Kai'Sa": {},"Kalista": {},"Karma": {},"Karthus": {},"Kassadin": {},"Katarina": {},"Kayle": {},"Kayn": {},"Kennen": {},"Kha'Zix": {},"Kindred": {},"Kled": {},"Kog'Maw": {},
        "LeBlanc": {},"Lee Sin": {},"Leona": {},"Lillia": {},"Lissandra": {},"Lucian": {},"Lulu": {},"Lux": {},"Malphite": {},"Malzahar": {},"Maokai": {},"Master Yi": {},"Miss Fortune": {},"Mordekaiser": {},"Morgana": {},
        "Nami": {},"Nasus": {},"Nautilus": {},"Neeko": {},"Nidalee": {},"Nocturne": {},"Nunu & Willump": {},"Olaf": {},"Orianna": {},"Ornn": {},"Pantheon": {},"Poppy": {},"Pyke": {},"Qiyana": {},"Quinn": {},
        "Rakan": {},"Rammus": {},"Rek'Sai": {},"Rell": {},"Renata Glasc": {},"Renekton": {},"Rengar": {},"Riven": {},"Rumble": {},"Ryze": {},"Samira": {},"Sejuani": {},"Senna": {},
        "Seraphine": {},"Sett": {},"Shaco": {},"Shen": {},"Shyvana": {},"Singed": {},"Sion": {},"Sivir": {},"Skarner": {},"Sona": {},"Soraka": {},"Swain": {},"Sylas": {},"Syndra": {},
        "Tahm Kench": {},"Taliyah": {},"Talon": {},"Taric": {},"Teemo": {},"Thresh": {},"Tristana": {},"Trundle": {},"Tryndamere": {},"Twisted Fate": {},"Twitch": {},"Udyr": {},
        "Urgot": {},"Varus": {},"Vayne": {},"Veigar": {},"Vel'Koz": {},"Vex": {},"Vi": {},"Viego": {},"Viktor": {},"Vladimir": {},"Volibear": {},"Warwick": {},"Wukong": {},"Xayah": {},
        "Xerath": {},"Xin Zhao": {},"Yasuo": {},"Yone": {},"Yorick": {},"Yuumi": {},"Zac": {},"Zed": {},"Zeri": {},"Ziggs": {},"Zilean": {},"Zoe": {},"Zyra": {}}

    for i in allChamps:
        allChamps[i] = {"adc": False, "enchanter": False, "tank": False}

    return allChamps

def getBruisers():
    bruisers = ["Aatrox", "Camille", "Dr. Mundo", "Fiora", "Garen", "Gnar", "Gwen", "Hecarim", "Illaoi", "Irelia", "Jarvan IV",
                "Jax", "Jayce"]    
    return

def getBanned():
    banned = ["Fiddlesticks", "Samira", "Malphite", "Ashe", "Qiyana", "Katarina"]
    return banned

def getADCs():
    adcs = ["Ashe", "Akshan", "Aphelios", "Caitlyn", "Corki", "Draven", "Jhin", "Jinx", "Lucian", "Kalista", "Kai'Sa", "Kindred", "Kog'Maw", "Miss Fortune", "Samira", "Senna", "Sivir", "Tristana", "Twitch", "Varus", "Vayne", "Xayah", "Zeri"]
    return adcs

def getEnchanters():
    enchanters = ["Ivern", "Janna", "Karma", "Lulu", "Nami", "Renata Glasc", "Seraphine", "Sona", "Soraka", "Yuumi"]
    return enchanters

def getTanks():
    tanks = ["Alistar", "Amumu", "Blitzcrank", "Braum", "Cho'Gath", "Dr. Mundo", "Galio", "Kled", "Leona", "Malphite", "Maokai",
         "Nautilus", "Nunu & Willump", "Ornn", "Poppy", "Rakan", "Rammus", "Rell", "Singed", "Sion", "Skarner", "Trundle", "Tahm Kench", "Taric",
         "Thresh", "Volibear", "Warwick"]
    return tanks

def powerPicks():
    return




client.run('OTQ0NDU2NzI1NTU2MjQwNDE0.YhB33g.l3Vw765fWBALxy_OGLSqvBeLARY')