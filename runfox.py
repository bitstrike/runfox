#!/usr/bin/python3

import os
import subprocess
import argparse

# create a list of these when reading firefox directory
class PROFILE:
    def __init__(self, path, profile):
        self.path = path
        self.profile = profile


# read all firefox profiles from passed path (usually /$HOME/.mozilla/firefox) but could 
# be another user if this is launched with sudo -i -u USER /usr/local/bin/runfox.py -d /home/USER/.mozilla/firefox
def read_profiles(path):
    profile_list = []
    for entry in os.listdir(path):
        if os.path.isdir(os.path.join(path, entry)):
            parts = entry.split('.')
            if len(parts) == 2 and parts[1].isalpha():
                print (f"found profile {parts[1]}")
                profile_list.append(PROFILE(path, parts[1]))
    return profile_list


# fork a firefox using the given profile. prompt to start if not selected from the list
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


# present a list of profiles to select from using zenity - why is tkinter so bugly?
def show_profile_list(profiles):
    sorted_profiles = sorted(profiles, key=lambda p: p.profile)
    profile_names = [p.profile for p in sorted_profiles]

    zenity_command = f'zenity --list --title="Firefox Profiles" --column="Profile Name" {" ".join(profile_names)}'
    result = subprocess.check_output(zenity_command, shell=True, text=True)
    return result.strip() if result else None


# start here
def main():
    parser = argparse.ArgumentParser(description='Launch Firefox with a specific profile.')
    parser.add_argument('-d', '--directory', help='Path to the Firefox directory', required=True)
    parser.add_argument('-p', '--profile', help='Profile to launch')
    args = parser.parse_args()

    # get what was specified from cli
    firefox_directory = args.directory
    profile_name = args.profile

    # can't find the path specified
    if not os.path.isdir(firefox_directory):
        print(f"Error: Directory '{firefox_directory}' does not exist.")
        return

    # read profiles
    profiles = read_profiles(firefox_directory)

    # if no profile_name specified to run, give a list of them
    if not profile_name:
        # If no profile is specified, show a list of profiles using Zenity
        selected_profile = show_profile_list(profiles)

        if not selected_profile:
            print("User canceled.")
            return

        profile_name = selected_profile

    # run firefox with selected profile, or cli profile
    result = run_profile(profiles, profile_name, args.profile)

    if not result:
        print(f"Profile '{profile_name}' not found or user canceled.")

if __name__ == "__main__":
    main()

