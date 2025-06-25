import subprocess

def take_screenshot(filename="screenshot.png"):
    """Takes a screenshot on the device and pulls it to your computer."""
    subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/temp_screen.png'])
    subprocess.run(['adb', 'pull', '/sdcard/temp_screen.png', filename])
    subprocess.run(['adb', 'shell', 'rm', '/sdcard/temp_screen.png'])

def open_settings():
    """Opens the system settings app."""
    subprocess.run(['adb', 'shell', 'am', 'start', '-a', 'android.settings.SETTINGS'])

def toggle_airplane_mode(on=True):
    """Enables or disables airplane mode."""
    mode = '1' if on else '0'
    subprocess.run(['adb', 'shell', 'settings', 'put', 'global', 'airplane_mode_on', mode])
    subprocess.run(['adb', 'shell', 'am', 'broadcast', '-a', 'android.intent.action.AIRPLANE_MODE'])

def increase_volume():
    """Increases the media volume by one step."""
    subprocess.run(['adb', 'shell', 'input', 'keyevent', '24'])  # KEYCODE_VOLUME_UP

def decrease_volume():
    """Decreases the media volume by one step."""
    subprocess.run(['adb', 'shell', 'input', 'keyevent', '25'])  # KEYCODE_VOLUME_DOWN

def press_power_button():
    """Simulates pressing the power button (locks/unlocks screen)."""
    subprocess.run(['adb', 'shell', 'input', 'keyevent', '26'])  # KEYCODE_POWER

def press_home_button():
    """Simulates pressing the home button."""
    subprocess.run(['adb', 'shell', 'input', 'keyevent', '3'])   # KEYCODE_HOME

def press_back_button():
    """Simulates pressing the back button."""
    subprocess.run(['adb', 'shell', 'input', 'keyevent', '4'])   # KEYCODE_BACK
