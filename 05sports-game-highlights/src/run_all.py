import subprocess
import time

from config import (
    RETRY_COUNT,
    RETRY_DELAY,
    WAIT_TIME_BETWEEN_SCRIPTS
)

def run_script(script_name, retries=RETRY_COUNT, delay=RETRY_DELAY):
    attempt = 0

    while attempt < retries:
        try:
            print(f"Running {script_name} (attempt {attempt + 1}/{retries})...")
            subprocess.run(["python", script_name], check=True)
            break
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_name}: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to run {script_name} after {retries} attempts.")
                raise

if __name__ == "__main__":
    scripts = ["fetch.py", "process_one_video.py"]
    for script in scripts:
        run_script(script)
        print(f"Waiting {WAIT_TIME_BETWEEN_SCRIPTS} seconds before running the next script...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)