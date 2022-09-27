import discord
from discord.ext import commands,tasks
from datetime import *
from discord.utils import get
import asyncio
from discord.emoji import Emoji
from discord import message

class moderation(commands.Cog):
    def __Init__(self,bot):
        self.bot=bot

           
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self,ctx,nombre:int):
        auteur=str(ctx.message.author)
        messages = await ctx.channel.history(limit = nombre + 1).flatten()
        chiffre=str(nombre)
        temps=str(datetime.now().strftime('%H:%M:%S'))
        date=str(datetime.now().strftime('%Y-%m-%d'))
        
        def LogsClear(auteur,temps,date,message):
            typeL="Clear"
            f=open("C:/Users/devre/Vs-Workspace/Bot_Discord/Logs/Logs.csv","a")
            f.write(f"{typeL};!clear {message};{auteur};{date};{temps}\n")
            f.close()
            
        LogsClear(auteur,temps,date,chiffre)        
        for message in messages :
            await message.delete()
            
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self,ctx, user : discord.User, *reason):
        auteur=ctx.message.author
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason = reason)
        await ctx.send(f"{user} à été kick.")
        
        temps=str(datetime.now().strftime('%H:%M:%S'))
        date=str(datetime.now().strftime('%Y-%m-%d'))
    
        def csvkicklogs(user,reason,temps,date):
            f=open("C:/Users/devre/Vs-Workspace/Bot_Discord/Logs/KickLogs.csv","a") 
            if reason=="":
                f.write(f"{user};////;{date};{temps}\n")
            else:
                f.write(f"{user};{reason};{date};{temps}\n")
            f.close()
            
        def LogsKick(auteur,temps,date,user,reason):
            typeL="Kick"
            f=open("C:/Users/devre/Vs-Workspace/Bot_Discord/Logs/Logs.csv","a")
            f.write(f"{typeL};!kick {user} {reason};{auteur};{date};{temps}\n")
            f.close()    
        LogsKick(auteur,temps,date,user,reason)  
        csvkicklogs(user,reason,temps,date)
    
    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self,ctx, user : discord.User, *reason):
        reason = " ".join(reason)
        auteur=ctx.message.author
        temps=str(datetime.now().strftime('%H:%M:%S'))
        date=str(datetime.now().strftime('%Y-%m-%d'))
    
        def csvbanlogs(user,reason,temps,date):
            f=open("C:/Users/devre/Vs-Workspace/Bot_Discord/Logs/BanLogs.csv","a") 
            if reason=="":
                f.write(f"{user};////;{date};{temps}\n")
            else:
                f.write(f"{user};{reason};{date};{temps}\n")
            f.close()
        
        
        def csvbanliste(user,reason,temps,date):
            f=open("C:/Users/devre/Vs-Workspace/Bot_Discord/Logs/BanListe.csv","a") 
            if reason=="":
                f.write(f"{user};////;{date};{temps}\n")
            else:
                f.write(f"{user};{reason};{date};{temps}\n")
            f.close()
        
        def LogsBan(auteur,temps,date,user,reason):
            typeL="Ban"
            f=open("C:/Users/devre/Vs-Workspace/Bot_Discord/Logs/Logs.csv","a")
            f.write(f"{typeL};!Ban {user} {reason};{auteur};{date};{temps}\n")
            f.close()    
        LogsBan(auteur,temps,date,user,reason) 
        csvbanliste(user,reason,temps,date)
        csvbanlogs(user,reason,temps,date)
        
        if reason=="":
            await ctx.send(f"{user} a été ban")
        else:
            await ctx.send(f"{user} a été ban pour la raison suivante : {reason}")
        
        await ctx.guild.ban(user, reason = reason)
        
    
        
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self,ctx , user , *reason):
        reason = " ".join(reason)
        auteur=ctx.message.author
        userName , userId = user.split ("#")
        bannedUsers = await ctx.guild.bans()
        
        temps=str(datetime.now().strftime('%H:%M:%S'))
        date=str(datetime.now().strftime('%Y-%m-%d'))
        
        def csvbanlisteremove(user):
            f=open("C:/Users/devre/Vs-Workspace/Bot_Discord/Logs/BanListe.csv","r") 
            lines=f.readlines()
            f.close()
            f=open("C:/Users/devre/Vs-Workspace/Bot_Discord/Logs/BanListe.csv","w") 
            for line in lines:
                if user not in line:
                    f.write(line)
            f.close()
        def LogsUnBan(auteur,temps,date,user,reason):
            typeL="Unban"
            f=open("C:/Users/devre/Vs-Workspace/Bot_Discord/Logs/Logs.csv","a")
            f.write(f"{typeL};!Ban {user} {reason};{auteur};{date};{temps}\n")
            f.close()    
            
 
                  
        for i in bannedUsers:
            if i.user.name == userName and i.user.discriminator == userId:
                await ctx.guild.unban(i.user, reason = reason)
                await ctx.send (f"{user} a été unban")
                LogsUnBan(auteur,temps,date,user,reason) 
                csvbanlisteremove(user)
                return
        await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")
        
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def tempmute(self,ctx, member : discord.Member, minutes : int,*reason):
        reason = " ".join(reason)
        auteur=ctx.message.author
        async def get_muted_role(guild : discord.Guild) -> discord.Role:
            role = get(guild.roles, name="Mute")
            if role is not None:
                return role
            else:
                permissions = discord.Permissions(send_messages=False,speak=False)
                role = await guild.create_role(name="Mute", permissions=permissions)
                return role
            
        temps=str(datetime.now().strftime('%H:%M:%S'))
        date=str(datetime.now().strftime('%Y-%m-%d'))
        
        def csvmutelogs(auteur,user,reason,temps,date):
            f=open("C:/Users/devre/Vs-Workspace/Bot_Discord/Logs/MuteLogs.csv","a") 
            if reason=="":
                f.write(f"{auteur};{user};////;{date};{temps};{minutes}\n")
            else:
                f.write(f"{auteur};{user};{reason};{date};{temps};{minutes}\n")
            f.close()
            
        def Logsmute(auteur,temps,date,user,reason,minutes):
            typeL="Mute"
            f=open("C:/Users/devre/Vs-Workspace/Bot_Discord/LogsLogs.csv","a")
            f.write(f"{typeL};!tempmute {user} {minutes} {reason};{auteur};{date};{temps};{minutes}\n")
            f.close()    
        Logsmute(auteur,temps,date,member,reason,minutes)  
        csvmutelogs(auteur,member,reason,temps,date)
        
        muted_role = await get_muted_role(ctx.guild)
        await member.add_roles(muted_role)
        if reason=="":
            await ctx.send(f"{member.mention} a été muté pour un durée de {minutes} minutes! 🎙")
        else :
            await ctx.send(f"{member.mention} a été muté pour un durée de {minutes} minutes! 🎙\n Pour la raison : {reason}")
        await asyncio.sleep(minutes*60)
        await member.remove_roles(muted_role)
        

    # role react

    @commands.command()
    async def role (self,ctx,*message): 
            role_id = ctx.message.raw_role_mentions
            async def get_role(roleId,guild : discord.Guild) -> discord.Role:
                role = get(guild.roles, id=role_id[0])
                return role
            roleptet=get_role(role_id,ctx.guild)
            roles = discord.utils.get(ctx.guild.roles, id=role_id)
            return await ctx.send(type(roleptet))
        
    @commands.command()
    async def emoticon(self,ctx,*message):
        for emoji in ctx.message.guild.emojis:
            for emoji in ctx.message.guild.emojis:
                if str(emoji) in  ctx.message.content:
                    emote = str(emoji)
                    return await ctx.send(emote)
    
        
    @commands.command()
    async def message(self,ctx,*message):
        return await ctx.send(message[1])