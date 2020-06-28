import discord
from pprint import pprint
import os
from os.path import join, dirname
from dotenv import load_dotenv

from service.kintai_service import KintaiService

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Client(discord.Client):
    def __init__(self, *, loop=None, **options):
        super().__init__()
        self.kintai_service = KintaiService()
        self.channed_id = int(os.environ.get("CHANNEL_ID"))

    async def on_ready(self):
        print('bot started 👀')

    async def on_voice_state_update(self, member, before, after):

        if (before.channel is None):
            try:
                self.kintai_service.start(member, after)
                await self.success_reaction(member)
            except IndexError:
                await self.fail_reaction(member)
        elif (after.channel is None):
            try:
                self.kintai_service.end(member, before)
                await self.success_reaction(member, True)
            except IndexError:
                await self.fail_reaction(member)

    async def success_reaction(self, member, is_end=False):
        channel = self.get_channel(self.channed_id)
        async for msg in channel.history(limit=10):
            if msg.author == member:
                await msg.add_reaction(
                    "👍") if is_end else await msg.add_reaction("👀")
                break

    async def fail_reaction(self, member):
        channel = self.get_channel(self.channed_id)
        async for msg in channel.history(limit=10):
            if msg.author == member:
                await msg.add_reaction("💔")
                break


if __name__ == "__main__":
    client = Client()
    client.run(os.environ.get("BOT_KEY"))