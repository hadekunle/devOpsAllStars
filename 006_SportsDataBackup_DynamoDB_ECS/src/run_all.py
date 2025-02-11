# run_all.py
import subprocess
import time

from config import (
    RETRY_COUNT,
    RETRY_DELAY,
    WAIT_TIME_BETWEEN_SCRIPTS
)

def run_script(script_name, retries=RETRY_COUNT, delay=RETRY_DELAY):
    """
    Run a script with retry logic and a delay.
    """
    attempt = 0
    while attempt < retries:
        try:
            print(f"Running {script_name} (attempt {attempt + 1}/{retries})...")
            subprocess.run(["python", script_name], check=True)
            print(f"{script_name} completed successfully.")
            return
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_name}: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"{script_name} failed after {retries} attempts.")
                raise e

def main():
    try:
        # Step 1: Run fetch.py (fetch data, save to S3, and store in DynamoDB)
        run_script("fetch.py")

        print("Waiting for resources to stabilize...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)

        # Step 2: Run process_one_video.py (now processing all video URLs)
        run_script("process_one_video.py")

        print("Waiting for resources to stabilize...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)

        # Step 3: Run mediaconvert_process.py (if needed)
        run_script("mediaconvert_process.py")

        print("All scripts executed successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
