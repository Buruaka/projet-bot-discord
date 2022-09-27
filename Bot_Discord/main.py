import discord
from discord import role
from discord.ext import commands
from discord.utils import get
from datetime import *
from random import randint
import Moderation
import asyncio
#Lancement du bot
bot = commands.Bot(command_prefix = "!", description = "Le Bot de Bura")

@bot.event
async def on_ready():
    print("ready !")
    
#commande stats
@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    numberOfPerson = server.member_count
    serverDescription = server.description
    serverName = server.name
    message= f"Le serveur **{serverName}** contient {numberOfPerson} personnes.\n{serverDescription}\nCe serveur possède {numberOfTextChannels} salons écrit ainsi que {numberOfVoiceChannels} vocaux"
    await ctx.send(message)


#Commande modo                

        

@bot.command()
async def survey(ctx, *message):
    auteur=str(ctx.message.author)
    cpt=1
    
    def checkMessage(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel
    
    txt = " ".join(message)
        
    if txt =="" or txt == " " :
        cpt+2
        await ctx.send(f"{auteur} écris ton sondage ")
        try: 
            message = await bot.wait_for("message", check = checkMessage, timeout = 180)
            cpt += 1
        except:
            messages = await ctx.channel.history(limit = cpt).flatten()
            for message in messages :
                await message.delete()
            return await ctx.send(f"{auteur} le sondage est annulé tu as mis trop de temps ")
    if txt =="help":
        return await ctx.send("__Voici le fonctionnement de la commande survey:__\n\n La commande **!survey** permet de créer des sondages jusqu'à 10 choix différents\nIl faut écrire !survey et le sujet du sondage à la suite \nEnsuite écrire message par message **chaques choix** possible\nPour limité le nombre de choix dans le sondage, après avoir écris tous les choix, il faut envoyé le message **fin**,\nEnsuite le bot supprimera automatiquement les message de commande et en enverra un nouveau plus propre et avec des réactions\n\nTous le monde pourra ensuite réagir au sondage ")
    choiceList =[]
    choiceMessage=""
    reactList= ["1️⃣", "2️⃣", "3️⃣" ,"4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟" ]
    choice = ""

    while choice!= "fin" and len(choiceList) < 10:
        try:    
            choice = await bot.wait_for("message", check = checkMessage, timeout = 180)
            if choice.content == "fin":
                break
            else:
                choiceList.append(choice.content)
                cpt += 1   
        except:
            messages = await ctx.channel.history(limit = cpt).flatten()
            for message in messages :
                await message.delete()
            return await ctx.send(f"{auteur} le sondage est annulé tu as mis trop de temps ")  
            
        
    for i in range(len(choiceList)):
        choiceMessage = choiceMessage + f"{reactList[i]} {choiceList[i]}\n"
    if choice.content=="fin":
        cpt +=1
    messages = await ctx.channel.history(limit = cpt).flatten()
    for message in messages :
        await message.delete()
    messageSondage = await ctx.send(f"**{auteur}** a lancé un nouveau sondage:\n**__{txt}__**\n\n{choiceMessage}\n Vous pouvez répondre grâce aux réactions")

    for i in range (len(choiceList)):
        await messageSondage.add_reaction(reactList[i])
    return


#commandes Jeux

@bot.command()
async def roll(ctx, *message):
    auteur=str(ctx.message.author)
    txt = " ".join(message)
    
    
    if txt=="help":
        return await ctx.send("__Voici le fonctionnement de la commande roll:__\n\nLa commande **!roll** sert à choisir un nombre aléatoire entre 1 et 100 si aucun nombre n'a était choisi\n Par contre si un nombre est choisi l'intervalle sera de 1 au nombre voici quelques exemples:\n !roll = entre 1 et 100\n !roll 1000 = entre 1 et 1000")
    
    if txt=="":
        count=100
        res=randint(1,count)
        return await ctx.send(f"{auteur} a roll {res} sur {count}")
    elif txt.isdigit()==False:
        return await ctx.send(f"{auteur} tu à mal écris la commande recommence ou envois !roll help")
    else:
        count= int(txt)
        res=randint(1,count)
        return await ctx.send(f"{auteur} a roll {res} sur {count}")

#role react

@bot.command()
@commands.has_permissions(manage_roles = True)
async def rolereact(ctx,*message):
    cpt=1
    def checkMessage(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel

        
    def getRole(ctx,message):
        role_id = message
        async def get_role(roleId,guild : discord.Guild) -> discord.Role:
            role = get(guild.roles, id=role_id[0])
            return role
        rolef=get_role(role_id,ctx.guild)
        return rolef

    def getEmote(ctx,message) :
        for emoji in ctx.message.guild.emojis:
            if str(emoji) in  message:
                emote = str(emoji)
                return emote
                 

    sujet = " ".join(message)
    if sujet =="help":
        return await ctx.send("__Voici le fonctionnement de la commande rolereact :__\n\n La commande **!survey** permet de s'ajouter un role en réagissant au message du bot\nIl faut écrire !rolereact l'emote puis le message à la suite \nEnsuite écrire message par message **chaques role** possible\nPour mettre fin à la commande, après avoir écris tous les roles, il faut envoyé le message **fin**,\nEnsuite le bot supprimera automatiquement tous les message de la commande et en enverra un nouveau plus propre et avec des réactions\n\nTous le monde pourra ensuite réagir")
    messageList = []
    emoteList = []
    roleList = []
    react=""
    while react!= "fin":
        
        react= await bot.wait_for("message", check = checkMessage, timeout = 180)

        if react.content == "fin":
            cpt+=1
            break
        else:
    
            text=react.content
            messageList.append(text)
            emoteList.append(getEmote(ctx,text))
            roleList.append(getRole(ctx,text))
            cpt += 1 
              
    reactMessage=""
    for i in range(len(messageList)):
        reactMessage = reactMessage + f" {messageList[i]}\n"
 
    messages = await ctx.channel.history(limit = cpt).flatten()
    for message in messages :
        await message.delete()
    messageRoleReact= await ctx.send(f"@everyone\n Des nouveaux roles sont disponibles:\n **__{sujet}__** \n\n {reactMessage} \n Vous pouvez répondre grâce aux réactions")

    for i in range (len(messageList)):
        await messageRoleReact.add_reaction(emoteList[i])


    async def on_raw_reaction_event(ctx,reactevent:discord.RawReactionActionEvent,roleList,messageId):
        messageId=messageRoleReact.id
        if reactevent.message_id == messageId:
            roleEmoji = reactevent.emoji
            roleEmojiId = emoteList.index(roleEmoji)
            print(roleEmojiId)


#@bot.command()
#async def  morpion(ctx, *message):
    
    

    
#execution bot
bot.add_cog(Moderation.moderation(bot))
bot.run("ODM0OTI3OTY4NzQ4MzA2NDMy.YIIBQw.QpG0II3cWUe4r9lK5VmRv-WQwQk")
    