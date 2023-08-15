#!/usr/bin/env python3

import subprocess
import sys
import os

def is_git_repository():
    """Check if the current directory is a Git repository."""
    return os.path.isdir(".git")

def is_origin_github():
    """Check if the 'origin' remote of the Git repository points to GitHub."""
    try:
        # Get the details of the remote named 'origin'
        remote_details = subprocess.check_output(["git", "remote", "-v"], text=True)
        # Look for lines specifically related to 'origin' that also mention 'github.com'
        github_related_lines = [line for line in remote_details if 'origin' in line and 'github.com' in line]
        return bool(github_related_lines)
    except subprocess.CalledProcessError:
        return False

def execute_command(command, message=""):
    try:
        if message:
            subprocess.check_call(command.split() + [message])
        else:
            subprocess.check_call(command.split())
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        sys.exit(1)

def initialize_git_repo():
    """Initialize a new Git repository in the current directory."""
    execute_command("git init")

def main():
    print("\nThis is the test version of autogit\n")

    # Ensure we're operating in the calling directory
    os.chdir(os.getcwd())  # This is generally redundant but ensures you're in the calling directory

    # Inform the user that the program is checking for a Git repository
    print("Checking if the present working directory contains a Git repository...")

    # Check if the present directory is a Git repository
    if not is_git_repository():
        print("The present working directory is not a Git repository!\n")
        choice = input("Would you like to initialize a new Git repository here? (y/n): ").strip().lower()

        if choice in ['yes', 'y']:
            initialize_git_repo()
            print("\nGit repository initialized!\n")
        else:
            if not is_origin_github():
                print("Warning: The 'origin' remote of this repository does not seem to point to GitHub.")
            
            choice = input("Do you want to continue anyway? (y/n): ").strip().lower()

            if choice not in ['yes', 'y']:
                print("Exiting program...")
                sys.exit(0)

    else:
        print("Confirmed: This directory contains a Git repository.\n")
        print("\nThis is the test version of autogit\n")

    # Ensure we're operating in the calling directory
    os.chdir(os.getcwd())  # This is generally redundant but ensures you're in the calling directory

    # Inform the user that the program is checking for a Git repository
    print("Checking if the present working directory contains a Git repository...")

    if not is_git_repository():
        print("The present working directory is not a Git repository!\n")
        choice = input("Would you like to initialize a new Git repository here? (y/n): ").strip().lower()

        if choice in ['yes', 'y']:
            initialize_git_repo()
            print("\nGit repository initialized!\n")
        else:
            print("Exiting program...")
            sys.exit(0)
    else:
        print("Confirmed: This directory contains a Git repository.\n")
        if is_origin_github():
            print("Confirmed: This Git repository's 'origin' remote is linked to GitHub.\n")
        else:
            print("Warning: The 'origin' remote of this repository does not seem to point to GitHub.")
            print("For the program to function correctly, this Git repository should be linked to a GitHub repository.")
            print("\033[106m\033[97mCreate a repository on the GitHub website and connect it to the local repository using the command git remote add origin name_of_repository.git\033[0m\n")
            #choice = input("Do you want to continue anyway? (y/n): ").strip().lower()

            #if choice not in ['yes', 'y']:
            print("Exiting program...\n")
            sys.exit(0)

    #Asks user to commit to git
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
