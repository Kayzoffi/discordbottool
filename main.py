import discord
from discord.ext import commands, tasks
import random
import asyncio
from discord.ext.commands import Bot
from asyncio import sleep
import youtube_dl
from discord.utils import get
intents = discord.Intents().all()
color = 0x206694

musics = {}
ytdl = youtube_dl.YoutubeDL()

bot = commands.Bot(command_prefix = "-", description = "Bot de Kayzo", intents = intents)
status = ["Modération",
        "Musique",
		"Version : bêta",
		"ReadingRP Tool", 
		"Dev - Kayzo"]

@bot.event
async def on_ready():
	print("Bot prêt à l'emploi !")
	changeStatus.start()

@tasks.loop(seconds = 8)
async def changeStatus():
	game = discord.Game(random.choice(status))
	await bot.change_presence(status = discord.Status.dnd, activity = game)

@bot.command()
async def setupmoderation(ctx):
	server = ctx.guild
	serverName = server.name
	embed = discord.Embed(title = f"**__{serverName} | Aide Modération__**", description = ":construction: Prefix : `-` \n :recycle: En cours développement !", color = 0x206694)
	embed.set_thumbnail(url = "https://media.giphy.com/media/l0Exezf44dEdueHRK/giphy.gif")
	embed.add_field(name = "> Modération", value = "`-ban <membre> [raison]` \n *Bannit un ou plusieurs membres du serveur, une raison peut être précisée* \n\n `-unban <#> ` \n *Enlève le ban d'un ou plusieurs membres sur le serveur* \n\n `-clear [nombre]` \n *Supprime le nombre de messages donnés dans le salon actuel. Si un membre est précisé, seul ses messages sont supprimés* \n\n `-unmute <membre>` \n *Met fin au mute d'un ou plusieurs membres* \n\n `-mute <membre> [raison]` \n *Mute un ou plusieurs membres, une raison peut être précisée* \n\n `-kick <membre> [raison]` *Expulse un ou plusieurs membres du serveur, une raison peut être précisée* \n\n `-lock/unlock` \n *Ferme ou réouvre un salon du serveur* \n\n `-addrole <rôle> <membre>` \n *Ajoute le ou les rôles souhaités à la ou les personnes souhaitées* \n\n `-removerole <rôle> <membre>` \n *Supprime le ou les rôles souhaités de la ou des personnes souhaités*", inline = True)


	await ctx.send(embed = embed)

@bot.command(aliases= ['purge','delete'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
   if amount == None:
       await ctx.channel.purge(limit=1000000)
   else:
       await ctx.channel.purge(limit=amount)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title = f"**__Commande inexistante !__**", description = f"**- Cette commande n'existe pas !** \n\n **- Veuillez vous aider à l'aide de cette commande `-aide <categories>`.**", color = 0x206694)
            embed.set_thumbnail(url = "https://media.giphy.com/media/o7dsbpFQZwRxPSOOaz/giphy.gif")

            await ctx.send(embed = embed)


def good_channel(ctx):
		return ctx.message.channel.id

@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = f"**__Erreur clear !__**", description = f"**- La commande __clear__ prend en parametre un nombre !** \n\n **- Veuillez réessayer avec `-clear [nombre]`.**", color = 0x206694)
            embed.set_thumbnail(url = "https://media.giphy.com/media/o7dsbpFQZwRxPSOOaz/giphy.gif")

            await ctx.send(embed = embed)

@bot.command()
async def servinfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	serverDescription = server.description
	numberOfPerson = server.member_count
	serverName = server.name
	message = f"`-` Le serveur **{serverName}** contient *{numberOfPerson}* personnes ! \n\n`-` La description du serveur est {serverDescription}. \n\n`-` Ce serveur possède {numberOfTextChannels} salons écrit et {numberOfVoiceChannels} salon vocaux."
	await ctx.send(message)

async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "**Creation du role Muted pour mute des gens.**")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)


@bot.command()
async def mute(ctx, member : discord.Member, *, reason = "**Aucune raison n'a été renseigné**"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    embed = discord.Embed(title = f"**__Mute effectué !__**", description = f"**- {member.mention} à bien été mute ! ** \n\n **- Pour le unmute `-unmute <membre>`**", color = 0x206694)
    embed.set_thumbnail(url = "https://media.giphy.com/media/RIkTZtY0xFzWJapNnU/giphy.gif")

    await ctx.send(embed = embed)

@mute.error
async def mute_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = f"**__Erreur mute !__**", description = f"**- La commande __mute__ prend en parametre un utilisateur !** \n\n **- Veuillez réessayer avec `-mute <membre>`.**", color = 0x206694)
            embed.set_thumbnail(url = "https://media.giphy.com/media/o7dsbpFQZwRxPSOOaz/giphy.gif")

            await ctx.send(embed = embed)


