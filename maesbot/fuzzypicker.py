#!/usr/bin/env python3
"""
FuzzyPicker - Simple wrapper around InquirerPy for common use cases

This library provides easy-to-use functions for:
- Picking from lists
- Picking files (with extension filtering)
- Picking from JSON/YAML files
- Picking and running associated functions

Requirements:
    pip install InquirerPy PyYAML
"""

from InquirerPy import inquirer
from InquirerPy.utils import get_style
from pathlib import Path
from typing import List, Optional, Tuple, Any, Callable
import json


def pick_from_list(
    items: List[str], message: str = "Select an item:", message_color: str = "#af87ff"
) -> Optional[str]:
    """
    Pick an item from a list of strings with fuzzy finding.

    Args:
        items: List of strings to choose from
        message: Question/title to display at the top
        message_color: Hex color for the message (default: purple #af87ff)

    Returns:
        Selected item or None if cancelled (Ctrl-C)

    Example:
        actions = ["Deploy", "Test", "Backup"]
        selected = pick_from_list(actions, "What do you want to do?", "#ff00ff")
        if selected:
            print(f"You chose: {selected}")
    """
    if not items:
        print("Error: No items provided")
        return None

    # Create custom style with colored message
    style = get_style({"question": message_color}, style_override=False)

    return inquirer.fuzzy(
        message=message,
        choices=items,
        style=style,
        border=True,
        info=True,
        max_height="70%",
    ).execute()


def pick_file(
    start_path: str = ".",
    message: str = "Select a file:",
    extensions: Optional[List[str]] = None,
    include_dirs: bool = False,
) -> Optional[str]:
    """
    Pick a file from a directory tree with fuzzy finding.

    Args:
        start_path: Starting directory to search from
        message: Question/title to display
        extensions: Filter by extensions (e.g., ['.py', '.txt'])
                   None means all files
        include_dirs: Whether to include directories in results

    Returns:
        Full path to selected file or None if cancelled

    Example:
        # Pick any Python file
        file = pick_file(".", "Select a Python file:", extensions=['.py'])

        # Pick any file or directory
        path = pick_file(".", "Select:", include_dirs=True)
    """
    start_path = Path(start_path).resolve()

    if not start_path.exists():
        print(f"Error: Path '{start_path}' does not exist")
        return None

    items = []

    # Walk through directory tree
    for root, dirs, files in os.walk(start_path):
        root_path = Path(root)
        try:
            rel_root = root_path.relative_to(start_path)
        except ValueError:
            continue

        # Add directories if requested
        if include_dirs:
            for d in dirs:
                items.append(str(rel_root / d) + "/")

        # Add files
        for f in files:
            # Filter by extension if specified
            if extensions:
                if not any(f.endswith(ext) for ext in extensions):
                    continue
            items.append(str(rel_root / f))

    if not items:
        print(
            f"No files found in {start_path}"
            + (f" with extensions {extensions}" if extensions else "")
        )
        return None

    items.sort()

    selected = inquirer.fuzzy(
        message=message,
        choices=items,
        border=True,
        info=True,
        max_height="70%",
    ).execute()

    if selected:
        return str(start_path / selected)
    return None


def pick_yaml_file(
    start_path: str = ".", message: str = "Select a YAML file:"
) -> Optional[str]:
    """
    Pick a YAML file (.yaml or .yml) from a directory tree.

    Args:
        start_path: Starting directory to search from
        message: Question/title to display

    Returns:
        Full path to selected YAML file or None if cancelled

    Example:
        config = pick_yaml_file("./configs", "Which config?")
        if config:
            with open(config) as f:
                data = yaml.safe_load(f)
    """
    start_path = Path(start_path).resolve()

    if not start_path.exists():
        print(f"Error: Path '{start_path}' does not exist")
        return None

    yaml_files = []

    # Search for .yaml files
    for file_path in start_path.rglob("*.yaml"):
        try:
            rel_path = file_path.relative_to(start_path)
            yaml_files.append(str(rel_path))
        except ValueError:
            continue

    # Search for .yml files
    for file_path in start_path.rglob("*.yml"):
        try:
            rel_path = file_path.relative_to(start_path)
            yaml_files.append(str(rel_path))
        except ValueError:
            continue

    if not yaml_files:
        print(f"No YAML files found in {start_path}")
        return None

    yaml_files.sort()

    selected = inquirer.fuzzy(
        message=message,
        choices=yaml_files,
        border=True,
        info=True,
        max_height="70%",
    ).execute()

    if selected:
        return str(start_path / selected)
    return None


