from mcp.server.fastmcp import FastMCP

import json
import requests
import asyncio

# Create an MCP server
mcp = FastMCP("Demo")

@mcp.tool()
async def joke() -> str:
    """Get joke"""
    res = requests.get("https://api.chucknorris.io/jokes/random")
    json_response = res.json()

    return json_response.get("value", "No joke found.")

@mcp.tool()
async def joke_param(category: str = "sport") -> str:
    """Get joke with parameter"""
    
    res = requests.get(f"https://api.chucknorris.io/jokes/random?category={category}")
    json_response = res.json()

    return json_response.get("value", "No joke found.")

if __name__ == "__main__":
    print("Running server")
    mcp.run()