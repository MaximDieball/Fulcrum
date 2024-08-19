# Fulcrum
**THIS CODE IS FOR LEARNING PURPOSES ONLY. THIS CODE IS NOT FOR USE WITHOUT PERMISSION. THE CURRENT VERSION IS NOT ANONYMIZED AND CAN BE TRACED BACK TO YOU. DO NOT MISUSE THIS!**

Fulcrum is a remote monitoring and access software with a Fulcrum beacon running on an infected computer that is accessible via a dedicated Discord server. The Discord server acts as a command and control server for an unlimited number of beacons. Each beacon creates its own text channel with the PC's name and a hardware ID as the channel's name. **Check out the supported commands below ↓**


### Setup
- If you want the installer to work without a `.env` file, you will need to modify the code and add the token directly. Add the token at the start of both the `fulcrum_beacon.pyw` file and the `installer.py` file.
- Create your own Discord bot at [Discord Developer Portal](https://discord.com/developers/applications).
- Set up a Discord server with the following structure

![image](https://github.com/user-attachments/assets/c5ecaac9-9e8d-4ba2-b3e6-b98066d3c38b)

- invite your bot to the server
- send your `fulcrum_beacon.pyw` file (can be renamed) into the `fulcrum-beacon` channel
    - if you want to use a compiled version of `fulcrum_beacon.pyw` you will need discord nitro to upload the file due to its size.

  
### Infecting a System
- Execute the `installer.py` file on the victim's computer.
  - If you did not modify the code, you will need a `.env` file with your bot token:
      - `TOKEN = 'YOUR TOKEN'`
- When the victim's computer is rebooted, the Fulcrum beacon will execute, and the victim will appear on Discord.

![image](https://github.com/user-attachments/assets/00af552b-57f7-4d3a-b14a-4fe0e6783ba9)  
![image](https://github.com/user-attachments/assets/f5adfc95-d592-4368-8305-7a9a06009580)

- You can now use any command through the created channel or the `all-channel` channel. 


### Current Commands
- **-TP [x]**: Takes a picture via a connected device. You can pass the identifier number to the command. If not, it will use 0.
- **-SG [x]**: Takes a screen grab. You can pass a number for a specific screen. If not, it will take one picture of all screens.
- **-SHELL**: Starts a remote shell controlled by the text channel. Any message that is typed will be sent as a command to the CMD, and the beacon will respond with the CMD prompt's response.
  - **quit**: Ends and terminates the shell.
- **-RC [command]** Run a singular cmd command.
- **-KL**: Starts a key logger, logging every key pressed.
  - **-UHK**: Stops and unhooks the keylogger.
  - **-GLK**: Gets logged keys and sends them into the channel.
- **-UF {message_attachment: file}** Uploads a file on the infected computer.

### Example
![image](https://github.com/user-attachments/assets/b16d0622-d443-426e-b908-e6943029c2d3)


### Soon
- **Triggers** that will activate the keylogger when certain events happen on the computer.
- **Obfuscation and encryption of the discord token.**
- **File Downloader** A download command that sends a file from the system into the discord channel -GF [path]
- **Internet History Log**
- **Clipboard monitoring**

