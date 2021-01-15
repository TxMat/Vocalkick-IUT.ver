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


async def helpp(message, *args):
    mem = message.author
    await mem.create_dm()
    await mem.dm_channel.send("__**command list:**__ \n\n**option alone_time :** temps (en sec) qu'un utilisateur peut rester seul dans un vocal (par défaut 5min)\n\n**option raison :** le message qui sera envoyé aux utilisateur kickés (le message se supprime au bout de <deltime>)\n\n**option prefix :** permet de changer le préfix du bot (& par défaut)\n\n**help :** envoie ce message à l'utilisateur qui effectue la commande\n\n**option emoji :** l'emoji avec le quel le bot réagit quand une personne fait <préfix>help (par défaut : :ok_hand:)\n\n**option frst_time :** temps (en sec) avant que le bot ne kick une personne qui est seul dans un vocal et qui n'a jamais été en conversation avec un autre utilisateur (30min par défaut )\n\n**option deltime :** temps (en sec) avant que le bot supprime le message d'avertissement envoyé en dm (par défaut : 24h)\n\n**option role :** nom du role qu'un membre doit posséder pour modifier les differents parametres (`modifier` par défaut)\n\n ```note : il vous faut la permission `déplacer les membres` ou le role defini par <role> pour parametrer le bot```\n\n`Une question/sugestion? contactez mon devloppeur : `<@259676097652719616>` :)`")
    await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])


