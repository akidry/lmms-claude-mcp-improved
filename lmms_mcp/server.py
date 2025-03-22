"""
MCP Server for LMMS integration with Claude AI.
"""

import logging
import json
import asyncio
import argparse
from typing import Dict, Any, List, Optional, Union, Tuple
from model_context_protocol import MCPServer as BaseMCPServer
from model_context_protocol.capabilities import Capability, CapabilityParameter, ParameterType
from .lmms_interface import LMMSInterface

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default settings
DEFAULT_SERVER_HOST = "127.0.0.1"
DEFAULT_SERVER_PORT = 8000
DEFAULT_LMMS_HOST = "127.0.0.1"
DEFAULT_LMMS_PORT = 9000

class MCPServer:
    """Model Context Protocol server for LMMS integration."""
    
    def __init__(self, server_host: str = DEFAULT_SERVER_HOST, server_port: int = DEFAULT_SERVER_PORT,
                 lmms_host: str = DEFAULT_LMMS_HOST, lmms_port: int = DEFAULT_LMMS_PORT):
        """
        Initialize the MCP server.
        
        Args:
            server_host: The hostname to run the MCP server on
            server_port: The port to run the MCP server on
            lmms_host: The hostname where LMMS is running
            lmms_port: The OSC port that LMMS listens on
        """
        self.server_host = server_host
        self.server_port = server_port
        self.lmms_interface = LMMSInterface(lmms_host, lmms_port)
        self.capabilities = self._register_capabilities()
        self.server = BaseMCPServer(self.capabilities)
        
    def _register_capabilities(self) -> List[Capability]:
        """Register all available capabilities for the MCP protocol."""
        capabilities = [
            Capability(
                name="get_session_info",
                description="Get detailed information about the current LMMS session",
                parameters={},
                handler=self.get_session_info
            ),
            Capability(
                name="get_track_info",
                description="Get detailed information about a specific track in LMMS",
                parameters={
                    "track_index": CapabilityParameter(type=ParameterType.INTEGER, required=True)
                },
                handler=self.get_track_info
            ),
            Capability(
                name="create_track",
                description="Create a new track in the LMMS session",
                parameters={
                    "track_type": CapabilityParameter(type=ParameterType.STRING, default="instrument"),
                    "name": CapabilityParameter(type=ParameterType.STRING, required=False)
                },
                handler=self.create_track
            ),
            Capability(
                name="set_track_name",
                description="Set the name of a track",
                parameters={
                    "track_index": CapabilityParameter(type=ParameterType.INTEGER, required=True),
                    "name": CapabilityParameter(type=ParameterType.STRING, required=True)
                },
                handler=self.set_track_name
            ),
            Capability(
                name="create_pattern",
                description="Create a new pattern in a track",
                parameters={
                    "track_index": CapabilityParameter(type=ParameterType.INTEGER, required=True),
                    "steps": CapabilityParameter(type=ParameterType.INTEGER, default=16)
                },
                handler=self.create_pattern
            ),
            Capability(
                name="add_notes_to_pattern",
                description="Add notes to a pattern",
                parameters={
                    "track_index": CapabilityParameter(type=ParameterType.INTEGER, required=True),
                    "pattern_index": CapabilityParameter(type=ParameterType.INTEGER, required=True),
                    "notes": CapabilityParameter(type=ParameterType.ARRAY, required=True)
                },
                handler=self.add_notes_to_pattern
            ),
            Capability(
                name="load_instrument",
                description="Load an instrument into a track",
                parameters={
                    "track_index": CapabilityParameter(type=ParameterType.INTEGER, required=True),
                    "instrument_path": CapabilityParameter(type=ParameterType.STRING, required=True)
                },
                handler=self.load_instrument
            ),
            Capability(
                name="set_tempo",
                description="Set the tempo of the LMMS session",
                parameters={
                    "tempo": CapabilityParameter(type=ParameterType.NUMBER, required=True)
                },
                handler=self.set_tempo
            ),
            Capability(
                name="play",
                description="Start playback of the LMMS session",
                parameters={},
                handler=self.play
            ),
            Capability(
                name="stop",
                description="Stop playback of the LMMS session",
                parameters={},
                handler=self.stop
            ),
            Capability(
                name="new_project",
                description="Create a new LMMS project",
                parameters={},
                handler=self.new_project
            ),
            Capability(
                name="save_project",
                description="Save the current LMMS project",
                parameters={
                    "path": CapabilityParameter(type=ParameterType.STRING, required=False)
                },
                handler=self.save_project
            ),
            Capability(
                name="get_instruments_list",
                description="Get a list of available instruments",
                parameters={},
                handler=self.get_instruments_list
            )
        ]
        
        return capabilities
        
    async def start(self):
        """Start the MCP server."""
        # First start the LMMS interface's OSC server
        transport = await self.lmms_interface.start_server()
        
        # Then start the MCP server
        logger.info(f"Starting MCP server on {self.server_host}:{self.server_port}")
        await self.server.start(host=self.server_host, port=self.server_port)
            
    # Function implementations
    async def get_session_info(self) -> Dict[str, Any]:
        """Get information about the current LMMS session."""
        return await self.lmms_interface.get_session_info()
    
    async def get_track_info(self, track_index: int) -> Dict[str, Any]:
        """Get information about a specific track."""
        return await self.lmms_interface.get_track_info(track_index)
    
    async def create_track(self, track_type: str = "instrument", name: str = None) -> Dict[str, Any]:
        """Create a new track."""
        return await self.lmms_interface.create_track(track_type, name)
    
    async def set_track_name(self, track_index: int, name: str) -> Dict[str, Any]:
        """Set the name of a track."""
        return await self.lmms_interface.set_track_name(track_index, name)
    
    async def create_pattern(self, track_index: int, steps: int = 16) -> Dict[str, Any]:
        """Create a new pattern for a track."""
        return await self.lmms_interface.create_pattern(track_index, steps)
    
    async def add_notes_to_pattern(self, track_index: int, pattern_index: int, notes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add notes to a pattern."""
        return await self.lmms_interface.add_notes_to_pattern(track_index, pattern_index, notes)
    
    async def load_instrument(self, track_index: int, instrument_path: str) -> Dict[str, Any]:
        """Load an instrument for a track."""
        return await self.lmms_interface.load_instrument(track_index, instrument_path)
    
    async def set_tempo(self, tempo: float) -> Dict[str, Any]:
        """Set the project tempo in BPM."""
        return await self.lmms_interface.set_tempo(tempo)
    
    async def play(self) -> Dict[str, Any]:
        """Start playback."""
        return await self.lmms_interface.play()
    
    async def stop(self) -> Dict[str, Any]:
        """Stop playback."""
        return await self.lmms_interface.stop()
    
    async def new_project(self) -> Dict[str, Any]:
        """Create a new project."""
        return await self.lmms_interface.new_project()
    
    async def save_project(self, path: str = None) -> Dict[str, Any]:
        """Save the current project."""
        return await self.lmms_interface.save_project(path)
    
    async def get_instruments_list(self) -> Dict[str, Any]:
        """Get a list of available instruments."""
        return await self.lmms_interface.get_instruments_list()

def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="LMMS MCP Server")
    parser.add_argument("--host", default=DEFAULT_SERVER_HOST, help="Server host")
    parser.add_argument("--port", type=int, default=DEFAULT_SERVER_PORT, help="Server port")
    parser.add_argument("--lmms-host", default=DEFAULT_LMMS_HOST, help="LMMS host")
    parser.add_argument("--lmms-port", type=int, default=DEFAULT_LMMS_PORT, help="LMMS port")
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create and start the server
    server = MCPServer(args.host, args.port, args.lmms_host, args.lmms_port)
    
    logger.info(f"Starting LMMS MCP server on {args.host}:{args.port}")
    logger.info(f"Connecting to LMMS on {args.lmms_host}:{args.lmms_port}")
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")

if __name__ == "__main__":
    main()