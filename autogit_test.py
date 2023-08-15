#!/usr/bin/env python3

import subprocess
import sys
import os

def is_git_repository():
    """Check if the current directory is a Git repository."""
    return os.path.isdir(".git")

# REVISAR
#def is_origin_github():
#    """Check if the 'origin' remote of the Git repository points to GitHub."""
#    try:
#        # Get the details of the remote named 'origin'
#        remote_details = subprocess.check_output(["git", "remote", "-v"], text=True)
#        # Look for lines specifically related to 'origin' that also mention 'github.com'
#        github_related_lines = [line for line in remote_details if 'origin' in line and 'github.com' in line]
#        print(remote_details)
#        return bool(github_related_lines)
#    except subprocess.CalledProcessError:
#        return False

def execute_command(command, message="", capture_output=False):
    """Execute a shell command provided in the form of a string"""
    try:
        if message:
            completed_process = subprocess.run(command.split() + [message], capture_output=capture_output, text=True)
        else:
            completed_process = subprocess.run(command.split(), capture_output=capture_output, text=True)
        
        if completed_process.returncode != 0:
            print(f"Error executing command: {command}")
            sys.exit(1)
        
        if capture_output:
            return completed_process.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        sys.exit(1)

def has_linked_github_repo():
    """Check if the Git repository in the present working directory is linked to a GitHub repository."""
    remotes = execute_command("git remote -v", capture_output=True)
    return "github.com" in remotes

def initialize_git_repo():
    """Initialize a new Git repository in the current directory."""
    execute_command("git init")

def main():

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
            print("Exiting program...")
            sys.exit(0)
    else:
        print("Confirmed: This directory contains a Git repository.\n")
        # REVISAR
#        if is_origin_github():
#            print("Confirmed: This Git repository's 'origin' remote is linked to GitHub.\n")
#        else:
#            print("Warning: The 'origin' remote of this repository does not seem to point to GitHub.")
#            print("For the program to function correctly, this Git repository should be linked to a GitHub repository.")
#            print("\033[43mCreate a repository on the GitHub website and connect it to the local repository using the command git remote add origin name_of_repository.git\033[0m\n")
#            print("Exiting program...\n")
#            sys.exit(0)

    # Check if the present directory is linked to a GitHub repository
    if not has_linked_github_repo():
        print("Warning: The present working directory is not linked to a GitHub repository!\n")
        choice = input("Do you wish to continue without linking to GitHub? (y/n): ").strip().lower()
        if choice not in ['yes', 'y']:
            print("Exiting program...")
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