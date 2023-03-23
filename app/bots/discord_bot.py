import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user.name}")

@bot.command()
async def send_image(ctx, channel_id: int, image_path="tvl_over_time.png"):
    target_channel = bot.get_channel(int(channel_id))
    
    if target_channel is None:
        await ctx.send("Invalid channel ID. Please provide a valid channel ID.")
        return

    if not os.path.exists(image_path):
        await ctx.send("Image not found. Please provide a valid file path.")
        return

    _, file_extension = os.path.splitext(image_path)
    if file_extension.lower() not in [".png", ".jpg", ".jpeg", ".gif"]:
        await ctx.send("Invalid file format. Please provide a valid image file.")
        return

    try:
        with open(image_path, "rb") as f:
            picture = discord.File(f)
            await target_channel.send(file=picture)
    except Exception as e:
        print(f"Error sending image: {e}")
        await ctx.send("An error occurred while trying to send the image.")
        

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN)