actions = {
    "option": option,
    "desc": change_presence,
    "help": helpp
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
                await client.get_user(259676097652719616).dm_channel.send(log)
                log = "by :", message.author
                await client.get_user(259676097652719616).dm_channel.send(log)
                return
            await message.author.dm_channel.send(">:(")
            log = "insult in dm :", message.content
            await client.get_user(259676097652719616).dm_channel.send(log)
            log = "get trolled :", message.author
            await client.get_user(259676097652719616).dm_channel.send(log)
            return
        log = "dm ressage recived :", message.content
        await client.get_user(259676097652719616).dm_channel.send(log)
        log = "by :", message.author
        await client.get_user(259676097652719616).dm_channel.send(log)
        return

    if len(message.content) and message.content[0] == OPTIONS[message.guild.
                                                              id]["prefix"]:
        a = message.content[1:].split(" ")
        if a[0] not in actions:
            log = "wrong command:", message.content, "by :", message.author
            await client.get_user(259676097652719616).dm_channel.send(log)
            await message.add_reaction("❔")
            return
        if a[0] in admin_actions and message.author.id not in CONFIG["admins"]:
            log = "wrong permission to use command:", message.content, "by :", message.author
            await client.get_user(259676097652719616).dm_channel.send(log)
            await message.add_reaction("❌")
            return
        if a[0] in perm_actions and (
                message.author.guild_permissions.move_members == False
                and OPTIONS[message.channel.guild.id]["role"] not in list(
                    map(lambda x: x.name, message.author.roles))):
            log = "no perms nice try ", message.author
            await client.get_user(259676097652719616).dm_channel.send(log)
            await message.add_reaction("❌")
            await client.get_user(259676097652719616).dm_channel.send(
                message.author.roles)
            return
        log = "executing command:", message.content, "by :", message.author
        await client.get_user(259676097652719616).dm_channel.send(log)
        await actions[a[0]](message, *a[1:])


@client.event
async def on_ready():
    mute = False
    await change_presence(None, '&help | online and ready')
    for server in client.guilds:
        OPTIONS[server.id] = dict(DEFAULT)
    print("**RESTART**")
    print('{} is online and ready to kick'.format(client.user))


@client.event
async def on_guild_join(guild):
    OPTIONS[guild.id] = dict(DEFAULT)


async def on_delay(channel, first=False):
    await client.get_user(259676097652719616).create_dm()
    if not OPTIONS[channel.guild.id]["running"]:
        if channel in CHANNELS:
            del CHANNELS[channel]
        return
    if first:
        log = channel.members[
            0].name, "is alone in", channel.name, "waiting for someone in the server :", channel.guild.name,
        await client.get_user(259676097652719616).dm_channel.send(log)
        log = "starting the alone time countdown before kicking(", OPTIONS[
            channel.guild.id]["frst_time"], "sec )"
        await client.get_user(259676097652719616).dm_channel.send(log)
        await asyncio.sleep(OPTIONS[channel.guild.id]["frst_time"])
        try:
            log = "Countdown ended for", channel.members[
                0].name, "in", channel.name, "(", channel.guild.name, ")"
            await client.get_user(259676097652719616).dm_channel.send(log)
        except:
            log = "Countdown ended but the member has left the channel before"
            await client.get_user(259676097652719616).dm_channel.send(log)
    else:
        log = channel.members[
            0].name, "is now alone in the channel", channel.name, "in the server :", channel.guild.name
        await client.get_user(259676097652719616).dm_channel.send(log)
        log = "starting the alone time countdown before kicking(", OPTIONS[
            channel.guild.id]["alone_time"], "sec )"
        await client.get_user(259676097652719616).dm_channel.send(log)
        await asyncio.sleep(OPTIONS[channel.guild.id]["alone_time"])
        try:
            log = "Countdown ended for", channel.members[
                0].name, "in", channel.name, "(", channel.guild.name, ")"
            await client.get_user(259676097652719616).dm_channel.send(log)
        except:
            log = "Countdown ended but the member has left the channel before"
            await client.get_user(259676097652719616).dm_channel.send(log)

    while not OPTIONS[channel.guild.id]["running"]:
        if first:
            await asyncio.sleep(OPTIONS[channel.guild.id]["frst_time"])
        else:
            await asyncio.sleep(OPTIONS[channel.guild.id]["alone_time"])
    if channel in CHANNELS:
        del CHANNELS[channel]
        members = channel.members
        nb = len(members)
        if nb != 1:
            if nb > 1:
                log = "there is now", nb, "person connected in", channel.name, "(", channel.guild.name, ") with", members[
                    0], "aborting kicking procedure..."
                await client.get_user(259676097652719616).dm_channel.send(log)
                return
            if nb == 0:
                log = "there is no one in the channel", channel.name, "can't process to kick..."
                await client.get_user(259676097652719616).dm_channel.send(log)
                return
        log = members[
            0], "is still alone in", channel.name, "on", channel.guild, "starting kicking procedure..."
        await client.get_user(259676097652719616).dm_channel.send(log)
        await members[0].edit(
            voice_channel=None, reason=OPTIONS[channel.guild.id]["reason"])
        log = members[0], "kicked!"
        await client.get_user(259676097652719616).dm_channel.send(log)
        await members[0].create_dm()
        try:
            await members[0].dm_channel.send(
                OPTIONS[channel.guild.id]["reason"],
                delete_after=OPTIONS[channel.guild.id]["deltime"])
        except Exception as e:
            if e.code == 50007:
                log = "can't send dm to", members[
                    0], "the user must have bocked me"
                await client.get_user(259676097652719616).dm_channel.send(log)


@client.event
async def on_voice_state_update(member, before, after):
    await client.get_user(259676097652719616).create_dm()
    if after.channel and before.channel != after.channel:
        if after.channel in CHANNELS:
            del CHANNELS[after.channel]
        if len(after.channel.members) == 1:
            CHANNELS[after.channel] = True
            log = "channel changed for", member.name, "(", before.channel, "->", after.channel, ")"
            await client.get_user(259676097652719616).dm_channel.send(log)
            await on_delay(after.channel, first=True)

    if before.channel and before.channel != after.channel:
        if len(before.channel.members) == 1:
            CHANNELS[before.channel] = True
            log = member.name, "leave"
            await client.get_user(259676097652719616).dm_channel.send(log)
            await on_delay(before.channel)
        else:
            if before.channel in CHANNELS:
                del CHANNELS[before.channel]

keep_live()
client.run(CONFIG["token"])
