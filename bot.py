import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from logger import logger

load_dotenv()


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    TOKEN = os.getenv("TOKEN")
    client = commands.Bot(command_prefix="/", intents=intents)

    @client.event
    async def on_ready():
        try:
            synced = await client.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @client.tree.command(name="signals_info")
    async def signals_info(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        pinned_messages = await interaction.channel.pins()

        if len(pinned_messages) == 0:
            await interaction.followup.send("There are no pinned messages in this channel")
            return

        signals_message = ""
        embed_list = []

        for msg in pinned_messages:
            msg_content = msg.content

            try:
                index = msg_content.index("\n")
            except ValueError:
                index = None

            formatted_msg = msg_content[:msg_content.index("\n")] + "\n" if index else msg_content + "\n"
            formatted_msg = formatted_msg.replace("*️⃣", ":asterisk:")

            if (len(signals_message) + len(formatted_msg)) < 1000:
                signals_message += formatted_msg
                continue

            embed_list.append(signals_message)
            signals_message = ""
            signals_message += formatted_msg

        if len(signals_message) > 0:
            embed_list.append(signals_message)

        embed_var = discord.Embed(title="Pinned signals", description=f"Total count: {len(pinned_messages)}", color=0x00ff00)

        count = 1
        for val in embed_list:
            embed_var.add_field(name=f"Part {count}", value=val, inline=False)
            count += 1

        await interaction.followup.send(embed=embed_var)

    client.run(TOKEN)
