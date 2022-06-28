from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

import discord
from core.functions import confirm
from discord.enums import Status
from discord.ext import commands
from discord.ext.commands.context import Context

if TYPE_CHECKING:
    from main import ModularBot


class Owner(commands.Cog):
    "Owner commands"

    def __init__(self, bot: "ModularBot"):
        self.bot = bot

    @commands.command(name="shutdown", help="Terminate the process", pass_context=True)  # type: ignore
    @commands.is_owner()
    async def shutdown(self, ctx: Context):
        confirmed = await confirm(self.bot, ctx, "Terminate process ?")
        if not confirmed:
            return

        logging.warning("Shutting down bot")
        embed = discord.Embed(
            colour=0x00ff00,
            description="✅ Shutting down..."
        )
        embed.set_author(name="Shutdown", icon_url=self.bot.avatar_url)
        await ctx.send(embed=embed)
        logging.info("Shutting down...")

        await self.bot.change_presence(activity=discord.Game(name=f"Shutting down..."), status=Status.offline)
        sys.exit()

    @commands.is_owner()
    @commands.command(name="eval", help="Evaluate string", pass_context=True)  # type: ignore
    async def eval(self, ctx: Context, *, message: str):
        if self.bot.enable_rce:
            try:
                await ctx.send(eval(message))
            except Exception as e:
                await ctx.send(e)
        else:
            await ctx.send("RCE disabled by default")

    @commands.is_owner()
    @commands.command(name="exec", help="Execute string", pass_context=True)  # type: ignore
    async def exec(self, ctx: Context, *, message: str):
        if self.bot.enable_rce:
            try:
                await ctx.send(exec(message))
            except Exception as e:
                await ctx.send(e)
        else:
            await ctx.send("RCE disabled by default")

def setup(bot: "ModularBot"):
    bot.add_cog(Owner(bot))
