import asyncio

import disnake
from disnake.ext import commands
from datetime import datetime, timedelta
from utils.checks import is_moderator


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="kick", description="Kick a user")
    @is_moderator()
    async def kick(self, ctx, member: disnake.Member, reason: str = "No reason provided"):
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.respond("❌ You can't kick this user", ephemeral=True)
            return

        await member.kick(reason=reason)
        embed = disnake.Embed(
            title="✅ Kick",
            description=f"{ctx.guild.name} has been kicked",
            color=disnake.Color.orange()
        )
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.slash_command(name="ban", description="Ban a user")
    @is_moderator()
    async def ban(self, ctx, member: disnake.Member, reason: str = "No reason provided"):
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.respond("❌ You can't ban this user", ephemeral=True)
            return

        await member.ban(reason=reason)
        embed = disnake.Embed(
            title="✅ Ban",
            description=f"{ctx.guild.name} has been banned",
            color=disnake.Color.red()
        )
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.slash_command(name="mute", description="Mute a user")
    @is_moderator()
    async def mute(self, ctx, member: disnake.Member, duration: int, unit: str ="min", reason: str = "No reason provided"):
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")

        if not mute_role:
            mute_role = ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False, add_reactions=False, connect=False)

        if mute_role in member.roles:
            await ctx.send("❌ User is already muted", ephemeral=True)
            return

        await member.add_roles(mute_role, reason=reason)

        # Time convertation
        if unit in ["s"]:
            delta = timedelta(seconds=duration)
        elif unit in ["h"]:
            delta = timedelta(hours=duration)
        elif unit in ["d"]:
            delta = timedelta(days=duration)
        else:
            delta = timedelta(minutes=duration)

        unmute_time = datetime.now() + delta

        embed = disnake.Embed(
            title="🔇 Mute",
            description=f"{ctx.guild.name} has been muted",
            color=disnake.Color.gold()
        )
        embed.add_field(name="duration", value=f"{duration}{unit}")
        embed.add_field(name="Reason", value=reason)
        embed.add_field(name="Unmute in", value=f"<t:{int(unmute_time.timestamp())}:R>")
        await ctx.send(embed=embed)

        # Asynchronous removal of mute
        await self.unmute_after_delay(member, mute_role, delta, ctx.guild.id)

    async def unmute_after_delay(self, member, mute_role, delta, guild_id):
        await asyncio.sleep(delta.total_seconds())
        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(member.id) if guild else None
        if member and mute_role in member.roles:
            await member.remove_roles(mute_role)

    @commands.slash_command(name="unmute", description="Unmute a user")
    @is_moderator()
    async def unmute(self, ctx, member: disnake.Member):
        mute_role = disnake.utils.get(ctx.guild.roles, name="Muted")
        if mute_role and mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"✅ {member.mention} has been unmuted", ephemeral=False)
        else:
            await ctx.send("❌ User is not muted", ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))