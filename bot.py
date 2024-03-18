import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

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
            print(f"Synced {len(synced)} command(s)")
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

        for msg in pinned_messages:
            string = msg.content
            signals_message += string[:string.index("\n")] + "\n"

        signals_message = signals_message.replace("*️⃣", ":asterisk:")
        await interaction.followup.send(signals_message)

    client.run(TOKEN)
