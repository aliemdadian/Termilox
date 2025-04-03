#!/usr/bin/env python3
import os
import getpass
import subprocess
import sys
import signal
import time
import hashlib  # Added for password hashing

# Ensure script runs for the correct user, not root
real_home = os.path.expanduser("~" if os.geteuid() != 0 else os.path.expanduser(f"~{os.getenv('SUDO_USER')}"))
password_file = os.path.join(real_home, ".terminal_password")
startup_file = os.path.join(real_home, ".bashrc")
script_path = os.path.abspath(__file__)
color_file = os.path.join(real_home, ".terminal_color")  # File to store selected color

# Get the real user (not root)
user = os.getenv('SUDO_USER') or os.getlogin()
group = subprocess.run(["id", "-gn", user], capture_output=True, text=True).stdout.strip()

# Fix ownership and permissions
try:
    subprocess.run(["chown", f"{user}:{group}", startup_file], check=True)
    subprocess.run(["chmod", "644", startup_file], check=True)
    if os.path.exists(password_file):
        subprocess.run(["chown", f"{user}:{group}", password_file], check=True)
        subprocess.run(["chmod", "600", password_file], check=True)
    if os.path.exists(color_file):
        subprocess.run(["chown", f"{user}:{group}", color_file], check=True)
        subprocess.run(["chmod", "600", color_file], check=True)
except subprocess.CalledProcessError as e:
    print(f"Warning: Could not modify permissions due to subprocess error: {e}")
except Exception as e:
    print(f"Warning: Unexpected error while modifying permissions: {e}")

