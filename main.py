import discord
from discord.ext import commands
import requests
import os
from datetime import datetime

# ═══════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
PASTEBIN_API_KEY = os.environ.get('PASTEBIN_API_KEY')
PASTEBIN_PASTE_ID = os.environ.get('PASTEBIN_PASTE_ID')

# Webhook for logging
WEBHOOK_URL = "https://ptb.discord.com/api/webhooks/1465439453068656733/B7yTKmZWeK63NLbj39dzhjvCR6beqguupeQXru-YZMT9h9_g87jV_EHHn8mYOp49duCr"

# ═══════════════════════════════════════
# BOT SETUP
# ═══════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def update_pastebin(command):
    """Update Pastebin with new command"""
    url = "https://pastebin.com/api/api_post.php"
    data = {
        'api_dev_key': PASTEBIN_API_KEY,
        'api_option': 'paste',
        'api_paste_code': command,
        'api_paste_private': '1',
        'api_paste_name': 'roblox_command',
        'api_paste_expire_date': '10M',
    }
    
    try:
        response = requests.post(url, data=data)
        return response.text
    except Exception as e:
        print(f"Error updating pastebin: {e}")
        return None

def send_webhook_log(title, description, color=3447003):
    """Send log to Discord webhook"""
    payload = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Webhook error: {e}")

@bot.event
async def on_ready():
    print(f'Bot online as {bot.user}')
    send_webhook_log("Bot Online", f"Bot **{bot.user.name}** is now running!", 5763719)

# ═══════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════

@bot.command()
async def poison(ctx, player_name: str, damage: int = 100):
    """Poison a player across all servers"""
    command = f"poison|{player_name}|{damage}"
    result = update_pastebin(command)
    
    if result:
        await ctx.send(f"Sending poison command for **{player_name}** ({damage} damage)")
        send_webhook_log("Poison Command", f"Target: {player_name}\nDamage: {damage}", 15158332)
    else:
        await ctx.send("Failed to send command")

@bot.command()
async def track(ctx, user_id: int):
    """Start tracking a UserID"""
    command = f"track|{user_id}"
    update_pastebin(command)
    await ctx.send(f"Now tracking UserID: **{user_id}**")
    send_webhook_log("Track Added", f"Tracking UserID: {user_id}", 15105570)

@bot.command()
async def untrack(ctx, user_id: int):
    """Stop tracking a UserID"""
    command = f"untrack|{user_id}"
    update_pastebin(command)
    await ctx.send(f"Stopped tracking UserID: **{user_id}**")
    send_webhook_log("Track Removed", f"Stopped tracking: {user_id}", 10038562)

@bot.command()
async def serverlist(ctx):
    """Request list of all active servers"""
    command = "serverlist"
    update_pastebin(command)
    await ctx.send("Requesting server list from all accounts...")
    send_webhook_log("Server List", "Requested from all active accounts", 3066993)

@bot.command()
async def stats(ctx, player_name: str):
    """Get stats for a player"""
    command = f"stats|{player_name}"
    update_pastebin(command)
    await ctx.send(f"Requesting stats for **{player_name}**...")
    send_webhook_log("Stats Request", f"Player: {player_name}", 3447003)

@bot.command()
async def admin(ctx, *, command_text: str):
    """Execute admin command across all servers"""
    command = f"admin|{command_text}"
    update_pastebin(command)
    await ctx.send(f"Executing admin command: `{command_text}`")
    send_webhook_log("Admin Command", f"Command: {command_text}", 16776960)

@bot.command()
async def clear(ctx):
    """Clear the command queue"""
    update_pastebin("none")
    await ctx.send("🗑️ Command queue cleared")
    send_webhook_log("🗑️ Queue Cleared", "All pending commands removed", 7506394)

@bot.command(name='help')
async def help_command(ctx):
    """Show all available commands"""
    embed = discord.Embed(
        title="Roblox Command Bot",
        description="Available commands for controlling your Roblox accounts",
        color=5763719
    )
    
    embed.add_field(name="!poison <player> [damage]", value="Poison a player (default 100)", inline=False)
    embed.add_field(name="!track <userid>", value="Start tracking a UserID", inline=False)
    embed.add_field(name="!untrack <userid>", value="Stop tracking a UserID", inline=False)
    embed.add_field(name="!serverlist", value="Get list of active servers", inline=False)
    embed.add_field(name="!stats <player>", value="Get player stats", inline=False)
    embed.add_field(name="!admin <command>", value="Execute admin command", inline=False)
    embed.add_field(name="!clear", value="Clear command queue", inline=False)
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f" Missing argument. Use `!help` for command info")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f" Invalid argument. Use `!help` for command info")
    else:
        print(f"Error: {error}")

# ═══════════════════════════════════════
# RUN BOT
# ═══════════════════════════════════════
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("DISCORD_TOKEN not set!")
    elif not PASTEBIN_API_KEY:
        print("PASTEBIN_API_KEY not set!")
    elif not PASTEBIN_PASTE_ID:
        print("PASTEBIN_PASTE_ID not set!")
    else:
        bot.run(DISCORD_TOKEN)
