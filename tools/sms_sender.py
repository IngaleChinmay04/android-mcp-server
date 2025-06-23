import xml.etree.ElementTree as ET
import subprocess
import re
import time
import os

def send_sms_via_adb(phone_number: str, message: str, wait_time: float = 5.0):
    """
    Sends an SMS via ADB automation.
    Usage: send_sms_via_adb("+919145097166", "Hello!", wait_time=7.0)
    Returns a formatted result message indicating success or the reason for failure.
    """
    # Ensure multi-word message is wrapped in double quotes for Windows/ADB parsing
    safe_message = f'"{message}"'

    proc = subprocess.run([
        'adb', 'shell', 'am', 'start',
        '-a', 'android.intent.action.SENDTO',
        '-d', f'sms:{phone_number}',
        '--es', 'sms_body', safe_message
    ], capture_output=True, text=True)

    # Optional: print for debugging
    # print("STDOUT:", proc.stdout)
    # print("STDERR:", proc.stderr)

    time.sleep(wait_time)
    subprocess.run(['adb', 'shell', 'uiautomator', 'dump', '/sdcard/view.xml'])
    subprocess.run(['adb', 'pull', '/sdcard/view.xml'])

    if not os.path.exists('view.xml'):
        return "UI dump failed: view.xml not found. The UI may not have loaded, or the dump command failed."

    with open('view.xml', 'r', encoding='utf-8') as f:
        xml_content = f.read()

    if not xml_content.strip().startswith('<?xml'):
        return f"UI dump failed: file is not valid XML. First 100 characters:\n{xml_content[:100]}"

    try:
        root = ET.fromstring(xml_content)
    except Exception as e:
        return f"XML parsing failed: {e}"

    send_button = None
    for node in root.iter('node'):
        if (node.get('text') and node.get('text').strip().lower() == 'send') or \
           (node.get('content-desc') and node.get('content-desc').strip().lower() == 'send') or \
           (node.get('resource-id') and 'send' in node.get('resource-id').lower()):
            send_button = node
            break

    try:
        os.remove('view.xml')
    except Exception as e:
        return f"Could not delete view.xml: {e}"

    if not send_button:
        return "Send button not found in the dumped XML. The UI may not have rendered, the message may be empty, or the button label may differ."

    bounds = send_button.get('bounds')
    match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
    if not match:
        return f"Could not parse Send button bounds: {bounds}"

    x1, y1, x2, y2 = map(int, match.groups())
    tap_x = (x1 + x2) // 2
    tap_y = (y1 + y2) // 2

    subprocess.run(['adb', 'shell', 'input', 'tap', str(tap_x), str(tap_y)])
    return f"SMS sent to {phone_number} by tapping coordinates ({tap_x}, {tap_y})."