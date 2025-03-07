import discord
import os
import requests
import asyncio
from datetime import datetime, timezone, timedelta
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

# Load tokens and URLs
TOKEN = os.getenv('TOKEN')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)
reminders = []
IST = timezone(timedelta(hours=5, minutes=30))  # Define IST timezone

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    reminder_checker.start()

async def get_gemini_response(user_message):
    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        json={"contents": [{"parts": [{"text": user_message}]}]},
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        gemini_response = response.json()
        reply = gemini_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No reply from Gemini.")
        return reply
    else:
        return f'Error connecting to Gemini API: {response.status_code} - {response.text}'

async def send_long_message(channel, message):
    """Splits long messages into multiple parts and sends them."""
    for i in range(0, len(message), 2000):
        await channel.send(message[i:i+2000])

@tasks.loop(seconds=60)
async def reminder_checker():
    """Check for reminders and notify users."""
    now = datetime.now(IST)  # Ensure timezone-aware datetime in IST
    for reminder in reminders[:]:
        if now >= reminder['time']:
            user = bot.get_user(reminder['user_id'])
            if user:
                await user.send(f"⏰ Reminder: {reminder['message']}")
            reminders.remove(reminder)

@bot.command()
async def set_reminder(ctx, date: str, time: str, *, message: str):
    """Set a reminder (format: YYYY-MM-DD HH:MM IST)."""
    try:
        reminder_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)
        reminders.append({"user_id": ctx.author.id, "time": reminder_time, "message": message})
        await ctx.send(f"Reminder set for {date} {time} IST: {message}")
    except ValueError:
        await ctx.send("Invalid date/time format. Use YYYY-MM-DD HH:MM IST.")

@bot.command()
async def modify_reminder(ctx, index: int, date: str, time: str, *, message: str):
    """Modify an existing reminder by index."""
    user_reminders = [r for r in reminders if r['user_id'] == ctx.author.id]
    if 0 <= index < len(user_reminders):
        try:
            new_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)
            user_reminders[index]['time'] = new_time
            user_reminders[index]['message'] = message
            await ctx.send(f"Reminder updated to: {date} {time} IST - {message}")
        except ValueError:
            await ctx.send("Invalid date/time format. Use YYYY-MM-DD HH:MM IST.")
    else:
        await ctx.send("Invalid reminder index.")

@bot.command()
async def list_reminders(ctx):
    """List all active reminders."""
    user_reminders = [r for r in reminders if r['user_id'] == ctx.author.id]
    if not user_reminders:
        await ctx.send("No active reminders.")
        return

    reminder_list = "\n".join([f"{i}. {r['time']} IST - {r['message']}" for i, r in enumerate(user_reminders)])
    await send_long_message(ctx.channel, f"Your active reminders:\n{reminder_list}")

@bot.command()
async def delete_reminder(ctx, index: int):
    """Delete a specific reminder by index."""
    user_reminders = [r for r in reminders if r['user_id'] == ctx.author.id]
    if 0 <= index < len(user_reminders):
        reminders.remove(user_reminders[index])
        await ctx.send("Reminder deleted successfully.")
    else:
        await ctx.send("Invalid reminder index.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Respond to messages that start with "$bot"
    if message.content.lower().startswith("$bot"):
        user_message = message.content[4:].strip()
        response = await get_gemini_response(user_message)
        await send_long_message(message.channel, response)
        return  # Prevent further command processing

    # Process bot commands
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    """Responds with a greeting."""
    await ctx.send(f'You have my respect, {ctx.author.name}!')

@bot.command()
async def summarize(ctx, *, text: str):
    """Summarize a long message using Gemini AI."""
    summary = await get_gemini_response(f"Summarize this text: {text}")
    await send_long_message(ctx.channel, summary)

@bot.event
async def on_member_join(member):
    """Sends a custom welcome message when a new member joins."""
    welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if welcome_channel:
        await welcome_channel.send(f"Welcome to the Jabari, {member.mention}! we heard praises of you from M'Baku!")

@bot.command()
async def poll(ctx, question: str, *options: str):
    """Create a poll with reactions."""
    if len(options) < 2:
        await ctx.send("Even the wisest choices require at least two!")
        return

    embed = discord.Embed(title=question, description="\n".join([f"{chr(65 + i)}. {option}" for i, option in enumerate(options)]))
    message = await ctx.send(embed=embed)

    reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯']  # Supports up to 10 options

    for i in range(len(options)):
        await message.add_reaction(reactions[i])

bot.run(TOKEN)
