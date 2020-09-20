#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Discord Welcome Helper
  Copyright (C) 2020 Douile

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
from discord import Embed
from redbot.core import commands, checks, Config, utils

class WelcomeHelper(commands.Cog):
    """Welcome helper cog"""

    def __init__(self, bot):
        super(commands.Cog).__init__(self, bot)

    @commands.command()
    async def help(self, ctx):
        """Get help"""

        author = ctx.message.author

        # Check for DMs
        dm_channel = author.dm_channel
        try:
            dm_channel = await author.create_dm()
        except Exception as e:
            # Unable to create DM
            await ctx.send("Unable to find/create a DM please check your privacy settings")
            return

        await dm_channel.send(embed=Embed(title="Test"))
