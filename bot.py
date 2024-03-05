import discord
from discord.ext import commands


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    TOKEN = ""
    client = commands.Bot(command_prefix="/", intents=intents)

    @client.event
    async def on_ready():
        # print(f'{client.user} is now running!')
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

    # @client.command(name="signals_info")
    # async def signals_info(ctx):
    #     await ctx.send("asd")

    # @client.event
    # async def on_message(message):
    #     username = str(message.author)
    #     user_message = str(message.content)
    #     channel = str(message.channel)
    #
    #     # print(f"{username} said: '{user_message}' ({channel})")
    #
    #     if message.author == client.user:
    #         return
    #
    #     if message.content != "/signals_info":
    #         return
    #
    #     pinned_messages = [msg for msg in await message.channel.pins()]
    #     signals_message = ""
    #
    #     for msg in pinned_messages:
    #         string = msg.content
    #         signals_message += string[:string.index("\n")] + "\n"
    #
    #     signals_message = signals_message.replace("*️⃣", ":asterisk:")
    #     await message.channel.send(content=signals_message, mention_author=True)

    client.run(TOKEN)