def pick_from_json(
    file_path: str, message: str = "Select from JSON:"
) -> Optional[Tuple[str, Any]]:
    """
    Pick a key-value pair from a JSON file.

    Args:
        file_path: Path to JSON file
        message: Question/title to display

    Returns:
        Tuple of (key, value) or None if cancelled

    Example:
        key, value = pick_from_json("config.json", "Select config:")
        if key:
            print(f"Key: {key}, Value: {value}")
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{file_path}': {e}")
        return None

    if not isinstance(data, dict):
        print("Error: JSON file must contain an object/dictionary at root")
        return None

    # Format items as "key: value"
    items = [f"{key}: {json.dumps(value)}" for key, value in data.items()]

    selected = inquirer.fuzzy(
        message=message,
        choices=items,
        border=True,
        info=True,
        max_height="70%",
    ).execute()

    if selected:
        # Extract key from "key: value" format
        key = selected.split(": ", 1)[0]
        return (key, data[key])
    return None


def pick_from_yaml(
    file_path: str, message: str = "Select from YAML:"
) -> Optional[Tuple[str, Any]]:
    """
    Pick a key-value pair from a YAML file.

    Args:
        file_path: Path to YAML file
        message: Question/title to display

    Returns:
        Tuple of (key, value) or None if cancelled

    Example:
        key, value = pick_from_yaml("settings.yml", "Select setting:")
        if key:
            print(f"Setting: {key} = {value}")
    """
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML is required. Install with: pip install PyYAML")
        return None

    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in '{file_path}': {e}")
        return None

    if not isinstance(data, dict):
        print("Error: YAML file must contain a mapping/dictionary at root")
        return None

    # Format items as "key: value"
    items = [f"{key}: {value}" for key, value in data.items()]

    selected = inquirer.fuzzy(
        message=message,
        choices=items,
        border=True,
        info=True,
        max_height="70%",
    ).execute()

    if selected:
        # Extract key from "key: value" format
        key = selected.split(": ", 1)[0]
        return (key, data[key])
    return None


def pick_and_run(
    options: List[Tuple[str, Callable]], message: str = "Select an action:"
) -> Any:
    """
    Pick from a list of options and execute the associated function.

    Args:
        options: List of (label, function) tuples
        message: Question/title to display

    Returns:
        Return value of the executed function, or None if cancelled

    Example:
        def deploy():
            print("Deploying...")
            return "success"

        def test():
            print("Testing...")
            return "passed"

        result = pick_and_run([
            ("Deploy to production", deploy),
            ("Run tests", test),
        ], "What do you want to do?")

        print(f"Result: {result}")
    """
    if not options:
        print("Error: No options provided")
        return None

    # Extract just the labels for display
    labels = [opt[0] for opt in options]

    selected = inquirer.fuzzy(
        message=message,
        choices=labels,
        border=True,
        info=True,
        max_height="70%",
    ).execute()

    if selected:
        # Find and execute the corresponding function
        for label, func in options:
            if label == selected:
                return func()

    return None


# Import os for file walking
import os


# Example usage and tests
if __name__ == "__main__":
    print("=== FuzzyPicker Library Test ===\n")

    # Test 1: Pick from list
    print("Test 1: Pick from a list")
    actions = ["Deploy to production", "Run tests", "Backup database", "View logs"]
    selected = pick_from_list(actions, "What would you like to do?")
    print(f"✓ Selected: {selected}\n")

    # Test 2: Pick and run
    print("Test 2: Pick and run")

    def hello():
        print("👋 Hello World!")
        return "greeted"

    def goodbye():
        print("👋 Goodbye!")
        return "farewell"

    result = pick_and_run(
        [
            ("Say Hello", hello),
            ("Say Goodbye", goodbye),
        ],
        "What do you want to say?",
    )
    print(f"✓ Function returned: {result}\n")

    # Test 3: Pick file (commented out - uncomment to test)
    # file = pick_file(".", "Select a Python file:", extensions=['.py'])
    # print(f"✓ Selected file: {file}\n")
