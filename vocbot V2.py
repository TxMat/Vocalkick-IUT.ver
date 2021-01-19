import discord
import asyncio
from keep_live import keep_live
from time import sleep, time
from json import load as json_load
from discord.utils import get
print(discord.__version__)

with open("config.json") as f:
    CONFIG = json_load(f)

OPTIONS = {}
DEFAULT = {}
DEFAULT["prefix"] = "&"
DEFAULT["alone_time"] = 300
DEFAULT["reason"] = "as-tu oublié de te déconnecter du vocal? ne t'inquiete pas je l'ai fait pour toi :)"
DEFAULT["emoji"] = "👌"
DEFAULT["deltime"] = 86400
DEFAULT["frst_time"] = 1800
DEFAULT["role"] = "modifier"

client = discord.Client()
CHANNELS = {}


async def option(message, var, value, *args):
    OPTIONS[message.guild.id][var] = type(
        OPTIONS[message.guild.id][var])(value)
    await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])


async def change_presence(message, *args):
    await client.change_presence(
        activity=discord.Activity(
            name=" ".join(args), type=discord.ActivityType.playing))
    log = "desc change to :", " ".join(args)
    print(str(log))

async def noo(message, *args):
  await message.delete()
  await message.channel.send("https://cdn.discordapp.com/attachments/496012052406468639/798961383949074432/NO.mp4")
  log = "no"
  print(log)

async def bott(message, *args):
    user = client.get_user(args[0])
    await client.wait_until_ready()
    message.channel.send(user.created_at)

async def statt(message, *args):
  await message.channel.send("voici mes page de statut \n *notez les bien si je suis offline je ne pourrais pas vous les redonner* \n\n page de staut de l'hebergeur : https://stats.uptimerobot.com/o8vVviXMNY \n mot de passe : vivelebot \n\n page de statut du bot : https://Vocalkick.txmat.repl.co \n *si la parge renvoie ;) c'est que tout va bien sinon il y a un soucis* ")

async def helpp(message, *args):
    mem = message.author
    await mem.create_dm()
    await mem.dm_channel.send("__**command list:**__ \n\n**option alone_time :** temps (en sec) qu'un utilisateur peut rester seul dans un vocal (par défaut 5min)\n\n**option raison :** le message qui sera envoyé aux utilisateur kickés (le message se supprime au bout de <deltime>)\n\n**option prefix :** permet de changer le préfix du bot (& par défaut)\n\n**help :** envoie ce message à l'utilisateur qui effectue la commande\n\n**option emoji :** l'emoji avec le quel le bot réagit quand une personne fait <préfix>help (par défaut : :ok_hand:)\n\n**option frst_time :** temps (en sec) avant que le bot ne kick une personne qui est seul dans un vocal et qui n'a jamais été en conversation avec un autre utilisateur (30min par défaut )\n\n**option deltime :** temps (en sec) avant que le bot supprime le message d'avertissement envoyé en dm (par défaut : 24h)\n\n**option role :** nom du role qu'un membre doit posséder pour modifier les differents parametres (`modifier` par défaut)\n\n ```note : il vous faut la permission `déplacer les membres` ou le role defini par <role> pour parametrer le bot```\n\n`Une question/sugestion? contactez mon devloppeur : `<@259676097652719616>` :)`\n\n*Ver : IUT2.3*")
    await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])


actions = {
    "option": option,
    "desc": change_presence,
    "help": helpp,
    "no": noo,
    "up": statt,
    "age": bott
}
perm_actions = ["option"]
admin_actions = ["desc"]

badwords = [
    "tg", "ntm", "pd", "fdp", "suce", "ftg"
]


