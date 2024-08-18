# Fulcrum
**THIS CODE IS FOR LEARNING PURPOSES ONLY. THIS CODE IS NOT FOR USE WITHOUT PERMISSION. THE CURRENT VERSION IS NOT ANONYMIZED AND CAN BE TRACED BACK TO YOU. DO NOT MISUSE THIS!**

Fulcrum is a remote monitoring and access software with a Fulcrum beacon running on an infected computer that is accessible via a dedicated Discord server. The Discord server acts as a command and control server for an unlimited number of beacons. Each beacon creates its own text channel with the PC's name and a hardware ID as the channel's name.

## setup
- if you want the installer to work without a .env file you will need to modify the code and add the token directly. add the token at the start of the fulcrum_beacon.py file and the installer.py file.
- create your own discord bot https://discord.com/developers/applications
- setup a discord server with the following structure and invite the bot
![image](https://github.com/user-attachments/assets/c5ecaac9-9e8d-4ba2-b3e6-b98066d3c38b)

## Infecting a system
- Execute the Installer.py file on the victims computer
  - if you did not modify the code you will need a .env file with your bot token
      - TOKEN = 'YOUR TOKEN'
- when the victems computer is rebooted the fulcrum beacon will execute and the victim will appear on the discord
![image](https://github.com/user-attachments/assets/f5adfc95-d592-4368-8305-7a9a06009580)
![image](https://github.com/user-attachments/assets/00af552b-57f7-4d3a-b14a-4fe0e6783ba9)
- now you can use any command through the created channel or the all-channel channel

##Current Commands:
- **-TP [x]**: Takes a picture via a connected device. You can pass the identifier number to the command. If not, it will use 0.
- **-SG [x]**: Takes a screen grab. You can pass a number for a specific screen. If not, it will take one picture of all screens.
- **-SHELL**: Starts a remote shell controlled by the text channel. Any message that is typed will be sent as a command to the CMD, and the beacon will respond with the CMD prompt's response.
  - **quit**: Ends and terminates the shell.
- **-RC [command]** Run a singular cmd command.
- **-KL**: Starts a key logger, logging every key pressed.
  - **-UHK**: Stops and unhooks the keylogger.
  - **-GLK**: Gets logged keys and sends them into the channel.
- **-UF {message_attachment: file}** Uploads a file on the infected computer.

## Example
![image](https://github.com/user-attachments/assets/b16d0622-d443-426e-b908-e6943029c2d3)


##Soon:
- **Triggers** that will activate the keylogger when certain events happen on the computer.
- **Installer** that installs the Fulcrum beacon.
- **Obfuscation and encryption of the discord token.**
- **File Downloader** A download command that sends a file from the system into the discord channel -GF [path]
- **Internet History Log**
- **Clipboard monitoring**

