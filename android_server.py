import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("android_control")

@mcp.tool()
def open_chrome_and_search(query: str) -> str:
    """Opens the default browser on the connected Android device and searches Google for the provided query."""
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '%20')}"
        subprocess.run(
            [
                "adb", "shell", "am", "start",
                "-a", "android.intent.action.VIEW",
                "-d", url
            ],
            check=True,
            stdout=subprocess.DEVNULL,   # Suppress stdout
            stderr=subprocess.DEVNULL    # Suppress stderr
        )
        return f"Opened browser and searched for: {query}"
    except subprocess.CalledProcessError as e:
        return f"Failed to open browser or search: {e}"

if __name__ == "__main__":
    mcp.run(transport='stdio')