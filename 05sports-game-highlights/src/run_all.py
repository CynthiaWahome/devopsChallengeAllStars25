import subprocess
import time

from config import {
    RETRY_COUNT,
    RETRY_DELAY,
    WAIT_TIME_BEWTWEEN_SCRIPTS
}

def run_script(script_name, retires=RETRY_COUNT, delay=RETRY_DELAY):
    attempt = 0

    while attempt < retries:
        try:
            print(f"Running {script_name} (attempt {attempt + 1}/{retries})...")
            subprocesss.run(["python", script_name], check=True)
            print(f"{script_name} completed successfully")
            return
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_name}: {e}")

            attempt += 1

            if attempt < retries:
                print(f"Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            else:
                print(f"{script_name} failed after {retries} attempts")
                raise e

def main():
    try:
        run_script("fetch.py")
        print("Waiting fo resources to stabilize...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)
        
        run_script("ffmpeg_process.py")
        print("All scripts executed successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ =="__main__":
    main()