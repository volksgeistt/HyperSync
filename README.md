# Hyper Sync: Discord Token Onliner
*Hyper Sync is a powerful and customizable Discord token updater that allows you to manage and update multiple Discord accounts simultaneously. It provides a seamless way to change custom status messages and online presence for multiple tokens automatically.*
### Features:
- **Multi-Token Support:** Update multiple Discord tokens concurrently.
- **Custom Status Rotation:** Randomly select and apply custom status messages from a predefined list.
- **Presence Cycling:** Automatically cycle through different online statuses (online, idle, do not disturb).
- **Asynchronous Operations:** Utilizes asyncio and aiohttp for efficient, non-blocking operations.
- **Token Validation:** Automatically checks and removes invalid tokens.
- **Colorful Console Output:** Uses colorama for visually appealing and informative console logs.
### Requirements:
`Python 3.7+ / aiohttp, colorama, pyfiglet`
### Configuration:
- Add your Discord tokens to config/tokens.txt, one token per line.
- Add your desired custom status messages to config/status.txt, one message per line.
### Usage:
Run the script using Python: `python main.py`
*The script will start updating the tokens' status and presence every 5 minutes. It will continue running until all tokens become invalid or the program is manually terminated.*
### How It Works:
1. The script reads Discord tokens and custom status messages from configuration files.
2. It creates an asynchronous session to manage HTTP requests.
3. For each token:
   - It validates the token by making an API call to Discord.
   - If valid, it randomly selects a custom status message and presence state.
   - It updates the token's settings using Discord's API.
   - It logs the update with a colorful, informative message.
4. The process repeats every 5 minutes, using only the tokens that were valid in the previous cycle.
### Customization:
- Modify the `updateTokens()` function to change the update behavior.
- Adjust the sleep time in the `main()` function to change the update frequency.
### Disclaimer:
**This tool is for educational purposes only. Use it responsibly and in accordance with Discord's Terms of Service. The authors are not responsible for any misuse or any violations of Discord's policies.**




