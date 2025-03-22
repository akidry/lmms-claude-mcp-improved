"""
Command-line interface for LMMS-Claude-MCP.
"""

import sys
import argparse
import logging
import asyncio

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="LMMS-Claude-MCP: LMMS integration with Claude AI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Server command
    server_parser = subparsers.add_parser("server", help="Run the MCP server")
    server_parser.add_argument("--host", default="127.0.0.1", help="Server host")
    server_parser.add_argument("--port", type=int, default=8000, help="Server port")
    server_parser.add_argument("--lmms-host", default="127.0.0.1", help="LMMS host")
    server_parser.add_argument("--lmms-port", type=int, default=9000, help="LMMS port")
    
    # Remote command
    remote_parser = subparsers.add_parser("remote", help="Run the LMMS remote script")
    remote_parser.add_argument("--listening-host", default="127.0.0.1", help="Listening host")
    remote_parser.add_argument("--listening-port", type=int, default=9000, help="Listening port")
    remote_parser.add_argument("--client-host", default="127.0.0.1", help="Client host")
    remote_parser.add_argument("--client-port", type=int, default=9001, help="Client port")
    
    args = parser.parse_args()
    
    # Default to server if no command is provided
    if not args.command:
        args.command = "server"
    
    try:
        if args.command == "server":
            from .server import MCPServer
            server = MCPServer(args.host, args.port, args.lmms_host, args.lmms_port)
            asyncio.run(server.start())
        elif args.command == "remote":
            from .lmms_remote import LMMSRemoteScript, main as remote_main
            remote = LMMSRemoteScript(args.listening_host, args.listening_port, 
                                      args.client_host, args.client_port)
            remote_main()
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()