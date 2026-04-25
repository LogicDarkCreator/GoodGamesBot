import disnake
from disnake.ext import commands


class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='rules', description='Shows rules for a user')
    async def rules(self, ctx):
        embed = disnake.Embed(
            title='📜 **Server Rules**',
            description="Violating the rules may result in a mute or ban.",
            color=disnake.Color.blue(),
            timestamp=ctx.message.created_at if ctx.message else disnake.utils.utcnow()
        )

        rules_text = {
            "1. Respect": "• Be respectful to participants and staff.\n• Prohibited: hatred, racism, sexual harassment, threats.\n• Don't nook or raid the server.",
            "2. Discussions": "• Don't create drama or bring up controversial topics.\n• Religion and politics are considered too provocative.",
            "3. Spamming": "• Spam is prohibited: cluttering chats, emoji spam, flooding.",
            "4. Privacy": "• Do not disclose personal information of participants publicly or in private messages.",
            "5. Language": "• This server is in English only.",
            "6. Advertisement": "• Advertising other servers/teams is prohibited.",
            "7. Respecting Staff": "• The staff has the final say. Respect them and avoid insults."
        }

        for title, description in rules_text.items():
            embed.add_field(name=title, value=description, inline=False)

        embed.set_footer(text='Requested by {}'.format(ctx.author), icon_url=ctx.author.avatar.url if
        ctx.author.avatar else None)

        await ctx.send(embed=embed)

    @commands.command(name="rules_embed", description="Send rules in perfect Embed to the specified channel")
    @commands.has_permissions(administrator=True)
    async def rules_embed(self, ctx, channel: disnake.TextChannel):
        embed = disnake.Embed(
            title="<:rules:> **Server Rules**",
            description="Please read the rules carefully before starting communication.",
            color=0x2B2D31
        )

        embed.add_field(
            name="`1` Respect",
            value="• Be respectful to members and staff.\n• No hate-speech, racism, harassment, threats.\n• No nuking or raiding.",
            inline=False
        )
        embed.add_field(
            name="`2` Discussions",
            value="• No unnecessary drama or controversial topics.\n• Religion and politics are forbidden.",
            inline=False
        )
        embed.add_field(
            name="`3` Spamming",
            value="• No spam, clogging chats, emoji spam, or flooding.",
            inline=False
        )
        embed.add_field(
            name="`4` Privacy",
            value="• Don't expose personal information of any member.",
            inline=False
        )
        embed.add_field(
            name="`5` Language",
            value="• English only in this server.",
            inline=False
        )
        embed.add_field(
            name="`6` Advertisement",
            value="• Team advertisement is not allowed.",
            inline=False
        )
        embed.add_field(
            name="`7` Respecting Staff",
            value="• Staff have the final say. Respect them and don't use offensive language.",
            inline=False
        )

        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_footer(text=f"Server: {ctx.guild.name}")

        await channel.send(embed=embed)
        await ctx.send(f"✅ Rules was sent to {channel.mention}.", ephemeral=True)

def setup(bot):
    bot.add_cog(Rules(bot))