@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = "**Aucune raison n'a été renseigné**"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    embed = discord.Embed(title = f"**__Unmute effectué !__**", description = f"**- {member.mention} à bien été unmute ! **", color = 0x206694)
    embed.set_thumbnail(url = "https://media.giphy.com/media/ZYDdrQToEZw5xh1QWM/giphy.gif")

    await ctx.send(embed = embed)

@unmute.error
async def unmute_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = f"**__Erreur unmute !__**", description = f"**- La commande __unmute__ prend en parametre un utilisateur !** \n\n **- Veuillez réessayer avec `-unmute <membre>`.**", color = 0x206694)
            embed.set_thumbnail(url = "https://media.giphy.com/media/o7dsbpFQZwRxPSOOaz/giphy.gif")

            await ctx.send(embed = embed)


@bot.command()
async def kick(ctx, user : discord.User, *, reason = "**__Aucune raison n'a été renseignée !__**"):
	await ctx.guild.kick(user, reason = reason)
    
	em = discord.Embed(description = f"{user.mention} **a été __kick__ avec succès !** \n\n **Cause** : **{reason}** \n\n **Auteur** : **__{ctx.author}__** ", color = 0x206694)
	em.set_thumbnail(url = user.avatar_url)
    
	await ctx.send(embed = em)


@kick.error
async def kick_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = f"**__Erreur kick !__**", description = f"**- La commande __kick__ prend en parametre un utilisateur et une raison !** \n\n **- Veuillez réessayer avec `-kick <membre> [raison]`.**", color = 0x206694)
            embed.set_thumbnail(url = "https://media.giphy.com/media/o7dsbpFQZwRxPSOOaz/giphy.gif")

            await ctx.send(embed = embed)


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = "**__Aucune raison n'a été renseignée !__**"):
	await member.ban(reason = reason)

	embed = discord.Embed(title = f"**__Ban effectué !__**", description = f"{member.mention} **a été __ban__ avec succès !** \n\n **Cause** : **{reason}** \n\n **Auteur** : **__{ctx.author}__** ", color = 0x206694)
	embed.set_thumbnail(url = "https://media.giphy.com/media/VmqjLOih0uhBBvMmrF/giphy.gif") 
    
	await ctx.send(embed = embed)

@ban.error
async def ban_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = f"**__Erreur ban !__**", description = f"**- La commande __ban__ prend en parametre un utilisateur et une raison !** \n\n **- Veuillez réessayer avec `-ban <membre> [raison]`.**", color = 0x206694)
            embed.set_thumbnail(url = "https://media.giphy.com/media/o7dsbpFQZwRxPSOOaz/giphy.gif")

            await ctx.send(embed = embed)


@bot.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user
  
  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)
    embed = discord.Embed(title = f"**__Unban effectué !__**", description = f"*{user}*  **a été __unban__ avec succès !** \n\n **Auteur** : **__{ctx.author}__** ", color = 0x206694)
    embed.set_thumbnail(url = "https://media.giphy.com/media/VmqjLOih0uhBBvMmrF/giphy.gif") 
    
    await ctx.send(embed = embed)
    return

@unban.error
async def unban_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = f"**__Erreur unban !__**", description = f"**- La commande __unban__ prend en parametre un utilisateur !** \n\n **- Veuillez réessayer avec `-unban <membre>`.**", color = 0x206694)
            embed.set_thumbnail(url = "https://media.giphy.com/media/o7dsbpFQZwRxPSOOaz/giphy.gif")

            await ctx.send(embed = embed)


@bot.command()
@commands.has_permissions(manage_channels = True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(title = f"**__Lock effectué !__**", description = ctx.channel.mention + f" **a été lock avec succès !**", color = 0x206694)
    embed.set_thumbnail(url = "https://media.giphy.com/media/LSFqQh5wSqjD2xhJIR/giphy.gif") 
    
    await ctx.send(embed = embed)


@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title = f"**__Unlock effectué !__**", description = ctx.channel.mention + f" **a été unlock avec succès !**", color = 0x206694)
    embed.set_thumbnail(url = "https://media.giphy.com/media/LSFqQh5wSqjD2xhJIR/giphy.gif")

    await ctx.send(embed = embed)

