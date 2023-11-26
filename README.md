# runfox.py

## Overview

`runfox.py` is a Python script designed to facilitate launching Mozilla Firefox with specific profiles from the command line. It provides a convenient way to interact with Firefox profiles stored in a designated directory.

## Features

- Launch Firefox with a specified profile directly from the command line.
- Display a list of available profiles using Zenity, allowing users to choose a profile interactively.

## Prerequisites

- Python 3
- Mozilla Firefox installed

## Usage

### Basic Usage

```bash
python runfox.py -d /path/to/firefox/profiles -p my_profile

    -d or --directory: Path to the directory containing Firefox profiles.
    -p or --profile: Name of the profile to launch.
```

## Interactive Mode

If the profile is not specified, the script will show an interactive list of available profiles:

```bash
python runfox.py -d /path/to/firefox/profiles
```
Users can select a profile from the list, and the script will launch Firefox with the chosen profile.

## Example
```bash
python runfox.py -d /home/user/.mozilla/firefox -p default
```
This example launches Firefox with the "default" profile from the specified directory.

## Notes
    Ensure that the provided directory path (-d option) is valid and contains Firefox profiles.

## License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute this script according to the terms of the license.
