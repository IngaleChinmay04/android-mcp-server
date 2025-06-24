from mcp.server.fastmcp import FastMCP
from tools.screenshot_process import screenshot_and_preprocess
from tools.chrome_search import open_chrome_and_search
from tools.sms_sender import send_sms_via_adb
from tools.system_info import get_device_model, get_battery_info, get_device_features, get_storage_info, get_network_info

# Initialize the FastMCP server with a specific name
# This name can be used to identify the server instance.
mcp = FastMCP("android_control") 

# Register the tools with the MCP server
# These tools can be called remotely via the MCP protocol.
mcp.tool()(screenshot_and_preprocess)
mcp.tool()(open_chrome_and_search)
mcp.tool()(send_sms_via_adb)
mcp.tool()(get_device_model)
mcp.tool()(get_battery_info)
mcp.tool()(get_device_features)
mcp.tool()(get_storage_info)
mcp.tool()(get_network_info)

# Start the MCP server  
if __name__ == "__main__":
    mcp.run(transport='stdio')