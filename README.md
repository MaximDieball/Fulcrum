# Fulcrum
**THIS CODE IS FOR LEARNING PURPOSES ONLY. THIS CODE IS NOT FOR USE WITHOUT PERMISSION. THE CURRENT VERSION IS NOT ANONYMIZED AND CAN BE TRACED BACK TO YOU. DO NOT MISUSE THIS!**

Fulcrum is a remote monitoring and access software with a Fulcrum beacon running on an infected computer that is accessible via a dedicated Discord server. The Discord server acts as a command and control server for an unlimited number of beacons. Each beacon creates its own text channel with the PC's name and a hardware ID as the channel's name.

Current Commands:
- **-TP [x]**: Takes a picture via a connected device. You can pass the identifier number to the command. If not, it will use 0.
- **-SG [x]**: Takes a screen grab. You can pass a number for a specific screen. If not, it will take one picture of all screens.
- **-SHELL**: Starts a remote shell controlled by the text channel. Any message that is typed will be sent as a command to the CMD, and the beacon will respond with the CMD prompt's response.
  - **quit**: Ends and terminates the shell.
- **-RC [command]** Run a singular cmd command.
- **-KL**: Starts a key logger, logging every key pressed.
  - **-UHK**: Stops and unhooks the keylogger.
  - **-GLK**: Gets logged keys and sends them into the channel.
- **-UF** {message_attachment: file}** Uploads a file on the infected computer.

Soon:
- **Triggers** that will activate the keylogger when certain events happen on the computer.
- **Installer** that installs the Fulcrum beacon.
- **Obfuscation and encryption of the discord token.**
- **File Downloader** A download command that sends a file from the system into the discord channel -GF [path]
- **Internet History Log**
- **Clipboard monitoring**

**WORK IN PROGRESS / MORE TO COME**
