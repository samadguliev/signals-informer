import os
import discord
import asyncio
import re
from dotenv import load_dotenv
from discord.ext import commands
from logger import logger
from models import Signal
from scheduler.tasks import update_prices
from telegram_logger import TelegramErrorLogger

load_dotenv()


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    TOKEN = os.getenv("TOKEN")
    client = commands.Bot(command_prefix="/", intents=intents)
    mutex = asyncio.Lock()
    telegram_logger = TelegramErrorLogger(os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID"))

    @client.event
    async def on_ready():
        try:
            synced = await client.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
            telegram_logger.send_message(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(e)
            telegram_logger.log_error(e)

    async def get_pinned_messages(channel) -> list[Signal]:
        signals = Signal.get_by_channel(channel.id)
        if len(signals) != 0:
            return signals
        return await init_table(channel)

    async def init_table(channel) -> list[Signal]:
        try:
            Signal.clear_table(channel.id)
            logger.info("Table is empty")

            pinned_messages = await channel.pins()
            if len(pinned_messages) == 0:
                return []

            messages: list[Signal] = []
            for msg in pinned_messages:
                msg_content = msg.content

                try:
                    index = msg_content.index("\n")
                except ValueError:
                    index = None

                formatted_msg = msg_content[:msg_content.index("\n")] if index else msg_content
                formatted_msg = formatted_msg.replace("*️⃣", ":asterisk:")

                signal = Signal(channel=channel.id, text=formatted_msg, currency_code="")
                match = re.search(r"\b\w+\b", formatted_msg)
                if match:
                    currency_code = match.group()
                    signal.currency_code = currency_code

                messages.append(signal)

            logger.info("Init is finished")
            Signal.create_signals(messages)
            update_prices.delay()

            signals_res = Signal.get_by_channel(channel.id)

            telegram_msg_arr = [item.text for item in signals_res]
            telegram_msg = "\n".join(telegram_msg_arr)
            telegram_logger.send_message(telegram_msg)

            return signals_res

        except Exception as e:
            logger.error(e)
            telegram_logger.log_error(e)

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
            msg_text = msg.text
            if hasattr(msg, "currency"):
                msg_text += ", **Price: " + str(msg.currency.price) + "**"
            msg_text += "\n"

            if (len(signals_message) + len(msg_text)) < 1000:
                signals_message += msg_text
                continue

            embed_list.append(signals_message)
            signals_message = ""
            signals_message += msg_text

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
