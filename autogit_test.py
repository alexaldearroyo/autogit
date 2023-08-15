#!/usr/bin/env python3

import subprocess
import sys
import os

def execute_command(command, message=""):
    try:
        if message:
            subprocess.check_call(command.split() + [message])
        else:
            subprocess.check_call(command.split())
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        sys.exit(1)


def is_git_repository():
    try:
        subprocess.check_call(["git", "status"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    # Ensure we're operating in the calling directory
    os.chdir(os.getcwd())  # This is generally redundant but ensures you're in the calling directory

    if not is_git_repository():
        print("This directory is not a Git repository. Initializing...")
        execute_command("git init")
        print("Git repository created in the working directory")

    choice = input("Do you want to add all changes in the repository? (y/n): ").strip().lower()
    
    if choice in ['yes', 'y']:
        execute_command("git add .")
    elif choice in ['no', 'n']:
        filename = input("Enter the name of the file you want to add: ").strip()
        execute_command(f"git add {filename}")
    else:
        print("Invalid choice!")
        sys.exit(1)

    commit_message = input("Enter a descriptive commit message: ").strip()
    execute_command("git commit -m", commit_message)

    execute_command("git push -u origin main")

if __name__ == "__main__":
    main()
