import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix='%')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command(brief="Draft a custom \'Balanced\' aram game", usage="<team size> <champs per player>")
async def baram(ctx, teamS=3, idvPool=3):
    embed = discord.Embed(
        title = "{name}\'s Aram".format(name = ctx.author.display_name),
        description="{teamS} vs. {teamS}. Balanced mode. Pool is comprised of {idvPool} champs per player.".format(teamS=teamS, idvPool=idvPool),
        color = discord.Color.dark_blue())

    allChamps = getallChamps()
    banned = getBanned()
    adcs = getADCs()
    tanks = getTanks()
    enchanters = getEnchanters()

    idvPool = min(idvPool, 10)

    teamSize = int(teamS)
    teamL = []
    teamR = []
    count = 0

    #remove banned
    for i in banned:
        allChamps.remove(i)
        try:
            adcs.remove(i)
        except:
            pass
        try:
            tanks.remove(i)
        except:
            pass
        try:
            enchanters.remove(i)
        except:
            pass

    #ADC
    adc = adcs.pop(random.randrange(0, len(adcs)))
    teamL.append(
        allChamps.pop(allChamps.index(adc))
    )
    try:
        tanks.pop(tanks.index(adc))
    except:
        pass
    try:
        enchanters.pop(enchanters.index(adc))
    except:
        pass
    adc = adcs.pop(random.randrange(0, len(adcs)))
    teamR.append(
        allChamps.pop(allChamps.index(adc))
    )
    try:
        tanks.pop(tanks.index(adc))
    except:
        pass
    try:
        enchanters.pop(enchanters.index(adc))
    except:
        pass
    count += 1


    if count < teamSize:
        enchanter = enchanters.pop(random.randrange(0, len(enchanters)))
        teamL.append(
            allChamps.pop(allChamps.index(enchanter))
        )
        try:
            enchanters.pop(tanks.index(enchanter))
        except:
            pass

        enchanter = enchanters.pop(random.randrange(0, len(enchanters)))

        teamR.append(
            allChamps.pop(allChamps.index(enchanter))
        )
        try:
            tanks.pop(tanks.index(enchanter))
        except:
            pass
        count += 1

    if count < teamSize:
        tank = tanks.pop(random.randrange(0, len(tanks)))
        teamL.append(
            allChamps.pop(allChamps.index(tank))
        )
        tank = tanks.pop(random.randrange(0, len(tanks)))
        teamR.append(
            allChamps.pop(allChamps.index(tank))
        )
        count +=1

    for i in range (0, (teamSize * idvPool) - count):
        teamL.append(allChamps.pop(random.randrange(0, len(allChamps))))
        teamR.append(allChamps.pop(random.randrange(0, len(allChamps))))

    embed.add_field(name="Left Team", value=listFormat(teamL), inline=True)
    embed.add_field(name="Right Team", value=listFormat(teamR), inline=True)
    await ctx.channel.send(embed=embed)
    return

@client.command(hidden="true")
async def secret(ctx):
    await ctx.channel.send("tom stinks")

@client.command(brief="Displays a list of banned champions.")
async def banned(ctx):
    embed = discord.Embed(
        title="Banlist",
        color=discord.Color.red()
    )
    embed.add_field(name="Restricted from baram", value=listFormat(getBanned()))
    await ctx.channel.send()
    return

@client.command(brief="Draft a custom aram game", usage="<team size> <champs per player>")
async def aram(ctx, teamS=3, idvPool=3):
    embed = discord.Embed(
        title = "{name}\'s Aram".format(name = ctx.author.display_name),
        description="{teamS} vs. {teamS}. Standard mode - Completely random. Pool is comprised of {idvPool} champs per player.".format(teamS=teamS, idvPool=idvPool),
        color = discord.Color.dark_blue())
    allChamps = getallChamps()
    idvPool = min(idvPool, 10)

    teamSize = int(teamS)
    teamL = []
    teamR = []

    for i in range (0, teamSize*idvPool):
        teamL.append(allChamps.pop(random.randrange(0, len(allChamps))))
        teamR.append(allChamps.pop(random.randrange(0, len(allChamps))))

    embed.add_field(name="Left Team", value=listFormat(teamL), inline=True)
    embed.add_field(name="Right Team", value=listFormat(teamR), inline=True)
    await ctx.channel.send(embed=embed)
    return

def listFormat(list):
    out = ""
    for i in list:
        out += i
        out += "\r"
    return out

def getallChamps():
    allChamps = ["Aatrox","Ahri","Akali","Akshan","Alistar","Amumu","Anivia","Annie","Aphelios","Ashe","Aurelion Sol","Azir",
        "Bard","Blitzcrank","Brand","Braum","Caitlyn","Camille","Cassiopeia","Cho'Gath","Corki","Darius","Diana","Draven","Dr. Mundo",
        "Ekko","Elise","Evelynn","Ezreal","Fiddlesticks","Fiora","Fizz","Galio","Gangplank","Garen","Gnar","Gragas","Graves","Gwen",
        "Hecarim","Heimerdinger","Illaoi","Irelia","Ivern","Janna","Jarvan IV","Jax","Jayce","Jhin","Jinx",
        "Kai'Sa","Kalista","Karma","Karthus","Kassadin","Katarina","Kayle","Kayn","Kennen","Kha'Zix","Kindred","Kled","Kog'Maw",
        "LeBlanc","Lee Sin","Leona","Lillia","Lissandra","Lucian","Lulu","Lux","Malphite","Malzahar","Maokai","Master Yi","Miss Fortune","Mordekaiser","Morgana",
        "Nami","Nasus","Nautilus","Neeko","Nidalee","Nocturne","Nunu & Willump","Olaf","Orianna","Ornn","Pantheon","Poppy","Pyke","Qiyana","Quinn",
        "Rakan","Rammus","Rek'Sai","Rell","Renata Glasc","Renekton","Rengar","Riven","Rumble","Ryze","Samira","Sejuani","Senna",
        "Seraphine","Sett","Shaco","Shen","Shyvana","Singed","Sion","Sivir","Skarner","Sona","Soraka","Swain","Sylas","Syndra",
        "Tahm Kench","Taliyah","Talon","Taric","Teemo","Thresh","Tristana","Trundle","Tryndamere","Twisted Fate","Twitch","Udyr",
        "Urgot","Varus","Vayne","Veigar","Vel'Koz","Vex","Vi","Viego","Viktor","Vladimir","Volibear","Warwick","Wukong","Xayah",
        "Xerath","Xin Zhao","Yasuo","Yone","Yorick","Yuumi","Zac","Zed","Zeri","Ziggs","Zilean","Zoe","Zyra"]
    return allChamps

def getBruisers():
    bruisers = ["Aatrox", "Camille", "Dr. Mundo", "Fiora", "Garen", "Gnar", "Gwen", "Hecarim", "Illaoi", "Irelia", "Jarvan IV",
                "Jax", "Jayce"]    
    return

def getBanned():
    banned = ["Fiddlesticks", "Samira", "LeBlanc", "Malphite", "Master Yi", "Soraka", "Sett", "Qiyana", "Senna", "Veigar"]
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