import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import time

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {levelname} {message}",
    style="{",
    datefmt="%m-%d-%y %H:%M:%S",
)

log = logging.getLogger()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!send_image", intents=intents)


@bot.event
async def on_ready():
    log.info(f"Bot is ready as {bot.user.name}")
    channel_id = int(os.getenv("CHANNEL_ID"))
    image_path = "tvl_over_time.png"

    target_channel = bot.get_channel(channel_id)

    if target_channel is None:
        log.info("Channel not found. Please check the channel ID.")
        return

    async for message in target_channel.history(limit=1):
        last_message = message
        log.info(f"Last message: {last_message.content}")
        break
    ctx = await bot.get_context(last_message)

    await send_image(ctx, channel_id, image_path)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    log.info(f"Message received: {message.content}")  # Debugging print statement

    await bot.process_commands(
        message
    )  # This line is important to process commands when using on_message


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    else:
        log.error(f"Error occurred: {error}")


@bot.command()
async def send_image(ctx, channel_id: int, image_path="tvl_over_time.png"):
    log.info("send_image command called")
    log.info(f"send image command called from {ctx.author} in {ctx.guild}")
    target_channel = bot.get_channel(int(channel_id))

    if target_channel is None:
        await ctx.send("Invalid channel ID. Please provide a valid channel ID.")
        return

    log.info(f"Channel found: {target_channel}")

    if not os.path.exists(image_path):
        await ctx.send("Image not found. Please provide a valid file path.")
        return

    log.info(f"Image found: {image_path}")

    _, file_extension = os.path.splitext(image_path)
    if file_extension.lower() not in [".png", ".jpg", ".jpeg", ".gif"]:
        await ctx.send("Invalid file format. Please provide a valid image file.")
        return

    try:
        with open(image_path, "rb") as f:
            picture = discord.File(f)
            await target_channel.send(file=picture)
        await stop_bot(ctx)
    except Exception as e:
        log.error(f"Sending image: {e}")
        await ctx.send("An error occurred while trying to send the image.")


@bot.command()
@commands.is_owner()
async def stop_bot(ctx):
    log.info("Stopping bot...")
    await bot.close()


if __name__ == "__main__":
    try:
        DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        log.error(f"Bot error: {e}")
        # continue
