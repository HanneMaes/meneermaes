#!/usr/bin/env python3

import subprocess
import sys
import yaml
from pathlib import Path
from fuzzypicker import pick_yaml_file, pick_from_list

#############################################################################
# Colors for output

CYAN = "\033[0;36m"
BRIGHT_CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
BRIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
MAGENTA = "\033[0;35m"
NC = "\033[0m"  # No Color
BOLD = "\033[1m"

#############################################################################
# Helper functions


def load_settings(settinsPath):
    """Load settings from settings.yaml"""
    settings_file = Path(settinsPath)
    if not settings_file.exists():
        print(f"{RED}✗ Error: settings.yaml not found!{NC}")
        sys.exit(1)
    try:
        with open(settings_file, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"{RED}✗ Error loading settings.yaml: {e}{NC}\n")
        sys.exit(1)


#########################################


def load_private_settings():
    """Load private settings (student lists)"""
    private_file = Path("/data/private/private-settings.yaml")
    if not private_file.exists():
        print(f"{RED}✗ Error: private-settings.yaml not found!{NC}")
        sys.exit(1)
    try:
        with open(private_file, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"{RED}✗ Error loading private-settings.yaml: {e}{NC}\n")
        sys.exit(1)


#########################################


def select_input_yaml(settings):
    """Select an input YAML file from the configured data directory"""
    input_dir = settings.get("paths", {}).get("punten_input_dir_website")
    if not input_dir:
        print(
            f"{RED}✗ Error: 'paths.punten_input_dir_website' not found in settings.yaml{NC}\n"
        )
        return None

    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"{RED}✗ Error: Input directory does not exist: {input_dir}{NC}\n")
        return None

    selected = pick_yaml_file(
        start_path=str(input_path), message="Select input YAML file:"
    )
    return selected


#########################################


def select_students():
    """Select a class and return list of students"""
    private_settings = load_private_settings()
    klassen = private_settings.get("klassen", {})

    if not klassen:
        print(f"{RED}✗ Error: No classes found in private-settings.yaml{NC}\n")
        return []

    # Pick a class
    class_names = list(klassen.keys())
    selected_class = pick_from_list(
        class_names, "Select class:", message_color="#d787d7"
    )

    if not selected_class:
        print(f"{YELLOW}No class selected{NC}\n")
        return []

    # Parse students from string format: '"Name 1", "Name 2"'
    students_str = klassen[selected_class]
    students = [s.strip().strip('"') for s in students_str.strip('"').split('", "')]

    return students, selected_class


#########################################


def run_script(script_path: str, args: list = None) -> bool:
    """Run Python script with optional arguments"""
    script = Path(script_path)
    if not script.exists():
        print(f"{RED}✗ Error: Script not found: {script}{NC}")
        return False

    # Build command
    cmd = [sys.executable, str(script)]
    if args:
        cmd.extend(args)

    print(f"{YELLOW}$ {GREEN}{BOLD}{script.name}{NC}\n")

    try:
        result = subprocess.run(cmd, check=True, text=True)
        print(f"{BRIGHT_GREEN}✓ Script completed successfully{NC}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}✗ Script failed with exit code {e.returncode}{NC}\n")
        return False
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Script interrupted by user{NC}\n")
        return False
    except Exception as e:
        print(f"{RED}✗ Error running script: {e}{NC}\n")
        return False


#############################################################################
# Main

# ASCII art
roboColor = GREEN
print(f"{RED}       ●     ●")
print(f"{roboColor}       |     |")
print(f"{roboColor}      ╭───────╮")
print(f"{roboColor}      |       |")
print(f"{roboColor}  MAES| {RED}|   |{roboColor} |BOT")
print(f"{roboColor}      |  {BLUE}...{roboColor}  |")
print(f"{roboColor}      ╰───────╯")
print(f"{roboColor}         > <{NC}")
print()

# Load settings
settings = load_settings("settings.yaml")

# Show main menu
actions = ["Punten: Create Sheets", "Punten: Sheets to PDF"]
selected = pick_from_list(
    actions, "What can I do for my Master?", message_color="#bade87"
)

if selected:
    # ##################### #
    # Punten: Create Sheets #
    # ##################### #
    if selected == "Punten: Create Sheets":
        # Select input YAML file
        input_file = select_input_yaml(settings)
        if not input_file:
            print(f"{RED}✗ No input file selected{NC}\n")
            sys.exit(1)

        # Select students
        students, className = select_students()
        if not students:
            print(f"{RED}✗ No students selected{NC}\n")
            sys.exit(1)
        students = " ".join(f'"{s}"' for s in students)  # Object to string

        # Get output directory
        output_dir = settings.get("paths", {}).get("punten_output_dir")
        output_dir = str(output_dir) + str(className)
        if not output_dir:
            print(
                f"{RED}✗ Error: 'paths.punten_output_dir' not found in settings.yaml{NC}\n"
            )
            sys.exit(1)

        # Run script
        run_script(
            "Punten/create-sheets.py",
            ["--input", input_file, "--output", output_dir, "--students", students],
        )

    # ###################### #
    # Punten: Sheets to PDF  #
    # ###################### #
    elif selected == "Punten: Sheets to PDF":
        run_script("Punten/sheets-to-pdf.py")
else:
    print(f"\n{YELLOW}⚠️  No action selected{NC}\n")
