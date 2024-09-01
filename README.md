# Fulcrum
**THIS CODE IS FOR LEARNING PURPOSES ONLY. THIS CODE IS NOT FOR USE WITHOUT PERMISSION. DO NOT MISUSE THIS!**

Fulcrum is a remote monitoring and access software with a Fulcrum beacon running on an infected computer that is accessible via a dedicated Discord server. The Discord server acts as a command and control server for an unlimited number of beacons. Each beacon creates its own text channel with the PC's name and a hardware ID as the channel's name. **Check out the supported commands below ↓**


### Setup
- Create your own Discord bot at [Discord Developer Portal](https://discord.com/developers/applications).
- Set up a Discord server with the following structure

![image](https://github.com/user-attachments/assets/9dc80efc-cb84-403f-ae3c-8e0e6bbd98d5)


- Invite your bot to the server.
- Run the ``token_and_key_gen.py`` and input your discord bot token.
    - There should be two new files in the directory called ``.env`` and ``key.key``.
    - Upload both files to the ``your-files`` channel.
- Copy the download link of the ``key.key`` file and add it to the code of the ``fulcrum_beacon.pyw`` file at `DECRYPTION_KEY_URL = "YOUR URL"`
- Upload the ``fulcrum_beacon.pyw`` file to the ``your-files`` channel.
  - You can rename ``fulcrum_beacon.pyw`` if you want to.
  - If you want to use a compiled version of ``fulcrum_beacon.pyw`` you will need Discord nitro to upload the file due to its size.
- Copy the download link of the ``.env`` file and add it to the code of the ``installer.py`` file at ``DOT_ENV_FILE_URL = "YOUR URL"``
- Copy the download link of the ``fulcrum_beacon.pyw``(or your renamed file) file and add it to the code of the ``installer.py`` file at ``BEACON_URL = "YOUR URL"`` 
image here    

  
### Infecting a System
- Execute the ``installer.py`` file on the victim's computer.
  - remember to add your Url to ``installer.py`` before.
- The Fulcrum beacon will be downloaded and execute.
- A new discord channel will appear on your discord server.
  - ``[pc name]-[hardware id]``
- The beacon adds a .lnk file to the Startup folder and will reconnect after the system is turn off and on again.

![image](https://github.com/user-attachments/assets/66c21fb5-249d-4891-8a31-cda244e2bf80)
![image](https://github.com/user-attachments/assets/f5adfc95-d592-4368-8305-7a9a06009580)

- You can now use any command through the created channel or the `all-channel` channel.

### Current Commands
- ``-TP [x]``: Takes a picture via a connected device. You can pass the identifier number to the command. If not, it will use 0.
- ``-SG [x]``: Takes a screen grab. You can pass a number for a specific screen. If not, it will take one picture of all screens.
- ``-SHELL``: Starts a remote shell controlled by the text channel. Any message that is typed will be sent as a command to the CMD, and the beacon will respond with the CMD prompt's response.
  - ``quit``: Ends and terminates the shell.
- ``-RC [command]`` Run a singular cmd command.
- ``-KL``: Starts a key logger, logging every key pressed.
  - ``-UHK``: Stops and unhooks the keylogger.
  - ``-GLK``: Gets logged keys and sends them into the channel.
- ``-UF {message_attachment: file}``: Uploads a file on the infected computer.
- ``-MB {message}``: Create a message box that contains a custom message.

### Example
![image](https://github.com/user-attachments/assets/b16d0622-d443-426e-b908-e6943029c2d3)


### Soon
- **Triggers** that will activate the keylogger when certain events happen on the computer.
- **File Downloader** A download command that sends a file from the system into the discord channel -GF [path]
- **Internet History Log**
- **Clipboard monitoring**


### Known bugs
- Keylogger not stopping after -UHK command.
