import os
import json
import argparse
from pathlib import Path
from mcp.server.fastmcp import FastMCP

parser = argparse.ArgumentParser()
parser.add_argument("--data", help="Expanded PLUGIN_DATA path from CLI args")
args, _ = parser.parse_known_args()

mcp = FastMCP("path-location-server")

def load_config_paths() -> dict:
    """Load config.json and expand embedded environment variables."""
    config_path = Path(__file__).parent / "config.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    k: os.path.expandvars(v) if isinstance(v, str) else v
                    for k, v in data.items()
                }
        except Exception as e:
            return {"error": f"Failed to load config: {e}"}
    return {}

CONFIG_PATHS = load_config_paths()

@mcp.tool()
def get_path_locations() -> dict:
    """Get the resolved path locations for PLUGIN_ROOT and PLUGIN_DATA."""
    return {
        "config_plugin_root": CONFIG_PATHS.get("root_location"),
        "config_plugin_data": CONFIG_PATHS.get("data_location"),
        "env_plugin_root": os.environ.get("PLUGIN_ROOT", "<NOT SET>"),
        "env_plugin_data": os.environ.get("PLUGIN_DATA", "<NOT SET>"),
        "cli_arg_plugin_data": args.data or "<NOT PASSED>",
    }

if __name__ == "__main__":
    mcp.run()