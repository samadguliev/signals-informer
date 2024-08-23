import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from logger import logger
from models import Signal

load_dotenv()


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    TOKEN = os.getenv("TOKEN")
    client = commands.Bot(command_prefix="/", intents=intents)
    mutex = asyncio.Lock()

    @client.event
    async def on_ready():
        try:
            synced = await client.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(e)

    async def get_pinned_messages(channel) -> list[Signal]:
        signals = Signal.get_all()
        if len(signals) != 0:
            return signals
        return await init_table(channel)

    async def init_table(channel) -> list[Signal]:
        try:
            Signal.clear_table()
            logger.info("Table is empty")

            pinned_messages = await channel.pins()
            if len(pinned_messages) == 0:
                return []

            messages: list[str] = []
            for msg in pinned_messages:
                msg_content = msg.content

                try:
                    index = msg_content.index("\n")
                except ValueError:
                    index = None

                formatted_msg = msg_content[:msg_content.index("\n")] + "\n" if index else msg_content
                formatted_msg = formatted_msg.replace("*️⃣", ":asterisk:")
                messages.append(formatted_msg)

            logger.info("Init is finished")
            return Signal.create_signals(messages)

        except Exception as e:
            logger.error(e)

    @client.event
    async def on_guild_channel_pins_update(channel, last_pin):
        async with mutex:
            await init_table(channel)

    @client.tree.command(name="signals_info")
    async def signals_info(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        async with mutex:
            pinned_messages = await get_pinned_messages(interaction.channel)

        if len(pinned_messages) == 0:
            await interaction.followup.send("There are no pinned messages in this channel")
            return

        signals_message = ""
        embed_list = []

        for msg in pinned_messages:
            if (len(signals_message) + len(msg.text)) < 1000:
                signals_message += msg.text
                continue

            embed_list.append(signals_message)
            signals_message = ""
            signals_message += msg.text

        if len(signals_message) > 0:
            embed_list.append(signals_message)

        embed_var = discord.Embed(title="Pinned signals", description=f"Total count: {len(pinned_messages)}",
                                  color=0x00ff00)

        count = 1
        for val in embed_list:
            embed_var.add_field(name=f"Part {count}", value=val, inline=False)
            count += 1

        await interaction.followup.send(embed=embed_var)

    client.run(TOKEN)
