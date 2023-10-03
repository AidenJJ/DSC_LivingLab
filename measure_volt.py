import subprocess

def get_voltage():
    try:
        result = subprocess.run(['vcgencmd', 'measure_volts'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout.strip()
        return output
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    voltage_info = get_voltage()
    if voltage_info:
        print(f"Voltage Info: {voltage_info}")