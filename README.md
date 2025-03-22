# LMMS-Claude-MCP

LMMS integration with Claude AI through Model Context Protocol (MCP), inspired by [ableton-mcp](https://github.com/ahujasid/ableton-mcp).

## Overview

LMMS-Claude-MCP connects LMMS to Claude AI through the Model Context Protocol (MCP), allowing Claude to directly interact with and control LMMS. This integration enables prompt-assisted music production, track creation, and session manipulation in LMMS.

## Features

* Two-way communication: Connect Claude AI to LMMS through a Python-based MCP server
* Track manipulation: Create, modify, and manipulate MIDI tracks
* Instrument and effect selection: Claude can access and load instruments and effects in LMMS
* Pattern creation: Create and edit MIDI patterns with notes
* Project control: Basic control over LMMS project

## Components

The system consists of two main components:

1. LMMS Integration Module: Python code that interacts with LMMS through its Remote Control API
2. MCP Server: A Python server that implements the Model Context Protocol and connects to LMMS

## Installation

### Prerequisites

* LMMS 1.2 or newer
* Python 3.8 or newer
* uv package manager (recommended) or pip

If you're on Mac, please install uv as:

```bash
brew install uv
```

Otherwise, install from [uv's official website](https://docs.astral.sh/uv/getting-started/installation/)

### Installation Methods

#### Method 1: Install from GitHub directly using uv (Recommended)

```bash
uv pip install git+https://github.com/akidry/lmms-claude-mcp-improved.git
```

#### Method 2: Clone and install locally

```bash
# Clone the repository
git clone https://github.com/akidry/lmms-claude-mcp-improved.git
cd lmms-claude-mcp-improved

# Install with uv
uv pip install -e .

# Or install with pip
pip install -e .
```

#### Method 3: Use with `uvx` without installation

```bash
# Run directly without installing
uvx https://github.com/akidry/lmms-claude-mcp-improved.git lmms-mcp
```

### Verify Installation

After installation, you should be able to run:

```bash
lmms-mcp --help
```

If you get a help message, the installation was successful.

### Claude for Desktop Integration

1. Go to Claude > Settings > Developer > Edit Config > claude_desktop_config.json to include the following:

```json
{ 
  "mcpServers": { 
    "LMMSMCP": { 
      "command": "lmms-mcp", 
      "args": [] 
    } 
  } 
}
```

If using uvx without installation:

```json
{ 
  "mcpServers": { 
    "LMMSMCP": { 
      "command": "uvx", 
      "args": [ "https://github.com/akidry/lmms-claude-mcp-improved.git", "lmms-mcp" ] 
    } 
  } 
}
```

### Cursor Integration

Add this to Cursor Settings > MCP:

```
lmms-mcp
```

If using uvx without installation:

```
uvx https://github.com/akidry/lmms-claude-mcp-improved.git lmms-mcp
```

⚠️ Only run one instance of the MCP server (either on Cursor or Claude Desktop), not both

## Usage

### Starting the Connection

1. Launch LMMS
2. Ensure the MCP server is configured in Claude Desktop or Cursor
3. The connection should be established automatically when you interact with Claude

### Using with Claude

Once the server is running, you can interact with Claude AI to control LMMS. For example, you can ask Claude to:

* "Create a new project with a synth bass track"
* "Add a drum pattern"
* "Create a melody for the chorus"
* "Set the tempo to 120 BPM"

## Troubleshooting

### Common Issues

#### Package Not Found or Dependencies Error

```
No solution found when resolving tool dependencies:
Because lmms-mcp was not found in the package registry...
```

**Solution**: 
- Make sure you've installed the package using one of the methods above
- Try installing directly from GitHub with: `uv pip install git+https://github.com/akidry/lmms-claude-mcp-improved.git`
- Ensure you have the required dependencies: `python-osc>=1.8.0`, `websockets>=10.0`, and `model-context-protocol>=0.1.0`

#### Connection Issues

**Solution**:
- Ensure LMMS is running before starting the MCP server
- Check that the ports (default: 8000 for MCP, 9000 for LMMS) are not blocked by a firewall
- Look for error messages in the console output

#### Command Not Found

**Solution**:
- If `lmms-mcp` command is not found, make sure the package is properly installed
- Check that your Python environment's bin directory is in your PATH
- Try using the full path to the command or use `python -m lmms_mcp.cli`

### Advanced Debugging

For detailed debugging, you can run the server manually with verbose logging:

```bash
lmms-mcp server --host 127.0.0.1 --port 8000 --lmms-host 127.0.0.1 --lmms-port 9000
```

## Technical Details

### Communication Protocol

The system uses a JSON-based protocol over TCP sockets:

* Commands are sent as JSON objects with a type and optional params
* Responses are JSON objects with a status and result or message

### Limitations

* LMMS has more limited remote control capabilities compared to Ableton Live
* Some features may require LMMS to be in specific modes or states
* Complex musical arrangements might need to be broken down into smaller steps

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This is a third-party integration and not made by LMMS or Anthropic.