# Move script to /usr/local/bin if not already there
if not os.path.exists("/usr/local/bin/termilox"):
    print("Moving the script to /usr/local/bin for global access...")
    try:
        subprocess.run(["sudo", "mv", script_path, "/usr/local/bin/termilox"], check=True)
        subprocess.run(["sudo", "chmod", "+x", "/usr/local/bin/termilox"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to move or set permissions for script: {e}")
        sys.exit(1)

# Function to hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Set initial password if not exists
if not os.path.exists(password_file):
    print("Setting up a new password for the first time")
    while True:
        try:
            new_password = getpass.getpass("Enter new password: ")
            confirm_password = getpass.getpass("Confirm new password: ")
            if new_password == confirm_password:
                try:
                    with open(password_file, "w") as f:
                        f.write(hash_password(new_password))  # Store hashed password
                    os.chmod(password_file, 0o600)
                    subprocess.run(["chown", f"{user}:{group}", password_file], check=True)
                    print("Password set successfully!")
                    break
                except IOError as e:
                    print(f"Error: Could not write to password file: {e}")
                    sys.exit(1)
            else:
                print("Passwords do not match. Try again.")
        except KeyboardInterrupt:
            print("\nPassword setup cannot be interrupted. Please enter a password.")
            continue

# Add script to .bashrc if not already added
if os.path.exists(startup_file):
    with open(startup_file, "r") as f:
        lines = f.readlines()
    command = f"python3 /usr/local/bin/termilox\n"
    if command not in lines:
        try:
            with open(startup_file, "a") as f:
                f.write(f"\n# Run security script for terminal\n{command}")
        except IOError as e:
            print(f"Warning: Could not append to .bashrc: {e}")

# Color options
COLORS = {
    '1': '\033[0;31m',  # Red
    '2': '\033[1;32m',  # Light Green
    '3': '\033[1;34m',  # Light Blue
    '4': '\033[0;93m',  # Yellow
    '5': '\033[0;35m',  # Purple
    '6': '\033[38;5;214m',  # Orange
    '7': '\033[0;37m',  # White
    '8': '\033[0;30m',  # Black
    '9': '\033[0;90m',  # Dark Gray
    '10': '\033[38;5;46m',  # Neon Green
    '11': '\033[38;5;94m',  # Brown
    '12': '\033[38;5;27m',  # Dark Blue
    '13': '\033[38;5;206m',  # Pink
}
RESET = '\033[0m'

# Function to change color
def change_color():
    print("Select a color for the terminal display:")
    print("1. Red")
    print("2. Light Green")
    print("3. Light Blue")
    print("4. Yellow")
    print("5. Purple")
    print("6. Orange")
    print("7. White")
    print("8. Black")
    print("9. Dark Gray")
    print("10. Neon Green")
    print("11. Brown")
    print("12. Dark Blue")
    print("13. Pink")

    while True:
        try:
            choice = input("Enter your choice (1-13): ").strip()
            if choice in COLORS:
                try:
                    with open(color_file, "w") as f:
                        f.write(choice)
                    print("Color set to option", choice)
                    break
                except IOError as e:
                    print(f"Error: Could not write to color file: {e}")
                    break
            else:
                print("Invalid choice. Please select a number between 1 and 13.")
        except KeyboardInterrupt:
            print("\nColor selection cannot be interrupted. Please choose a color.")
            continue

# Function to get current color
def get_color():
    if os.path.exists(color_file):
        try:
            with open(color_file, "r") as f:
                color_choice = f.read().strip()
                return COLORS.get(color_choice, '\033[91m')  # Default to red if invalid
        except IOError as e:
            print(f"Warning: Could not read color file: {e}")
            return '\033[91m'
    return '\033[91m'  # Default color

# Function to remove settings
def remove_settings():
    if os.path.exists(startup_file):
        try:
            with open(startup_file, "r") as f:
                lines = f.readlines()
            with open(startup_file, "w") as f:
                skip_next = False
                for line in lines:
                    if line.strip() == "# Run security script for terminal" or "/usr/local/bin/termilox" in line:
                        skip_next = True
                    elif skip_next and "/usr/local/bin/termilox" not in line:
                        skip_next = False
                    else:
                        f.write(line)
        except IOError as e:
            print(f"Error: Could not modify .bashrc: {e}")
    for file in [password_file, color_file]:
        if os.path.exists(file):
            try:
                os.remove(file)
            except OSError as e:
                print(f"Warning: Could not remove {file}: {e}")
    print("Settings removed successfully, but the script is still present.")
    sys.exit(0)

# Function to change password
def change_password():
    try:
        with open(password_file, "r") as f:
            saved_password_hash = f.read().strip()
    except IOError as e:
        print(f"Error: Could not read password file: {e}")
        return
    current_color = get_color()
    while True:
        try:
            old_password = getpass.getpass(f"{current_color}Enter current password: {RESET}")
            if hash_password(old_password) != saved_password_hash:
                print(f"{current_color}Incorrect current password.{RESET}")
                return
            break
        except KeyboardInterrupt:
            print(f"\n{current_color}Password change cannot be interrupted. Please enter the current password.{RESET}")
            continue
    while True:
        try:
            new_password = getpass.getpass(f"{current_color}Enter new password: {RESET}")
            confirm_password = getpass.getpass(f"{current_color}Confirm new password: {RESET}")
            if new_password == confirm_password:
                try:
                    with open(password_file, "w") as f:
                        f.write(hash_password(new_password))  # Store hashed password
                    print(f"{current_color}Password changed successfully!{RESET}")
                    break
                except IOError as e:
                    print(f"Error: Could not write to password file: {e}")
                    break
            else:
                print(f"{current_color}Passwords do not match. Try again.{RESET}")
        except KeyboardInterrupt:
            print(f"\n{current_color}Password change cannot be interrupted. Please enter a new password.{RESET}")
            continue

# Handle command-line arguments
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-r":
            remove_settings()
        elif sys.argv[1] == "-c":
            change_color()
            sys.exit(0)
        elif sys.argv[1] == "-p":
            change_password()
            sys.exit(0)

    # Block Ctrl+C (SIGINT) and Ctrl+Z (SIGTSTP) while password is being entered
    def block_ctrl_c(signal, frame):
        print(f"\n{current_color}You cannot exit the program until the correct password is entered! (Press Enter to continue){RESET}")

    def block_ctrl_z(signal, frame):
        print(f"\n{current_color}You cannot suspend the program until the correct password is entered! (Press Enter to continue){RESET}")

    # Register the SIGINT and SIGTSTP handlers
    signal.signal(signal.SIGINT, block_ctrl_c)  # Ctrl+C
    signal.signal(signal.SIGTSTP, block_ctrl_z)  # Ctrl+Z

    # Read the stored password hash
    try:
        with open(password_file, "r") as f:
            saved_password_hash = f.read().strip()
    except IOError as e:
        print(f"Error: Could not read password file: {e}")
        sys.exit(1)

    # Get current color
    current_color = get_color()

    # ASCII Art with dynamic color
    ascii_art = f"""
{current_color}▄▄▄█████▓▓█████  ██▀███   ███▄ ▄███▓ ██▓ ██▓     ▒█████  ▒██   ██▒
▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒▓██▒▀█▀ ██▒▓██▒▓██▒    ▒██▒  ██▒▒▒ █ █ ▒░
▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒▓██    ▓██░▒██▒▒██░    ▒██░  ██▒░░  █   ░
░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  ▒██    ▒██ ░██░▒██░    ▒██   ██░ ░ █ █ ▒
  ▒██▒ ░ ░▒████▒░██▓ ▒██▒▒██▒   ░██▒░██░░██████▒░ ████▓▒░▒██▒ ▒██▒
  ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░   ░  ░░▓  ░ ▒░▓  ░░ ▒░▒░▒░ ▒▒ ░ ░▓ ░
    ░     ░ ░  ░  ░▒ ░ ▒░░  ░      ░ ▒ ░░ ░ ▒  ░  ░ ▒ ▒░ ░░   ░▒ ░
  ░         ░     ░░   ░ ░      ░    ▒ ░  ░ ░   ░ ░ ░ ▒   ░    ░
            ░  ░   ░            ░    ░      ░  ░    ░ ░   ░    ░
{RESET}"""

    print(ascii_art)

    # Lock terminal when 'termilox' is run without arguments
    wrong_attempts = 0
    lockout_count = 0
    print(f"{current_color}Terminal locked. Enter password to unlock.{RESET}")
    while True:
        try:
            entered_password = getpass.getpass(f"{current_color}Enter terminal password: {RESET}")
            if entered_password == "":  # Ignore empty input after Ctrl+C or Ctrl+Z
                continue
            if hash_password(entered_password) == saved_password_hash:
                print(f"{current_color}Access granted! Terminal unlocked.{RESET}")
                break
            else:
                wrong_attempts += 1
                remaining_attempts = 3 - (wrong_attempts % 3 if wrong_attempts % 3 != 0 else 3)
                print(f"{current_color}Incorrect password. Attempt {wrong_attempts % 3 if wrong_attempts % 3 != 0 else 3} of 3.{RESET}")
                if wrong_attempts % 3 == 0:  # Every 3 wrong attempts
                    lockout_count += 1
                    lockout_time = 5 * lockout_count  # 5 seconds for first lockout, 10 for second, etc.
                    print(f"{current_color}Too many incorrect attempts. Terminal locked for {lockout_time} seconds.{RESET}")
                    time.sleep(lockout_time)
        except KeyboardInterrupt:
            print(f"\n{current_color}You cannot exit the program until the correct password is entered! (Press Enter to continue){RESET}")
            continue
        except Exception as e:
            print(f"\n{current_color}An unexpected error occurred: {e}. Please try again.{RESET}")
            continue