class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []
    channel = ctx.author.voice.channel
    channelMention = channel.mention
    embed = discord.Embed(title = f"**:stop_button: ・ Déconnection en cours...**", description = f"**Je me déconnecte de ** __{channelMention}__. \n\n *Si tu veux une autre musique  `-play <url>`* ", color = 0x206694)
    embed.set_thumbnail(url = "https://media.giphy.com/media/loLjad4noNNNGUe0f1/giphy-downsized-large.gif")

    await ctx.send(embed = embed)

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()
    channel = ctx.author.voice.channel
    channelMention = channel.mention
    embed = discord.Embed(title = f"**:arrow_forward: ・ Resume...**", description = f"**Je relance la musique dans ** __{channelMention}__. \n\n *Si tu veux mettre la pause `-pause`* ", color = 0x206694)
    embed.set_thumbnail(url = "https://media.giphy.com/media/loLjad4noNNNGUe0f1/giphy-downsized-large.gif")
    
    await ctx.send(embed = embed)  

@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()
    channel = ctx.author.voice.channel
    channelMention = channel.mention
    embed = discord.Embed(title = f"**:pause_button: ・ Pause...**", description = f"**Je suis en pause dans ** __{channelMention}__. \n\n *Si tu veux remettre la musique `-resume`* ", color = 0x206694)
    embed.set_thumbnail(url = "https://media.giphy.com/media/loLjad4noNNNGUe0f1/giphy-downsized-large.gif")

    await ctx.send(embed = embed)  


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def play(ctx, url):
    print("play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        server = ctx.guild
        channelMention = channel.mention
        embed = discord.Embed(title = f"**:play_pause: ・ Lecture en cours...**", description = f"**Je lance la musique dans** __{channelMention}__. \n\n *url :* ||{(url)}|| ", color = 0x206694)
        embed.set_thumbnail(url = "https://media.giphy.com/media/loLjad4noNNNGUe0f1/giphy-downsized-large.gif")
        
        await ctx.send(embed = embed)

        play_song(client, musics[ctx.guild], video)

@play.error
async def play_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = f"**__Erreur play !__**", description = f"**- La commande __play__ prend en parametre une url !** \n\n **- Veuillez réessayer avec `-play (url)`.**", color = 0x206694)
            embed.set_thumbnail(url = "https://media.giphy.com/media/o7dsbpFQZwRxPSOOaz/giphy.gif")

            await ctx.send(embed = embed)


@bot.command()
async def setupmusic(ctx):
	server = ctx.guild
	serverName = server.name
	embed = discord.Embed(title = f"**__{serverName} | Aide Music__**", description = ":construction: Prefix : `-` \n :recycle: En cours développement !", color = 0x206694)
	embed.set_thumbnail(url = "https://media.giphy.com/media/l0Exezf44dEdueHRK/giphy.gif")
	embed.add_field(name = "> Musique", value = "`-play (url)` \n *Permet de lancer une musique dans le channel connecté* \n\n `-pause` \n *Permet de mettre pause à la musique* \n\n `-resume` \n *Permet de relancer la musique* \n\n `-leave` \n *Permet de déconnecter la musique*", inline = True)


	await ctx.send(embed = embed)

@bot.command()
async def addrole(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        embed = discord.Embed(title = f"**__Addrole effectué !__**", description = f"**Le role __{role.mention}__ a été ajouté à {user} !** \n\n **Auteur** : **__{ctx.author}__**", color = 0x206694)
        embed.set_thumbnail(url = "https://media.giphy.com/media/H5I4jTmQ9mpaFwiMAf/giphy.gif")

        await ctx.send(embed = embed)

@addrole.error
async def addrole_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = f"**__Erreur addrole !__**", description = f"**- La commande __addrole__ prend en parametre un role et un utilisateur !** \n\n **- Veuillez réessayer avec `-addrole <rôle> <member>`.**", color = 0x206694)
            embed.set_thumbnail(url = "https://media.giphy.com/media/o7dsbpFQZwRxPSOOaz/giphy.gif")

            await ctx.send(embed = embed)

@bot.command()
async def removerole(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        embed = discord.Embed(title = f"**__Removerole effectué !__**", description = f"**Le role __{role.mention}__ a été retiré à {user} !** \n\n **Auteur** : **__{ctx.author}__**", color = 0x206694)
        embed.set_thumbnail(url = "https://media.giphy.com/media/H5I4jTmQ9mpaFwiMAf/giphy.gif")

        await ctx.send(embed = embed)

@removerole.error
async def removerole_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title = f"**__Erreur removerole !__**", description = f"**- La commande __removerole__ prend en parametre un role et un utilisateur !** \n\n **- Veuillez réessayer avec `-removerole <rôle> <member>`.**", color = 0x206694)
            embed.set_thumbnail(url = "https://media.giphy.com/media/o7dsbpFQZwRxPSOOaz/giphy.gif")

            await ctx.send(embed = embed)

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Citoyen')
    await member.add_roles(role)



bot.run ("OTMzNzczMDk5OTE5MzQzNjU2.YemZ9w.TYVxjVWm3EwL8xC6XlMx8fRGpho")
