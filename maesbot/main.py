#!/usr/bin/env python3

import subprocess
import sys
import yaml
from pathlib import Path
from fuzzypicker import pick_yaml_file, pick_from_list

#############################################################################@
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

#############################################################################@
# Helper functions


# Load settings from settings.yaml
def load_settings():
    settings_file = Path("settings.yaml")

    if not settings_file.exists():
        print(f"{RED}✗ Error: settings.yaml not found!{NC}")
        sys.exit(1)

    try:
        with open(settings_file, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"{RED}✗ Error loading settings.yaml: {e}{NC}\n")
        sys.exit(1)


###############################################################


def select_input_yaml(settings):
    """
    Select an input YAML file from the configured data directory.

    Returns:
        Full path to selected YAML file or None
    """
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

    print(f"{CYAN}📁 Selecting from: {BOLD}{input_dir}{NC}\n")

    # Use fuzzy picker to select YAML file
    selected = pick_yaml_file(
        start_path=str(input_path), message="Select input YAML file:"
    )

    return selected


###############################################################


# Run Python scripts
def run_script(script_path: str) -> bool:
    script = Path(script_path)

    if not script.exists():
        print(f"{RED}✗ Error: Script not found: {script}{NC}")
        return False

    print(f"{CYAN}  → Running: {BOLD}{script}{NC}\n")
    print(f"{CYAN}{'─' * 60}{NC}")

    try:
        # Run the script and capture output in real-time
        result = subprocess.run([sys.executable, str(script)], check=True, text=True)

        print(f"{CYAN}{'─' * 60}{NC}")
        print(f"{BRIGHT_GREEN}✓ Script completed successfully{NC}\n")
        return True

    except subprocess.CalledProcessError as e:
        print(f"{CYAN}{'─' * 60}{NC}")
        print(f"{RED}✗ Script failed with exit code {e.returncode}{NC}\n")
        return False

    except KeyboardInterrupt:
        print(f"\n{YELLOW}⚠️  Script interrupted by user{NC}\n")
        return False

    except Exception as e:
        print(f"{RED}✗ Error running script: {e}{NC}\n")
        return False


#############################################################################@

# Load settings
settings = load_settings()

# Show main menu
actions = ["Punten: Create Sheets", "Punten: Sheets to PDF"]
selected = pick_from_list(actions, "What do you want to do?", message_color="#d787d7")

if selected:
    # ##################### #
    # Punten: Create Sheets #
    # ##################### #
    if selected == "Punten: Create Sheets":
        input_file = select_input_yaml(settings)  # select YAML file from website
        output_dir = settings.get("paths", {}).get(
            "output_data"
        )  # Get output directory from settings
        run_script("Punten/create-sheets.py")
        if not output_dir:
            print(f"{RED}✗ Error: 'paths.output_data' not found in settings.yaml{NC}\n")
            sys.exit(1)

    elif selected == "Punten: Sheets to PDF":
        run_script("Punten/sheets-to-pdf.py")

else:
    print(f"\n{YELLOW}⚠️  No action selected{NC}\n")
