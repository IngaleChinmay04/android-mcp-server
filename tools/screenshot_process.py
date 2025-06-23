import subprocess
import tempfile
from PIL import Image
import os

def screenshot_and_preprocess(max_dim: int = 1024, jpeg_quality: int = 85) -> str:
    """
    Takes a screenshot on the Android device, preprocesses it (resize, compress), and returns the local path.
    - max_dim: Maximum width or height of the image (default 1024px).
    - jpeg_quality: JPEG quality for compression (default 85).
    """
    try:
        device_path = "/sdcard/screen.png"
        # Create a temp file for the pulled screenshot
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        local_path = tmp.name
        tmp.close()

        # Take screenshot on device
        subprocess.run([
            "adb", "shell", "screencap", "-p", device_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Pull screenshot to local temp path (as PNG)
        raw_png = local_path.replace('.jpg', '.png')
        subprocess.run([
            "adb", "pull", device_path, raw_png
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Remove screenshot from device
        subprocess.run([
            "adb", "shell", "rm", device_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Preprocess: open, resize, and re-save as JPEG
        img = Image.open(raw_png)
        img.thumbnail((max_dim, max_dim))
        img = img.convert("RGB")  # Ensure JPEG compatible
        img.save(local_path, "JPEG", quality=jpeg_quality, optimize=True)
        os.remove(raw_png)  # Cleanup

        return f"Screenshot captured and preprocessed. Saved to {local_path}"
    except Exception as e:
        return f"Failed to capture or preprocess screenshot: {e}"