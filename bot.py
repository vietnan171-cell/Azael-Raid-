import discord
from discord.ext import commands
from discord import app_commands
import os
from colorama import init, Fore, Style

init(autoreset=True)

# Função para pegar o token direto da variável de ambiente
def load_token():
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print(Fore.RED + "❌ Error: Discord token not found in environment variables.")
    return token

def display_logo():
    logo = '''
░░█ ▄▀█ █▀▀ █▄▀ █▀█ █▀ █▀█ ▄▀█ █▀▄▀█
█▄█ █▀█ █▄▄ █░█ █▄█ ▄█ █▀▀ █▀█ █░▀░█ 
'''
    print(Fore.BLUE + logo)

def display_status(connected):
    if connected:
        print(Fore.GREEN + "Status: Connected")
    else:
        print(Fore.RED + "Status: Disconnected")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

# Exemplo de comando seguro
@bot.tree.command(name="spamraid", description="Send a message and generate a button to spam")
@app_commands.describe(message="The message you want to spam")
async def spamraid(interaction: discord.Interaction, message: str):
    view = SpamButton(message)
    await interaction.response.send_message(f"💥SPAM TEXT💥 : {message}", view=view, ephemeral=True)  

@bot.event
async def on_ready():
    display_logo()
    display_status(True)
    print("Connected as " + Fore.YELLOW + f"{bot.user}")
    try:
        await bot.tree.sync()
        print(Fore.GREEN + "Commands successfully synchronized.")
    except Exception as e:
        display_status(False)
        print(Fore.RED + f"Error during synchronization: {e}")

if __name__ == "__main__":
    TOKEN = load_token()
    if TOKEN:
        try:
            bot.run(TOKEN)
        except discord.errors.LoginFailure:
            print(Fore.RED + "Can't connect to token. Please check your token.")
        except Exception as e:
            print(Fore.RED + f"An unexpected error occurred: {e}")
    else:
        print(Fore.RED + "❌ Error: Unable to load Discord token.")
