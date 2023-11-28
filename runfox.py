#!/usr/bin/python3

import os
import subprocess
import argparse

class PROFILE:
    def __init__(self, path, profile):
        self.path = path
        self.profile = profile

def read_profiles(path):
    profile_list = []
    for entry in os.listdir(path):
        if os.path.isdir(os.path.join(path, entry)):
            parts = entry.split('.')
            if len(parts) == 2 and parts[1].isalpha():
                print (f"found profile {parts[1]}")
                profile_list.append(PROFILE(path, parts[1]))
    return profile_list


def run_profile(plist, profile, arg_profile):
    result = 0

    for p in plist:
        if p.profile == profile:
            # Use Zenity to display a confirmation dialog
            if arg_profile:
                zenity_command = f'zenity --question --text="Do you want to start Firefox with profile {p.profile}?"'
                result = subprocess.call(zenity_command, shell=True)


            if result == 0:  # User clicked "OK"
                # Launch Firefox
                command = f"firefox -P {p.profile} &"
                subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return True
            else:
                return False
    return False


def show_profile_list(args,profiles):
    sorted_profiles = sorted(profiles, key=lambda p: p.profile)
    profile_names = [p.profile for p in sorted_profiles]
    geo=""
    user = os.getenv('LOGNAME')

    if args.xwidth:
        geo=f'--width={args.xwidth}'
    if args.yheight:
        geo=f'{geo} --height={args.yheight}'

    zenity_command = f'zenity --list {geo} --title="Firefox Profiles for {user}" --column="Profile Name" {" ".join(profile_names)}'
    result = subprocess.check_output(zenity_command, shell=True, text=True)
    return result.strip() if result else None


def main():
    parser = argparse.ArgumentParser(description='Launch Firefox with a specific profile.')
    parser.add_argument('-d', '--directory', help='Path to the Firefox directory')
    parser.add_argument('-p', '--profile', help='Profile to launch')
    parser.add_argument('-y', '--yheight', help='height of window')
    parser.add_argument('-x', '--xwidth', help='width of window')
    args = parser.parse_args()

    firefox_directory = args.directory
    profile_name = args.profile

    # use default $HOME/.mozilla/firefox if -d is empty
    if not firefox_directory:
        firefox_directory = os.path.join(os.path.expanduser("~"), ".mozilla", "firefox")

    if not os.path.isdir(firefox_directory):
        print(f"Error: Directory '{firefox_directory}' does not exist.")
        return

    profiles = read_profiles(firefox_directory)

    if not profile_name:
        # If no profile is specified, show a list of profiles using Zenity
        selected_profile = show_profile_list(args,profiles)

        if not selected_profile:
            print("User canceled.")
            return

        profile_name = selected_profile

    result = run_profile(profiles, profile_name, args.profile)

    if not result:
        print(f"Profile '{profile_name}' not found or user canceled.")

if __name__ == "__main__":
    main()

