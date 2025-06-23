from mcp.server.fastmcp import FastMCP
from tools.screenshot_process import screenshot_and_preprocess
from tools.chrome_search import open_chrome_and_search

# Initialize the FastMCP server with a specific name
# This name can be used to identify the server instance.
mcp = FastMCP("android_control") 

# Register the tools with the MCP server
# These tools can be called remotely via the MCP protocol.
mcp.tool()(screenshot_and_preprocess)
mcp.tool()(open_chrome_and_search)


# Start the MCP server  
if __name__ == "__main__":
    mcp.run(transport='stdio')