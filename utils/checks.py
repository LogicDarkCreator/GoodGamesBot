from disnake.ext import commands

def is_moderator():
    async def predicate(ctx):
        return ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.kick_members
    return commands.check(predicate)

def is_admin():
    return commands.has_permissions(administrator=True)