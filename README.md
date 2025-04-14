## Termilox - Terminal Security Lock
Termilox is a Python-based terminal lock script designed to enhance security by requiring a password to unlock the terminal. It offers a range of customizable features, including terminal color selection, secure password management, and seamless integration into your shell startup file. Perfect for Linux users looking to add an extra layer of protection to their terminal sessions with improved security through password hashing.

## Features

### Password-Protected Terminal Lock:
Locks the terminal and requires a password to unlock, preventing unauthorized access.

### Hashed Password Storage:
Passwords are securely hashed using SHA-256 (via Python's hashlib) before storage, ensuring they are never saved in plaintext for enhanced security.

### Customizable Terminal Colors:
Choose from 13 color options (e.g., red, light green, neon green, pink) to personalize the terminal display.

### Persistent Configuration:
Saves hashed passwords and color preferences in user-specific files (~/.terminal_password and ~/.terminal_color).

### Autostart Integration:
Automatically adds itself to the user's .bashrc file to run when the terminal launches.

### Password Management:
Set a new password on first run and change it later using a command-line option, with all passwords securely hashed.

### Increased Security:
Blocks Ctrl+C (SIGINT) and Ctrl+Z (SIGTSTP) during password entry to prevent interruptions.
Implements a lockout mechanism after 3 incorrect attempts, with escalating delay times (5s, 10s, 15s, etc.).
Stores passwords as SHA-256 hashes, making them unreadable even if the configuration file is accessed.
### Permission Management:
Ensures correct ownership and permissions for configuration files, even when run with sudo.

### Show ASCII Art:
Displays a colorful ASCII art banner when the terminal is locked.

### Global Access:
Installs itself in /usr/local/bin/termilox for system-wide availability.

### Settings Removal:
Offers an option to remove all settings while keeping the script intact.

### Error Handling:
Includes comprehensive error checking for file operations, permissions, and subprocess calls.

## Requirements
Operating System: Linux distribution

Python: Python 3.x

Permissions: Requires sudo privileges for initial setup (moving script to /usr/local/bin and setting permissions).

Dependencies: No external Python libraries required. Uses only standard library modules (os, getpass, subprocess, sys, signal, time, hashlib).

## Installation

Download the Script:
Save termilox.py to any directory on your system (e.g., ~/Downloads).
Run the Script:

```bash
sudo python3 termilox.py
```
After running the program, it will ask you to set your password, and after setting the password, the security layer will be activated.

## Usage
Default Behavior
When you open a terminal, termilox locks it and displays an ASCII art banner. Enter the correct password to unlock it.

## Command-Line Options
Run the script with the following arguments for additional functionality:

### Change lock color:
```bash
termilox -c
```
Displays a menu to select from 13 color options.
Saves the choice to ~/.terminal_color.

### Change Password:
```bash
termilox -p
```
Prompts for the current password, then allows setting a new one.

### Remove Settings:
```bash
termilox -r
```
Removes the script from ~/.bashrc and deletes configuration files (~/.terminal_password, ~/.terminal_color).

The script itself remains in /usr/local/bin/termilox.
After uninstalling the program, simply run it and reconfigure it by typing termilox in the terminal.

## Example Workflow

### Lock the terminal:
```bash
termilox
```

## Acknowledgements
Built with Python 3 and standard library tools.
Inspired by the need for simple and customizable terminal security.

## Contribute
You can easily fork this repository, file issues, or create pull requests to improve Termilox. Suggestions for new features are welcome!

## License
This project is licensed under the MIT License. See the file for details.
