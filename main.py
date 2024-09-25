import asyncio
import aiohttp
import random
import shutil
import time
from colorama import init, Fore, Style
from datetime import datetime
from pathlib import Path
from pyfiglet import Figlet

init(autoreset=True)

def staticArt():
    figText = Figlet(font='slant')
    banner = figText.renderText('Hyper Sync')
    terminalWidth, _ = shutil.get_terminal_size()
    xType = ""
    for line in banner.split("\n"):
        cType = line.center(terminalWidth)
        xType += f"{Fore.CYAN}{Style.BRIGHT}{cType}\n"
    print(xType)
    print(f"{Fore.CYAN}{Style.BRIGHT}Hyper Sync : Token Updater - Customize Your Presence\n".center(terminalWidth))
    
async def checkToken(session, token):
    headers = {
        'Authorization': token
    }
    async with session.get('https://discordapp.com/api/v9/users/@me', headers=headers) as response:
        return response.status == 200

async def updateToken(session, token, status_text, presence):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    data = {
        'custom_status': {'text': status_text},
        'status': presence
    }
    async with session.patch('https://discordapp.com/api/v9/users/@me/settings', headers=headers, json=data) as response:
        return response.status in [200, 201, 204]

def logUpdate(token, status_text, presence):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.WHITE}{Style.DIM}{timestamp} - ", end="")
    print(f"{Fore.GREEN}{Style.BRIGHT}INFO ", end="")
    print(f"{Fore.WHITE}- Updated settings for token ", end="")
    print(f"{Fore.CYAN}{token[:10]}...: ", end="")
    print(f"{Fore.WHITE}{{'custom_status': {{'text': '", end="")
    print(f"{Fore.MAGENTA}{status_text}", end="")
    print(f"{Fore.WHITE}'}}, 'status': '", end="")
    print(f"{getPresenceColor(presence)}{presence}", end="")
    print(f"{Fore.WHITE}'}}")

def logInvalidToken(token):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.WHITE}{Style.DIM}{timestamp} - ", end="")
    print(f"{Fore.RED}{Style.BRIGHT}ERROR ", end="")
    print(f"{Fore.WHITE}- Invalid token: ", end="")
    print(f"{Fore.CYAN}{token[:10]}...")

def getPresenceColor(presence):
    if presence == 'online':
        return Fore.GREEN
    elif presence == 'idle':
        return Fore.YELLOW
    elif presence == 'dnd':
        return Fore.RED
    else:
        return Fore.WHITE

async def updateTokens(session, tokens, statusTexts):
    validTokens = []
    for token in tokens:
        if await checkToken(session, token):
            validTokens.append(token)
            status = random.choice(statusTexts)
            presence = random.choice(['online', 'idle', 'dnd'])
            success = await updateToken(session, token, status, presence)
            if success:
                logUpdate(token, status, presence)
        else:
            logInvalidToken(token)
    return validTokens

def readFile(file_path):
    path = Path(file_path)
    if path.exists():
        with path.open() as f:
            return [line.strip() for line in f if line.strip()]
    else:
        print(f"{Fore.RED}Error: {file_path} not found.")
        return []

async def main():
    staticArt()
    tokens = readFile('config/tokens.txt')
    statusTexts = readFile('config/status.txt')
    if not tokens or not statusTexts:
        return
    async with aiohttp.ClientSession() as session:
        while True:
            validTokens = await updateTokens(session, tokens, statusTexts)
            if not validTokens:
                print(f"\n{Fore.RED}{Style.BRIGHT}All tokens are invalid. Closing the program.")
                return
            tokens = validTokens
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}Waiting for 5 minutes before next update...")
            await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
