import subprocess
import re

def get_device_model():
    """Returns the device model, manufacturer, and Android version."""
    model = subprocess.run(['adb', 'shell', 'getprop', 'ro.product.model'], capture_output=True, text=True).stdout.strip()
    manufacturer = subprocess.run(['adb', 'shell', 'getprop', 'ro.product.manufacturer'], capture_output=True, text=True).stdout.strip()
    android_version = subprocess.run(['adb', 'shell', 'getprop', 'ro.build.version.release'], capture_output=True, text=True).stdout.strip()
    return {
        "manufacturer": manufacturer,
        "model": model,
        "android_version": android_version
    }


def get_battery_info():
    """Returns battery level, status, temperature, and health."""
    result = subprocess.run(['adb', 'shell', 'dumpsys', 'battery'], capture_output=True, text=True).stdout
    info = {}
    for line in result.splitlines():
        if ':' in line:
            key, val = line.split(':', 1)
            info[key.strip()] = val.strip()
    # Clean and format data
    return {
        "level": info.get("level"),
        "status": info.get("status"),
        "health": info.get("health"),
        "temperature_C": float(info.get("temperature", 0))/10 if "temperature" in info else None,
        "voltage_mV": info.get("voltage")
    }


def get_device_features():
    """Returns a list of feature strings supported by the device."""
    result = subprocess.run(['adb', 'shell', 'pm', 'list', 'features'], capture_output=True, text=True).stdout
    features = [line.replace('feature:', '').strip() for line in result.splitlines() if 'feature:' in line]
    return features


def get_storage_info():
    """Returns internal storage total and available (in bytes)."""
    result = subprocess.run(['adb', 'shell', 'df', '/data'], capture_output=True, text=True).stdout
    lines = result.splitlines()
    if len(lines) >= 2:
        headers = re.split(r'\s+', lines[0])
        values = re.split(r'\s+', lines[1])
        info = dict(zip(headers, values))
        return {
            "filesystem": info.get('Filesystem', ''),
            "total": info.get('Size', ''),
            "used": info.get('Used', ''),
            "available": info.get('Available', ''),
            "use%": info.get('Use%', '')
        }
    return {}



def get_network_info():
    """Returns IP address and connected Wi-Fi SSID (if any)."""
    ip_result = subprocess.run(['adb', 'shell', 'ip', 'addr', 'show', 'wlan0'], capture_output=True, text=True).stdout
    ssid_result = subprocess.run(['adb', 'shell', 'dumpsys', 'wifi'], capture_output=True, text=True).stdout
    ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', ip_result)
    ssid_match = re.search(r'SSID: ([^\s]+)', ssid_result)
    return {
        "ip_address": ip_match.group(1) if ip_match else None,
        "wifi_ssid": ssid_match.group(1) if ssid_match else None
    }
