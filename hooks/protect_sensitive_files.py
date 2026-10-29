#!/usr/bin/env python3
import sys
import json
import os
from pathlib import Path
from fnmatch import fnmatch

def load_settings():
    """Load Claude settings and extract deny patterns."""
    settings_path = Path.home() / '.claude' / 'settings.json'
    try:
        with open(settings_path) as f:
            settings = json.load(f)
            deny_patterns = settings.get('permissions', {}).get('deny', [])
            return deny_patterns
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return []

def extract_path_pattern(deny_rule):
    """Extract file path pattern from deny rule like 'Read(./path/pattern)'."""
    if deny_rule.startswith('Read(') and deny_rule.endswith(')'):
        return deny_rule[5:-1]  # Remove 'Read(' and ')'
    return None

def matches_pattern(file_path, pattern):
    """Check if file path matches a deny pattern."""
    file_path = str(file_path)

    # If pattern has no path separator, match against filename only
    if '/' not in pattern and not pattern.startswith('./'):
        filename = os.path.basename(file_path)
        if fnmatch(filename, pattern):
            return True

    # Convert relative patterns to work with absolute paths
    if pattern.startswith('./'):
        # For patterns like './local/**', check if any part of the path matches
        pattern = pattern[2:]  # Remove './'
        # Check if the pattern matches any suffix of the path
        path_parts = file_path.split('/')
        for i in range(len(path_parts)):
            partial_path = '/'.join(path_parts[i:])
            if fnmatch(partial_path, pattern):
                return True
    else:
        # Direct pattern matching
        if fnmatch(file_path, pattern):
            return True
    
    return False

def main():
    """
    Main function to process the hook input and check for sensitive file access.
    """
    try:
        # Read the JSON data passed from Claude Code via stdin
        data = json.load(sys.stdin)
        tool_input = data.get('tool_input', {})
        file_path_str = tool_input.get('file_path')

        if not file_path_str:
            # If no file path is involved, the hook doesn't need to act.
            sys.exit(0)

        file_path = Path(file_path_str)
        
        # Load deny patterns from settings
        deny_rules = load_settings()
        
        # Check if the file path matches any deny pattern
        for rule in deny_rules:
            pattern = extract_path_pattern(rule)
            if pattern and matches_pattern(file_path, pattern):
                # Construct a clear, educational error message for the LLM
                error_message = (
                    f"SECURITY_POLICY_VIOLATION: Access to '{file_path}' is blocked by deny rule: {rule}\n"
                    f"Reason: This file matches a pattern in your Claude settings.json deny list.\n"
                    "Action: Files in denied paths contain sensitive information and should not be accessed by the AI."
                )
                
                # Print the error message to stderr
                print(error_message, file=sys.stderr)
                
                # Exit with code 2 to block the tool and feed stderr back to Claude
                sys.exit(2)

    except (json.JSONDecodeError, KeyError) as e:
        # Handle potential errors in the input data
        print(f"Error processing hook input: {e}", file=sys.stderr)
        # Exit with a non-blocking error code
        sys.exit(1)

    # If no sensitive file was detected, exit with 0 to allow the action
    sys.exit(0)

if __name__ == "__main__":
    main()
