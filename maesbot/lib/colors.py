"""
colors.py - ANSI color codes for terminal output

Usage:
    from colors import CYAN, GREEN, RED, NC
    print(f"{GREEN}Success!{NC}")
    print(f"{RED}Error!{NC}")
    print(f"{CYAN}Info: {BOLD}Important{NC}")
"""

# Basic colors
CYAN = "\033[0;36m"
BRIGHT_CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
BRIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
MAGENTA = "\033[0;35m"
DARK_GREY = "\033[0;90m"
GREY = "\033[0;37m"

# Text formatting
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
ITALIC = "\033[3m"

# Reset
NC = "\033[0m"  # No Color / Reset