@client.event
async def on_message(message):
    
    if type(message.channel) != discord.TextChannel:
        if message.author.id == 697343120433741947:
            return
        if message.content.lower() in badwords:
            if message.author.id == 328521363180748801:
                log = "insult in dm :", message.content
                print(log)
                log = "by :", message.author
                print(log)
                return
            await message.author.dm_channel.send(">:(")
            log = "insult in dm :", message.content
            print(log)
            log = "get trolled :", message.author
            print(log)
            return
        log = "dm ressage recived :", message.content
        print(log)
        log = "by :", message.author
        print(log)
        return

    if len(message.content) and message.content[0] == OPTIONS[message.guild.
                                                              id]["prefix"]:
        a = message.content[1:].split(" ")
        if a[0] not in actions:
            log = "wrong command:", message.content, "by :", message.author
            print(log)
            await message.add_reaction("❔")
            return
        if a[0] in admin_actions and message.author.id not in CONFIG["admins"]:
            log = "wrong permission to use command:", message.content, "by :", message.author
            print(log)
            await message.add_reaction("❌")
            return
        if a[0] in perm_actions and (
                message.author.guild_permissions.move_members == False
                and OPTIONS[message.channel.guild.id]["role"] not in list(
                    map(lambda x: x.name, message.author.roles))):
            log = "no perms nice try ", message.author
            print(log)
            await message.add_reaction("❌")
            print(
                message.author.roles)
            return
        log = "executing command:", message.content, "by :", message.author
        print(log)
        await actions[a[0]](message, *a[1:])


@client.event
async def on_ready():
    await change_presence(None, '&help | online and ready')
    for server in client.guilds:
        OPTIONS[server.id] = dict(DEFAULT)
    print("**RESTART**")
    print('{} is online and ready to kick'.format(client.user))


@client.event
async def on_guild_join(guild):
    OPTIONS[guild.id] = dict(DEFAULT)


async def on_delay(channel, first=False):
    if first:
        log = channel.members[
            0].name, "is alone in", channel.name, "waiting for someone in the server :", channel.guild.name,
        print(log)
        log = "starting the alone time countdown before kicking(", OPTIONS[
            channel.guild.id]["frst_time"], "sec )"
        print(log)
        await asyncio.sleep(OPTIONS[channel.guild.id]["frst_time"])
        try:
            log = "Countdown ended for", channel.members[
                0].name, "in", channel.name, "(", channel.guild.name, ")"
            print(log)
        except:
            log = "Countdown ended but the member has left the channel before"
            print(log)
    else:
        log = channel.members[
            0].name, "is now alone in the channel", channel.name, "in the server :", channel.guild.name
        print(log)
        log = "starting the alone time countdown before kicking(", OPTIONS[
            channel.guild.id]["alone_time"], "sec )"
        print(log)
        await asyncio.sleep(OPTIONS[channel.guild.id]["alone_time"])
        try:
            log = "Countdown ended for", channel.members[
                0].name, "in", channel.name, "(", channel.guild.name, ")"
            print(log)
        except:
            log = "Countdown ended but the member has left the channel before"
            print(log)

    if channel in CHANNELS:
        del CHANNELS[channel]
        members = channel.members
        nb = len(members)
        if nb != 1:
            if nb > 1:
                log = "there is now", nb, "person connected in", channel.name, "(", channel.guild.name, ") with", members[
                    0], "aborting kicking procedure..."
                print(log)
                return
            if nb == 0:
                log = "there is no one in the channel", channel.name, "can't process to kick..."
                print(log)
                return
        log = members[
            0], "is still alone in", channel.name, "on", channel.guild, "starting kicking procedure..."
        print(log)
        await members[0].edit(
            voice_channel=None, reason=OPTIONS[channel.guild.id]["reason"])
        log = members[0], "kicked!"
        print(log)
        await members[0].create_dm()
        try:
            await members[0].dm_channel.send(
                OPTIONS[channel.guild.id]["reason"],
                delete_after=OPTIONS[channel.guild.id]["deltime"])
        except Exception as e:
            if e.code == 50007:
                log = "can't send dm to", members[
                    0], "the user must have bocked me"
                print(log)


@client.event
async def on_voice_state_update(member, before, after):
    
    if after.channel and before.channel != after.channel:
        if after.channel in CHANNELS:
            del CHANNELS[after.channel]
        if len(after.channel.members) == 1:
            CHANNELS[after.channel] = True
            log = "channel changed for", member.name, "(", before.channel, "->", after.channel, ")"
            print(log)
            await on_delay(after.channel, first=True)

    if before.channel and before.channel != after.channel:
        if len(before.channel.members) == 1:
            CHANNELS[before.channel] = True
            log = member.name, "leave"
            print(log)
            await on_delay(before.channel)
        else:
            if before.channel in CHANNELS:
                del CHANNELS[before.channel]

keep_live()
client.run(CONFIG["token"])