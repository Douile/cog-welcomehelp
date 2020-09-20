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

DEFAULTS = dict(
    expire_time = 60 *5 # 5 minutes
)

class HelpSession:
    """Handles help sessions and their expiry"""

    _expire_task = None

    def __init__(self, channel, *, **kwargs):
        self.id = channel.id
        self._channel = channel
        self.expire_time = kwargs.get("expire_time", DEFAULTS.expire_time)
        self.current_menu = kwargs.get("current_menu", None)

    @property
    def is_expired(self):
        if self._expire_task is None:
            return False
        return self._expire_task.done()

    def expire_start(self):
        """Starts/Restarts session expiry"""
        if self.expire_task is not None and not self.is_expired:
            self._expire_task.cancel()
        self._expire_task = asyncio.create_task(self.expire_sleep())
        self._expire_task.add_done_callback(self.expire_end, context=self)

    def expire_end(self):
        """Runs when session expires"""
        print("Session {} expired".format(self.id))

    async def expire_sleep(self):
        await asyncio.sleep(self.expire_time)

    async def send_menu(self, menu):
        """ Sends a menu """
        self.expire_start() # Reset session expiry

        self.current_menu = menu
        await self._channel.send(embed=Embed(title="Gethelp menu",description="ID `{}`".format(self.id)))


class WelcomeHelper(commands.Cog):
    """Welcome helper cog"""

    _activehelp = dict()

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gethelp(self, ctx):
        """Get advanced server help"""

        author = ctx.message.author

        # Check for DMs
        dm_channel = author.dm_channel
        try:
            dm_channel = await author.create_dm()
        except Exception as e:
            # Unable to create DM
            await ctx.send("Unable to find/create a DM please check your privacy settings")
            return

        session = HelpSession(dm_channel, expire_time=30) # 30 second expiry for testing

        await dm_channel.send(embed=Embed(title="Test"))
