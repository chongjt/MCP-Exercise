
import os
from datetime import datetime
from pathlib import Path
import requests

# Simulate MCP server decorator
def tool(func):
    print(f"Tool Registered: {func.__name__}")
    return func

# Simulate server startup
print("Starting MCP server...")

@tool
def say_hello(name: str) -> str:
    """Say hello to someone"""
    return f"Hello, {name}! Welcome to MCP."

@tool
def list_directory(directory_path: str) -> list:
    """List the contents of a directory (basic)"""
    try:
        return os.listdir(directory_path)
    except FileNotFoundError:
        return "Directory not found"
    except PermissionError:
        return "Permission denied"

@tool
def get_weather(location: str) -> str:
    """Fetch current weather using wttr.in"""
    try:
        url = f"https://wttr.in/{location}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Error: Status {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

@tool
def list_details(directory_path: str) -> list:
    """List directory with details: name, size, type, last modified"""
    path = Path(directory_path)
    if not path.exists():
        return "Directory not found"
    if not path.is_dir():
        return "Not a directory"
    result = []
    for item in path.iterdir():
        stat = item.stat()
        size = stat.st_size
        is_dir = item.is_dir()
        last_modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        result.append({
            'name': item.name,
            'size': size,
            'type': 'directory' if is_dir else 'file',
            'last_modified': last_modified
        })
    return result

# Testing all tools locally
if __name__ == "__main__":
    print("\n>>> say_hello(\"Chelyn\")")
    print(say_hello("Chelyn"))

    print("\n>>> list_directory(\".\")")
    print(list_directory("."))

    print("\n>>> get_weather(\"Singapore\")")
    print(get_weather("Singapore"))

    print("\n>>> list_details(\".\")")
    detailed_output = list_details(".")
    for entry in detailed_output if isinstance(detailed_output, list) else [detailed_output]:
        print(entry)
