# run_all.py

# Import the 'subprocess' module to run external scripts as subprocesses
import subprocess

# Import the 'time' module to handle delays between script executions
import time

# Import specific configuration variables from the 'config.py' module
from config import (
    RETRY_COUNT,               # The number of retry attempts for failed scripts
    RETRY_DELAY,               # The delay (in seconds) between retry attempts
    WAIT_TIME_BETWEEN_SCRIPTS  # The waiting time (in seconds) between different scripts
)

def run_script(script_name, retries=RETRY_COUNT, delay=RETRY_DELAY):
    """
    Run a script with retry logic and a delay.
    
    This function attempts to execute a given Python script using subprocess.
    If the script fails, it retries the execution up to a specified number of times,
    waiting for a specified delay between attempts.
    
    Args:
        script_name (str): The name of the Python script to execute.
        retries (int, optional): The maximum number of retry attempts. Defaults to RETRY_COUNT.
        delay (int, optional): The delay in seconds between retry attempts. Defaults to RETRY_DELAY.
    
    Raises:
        subprocess.CalledProcessError: If the script fails after all retry attempts.
    """
    # Initialize the attempt counter to zero
    attempt = 0
    
    # Continue attempting to run the script until the maximum number of retries is reached
    while attempt < retries:
        try:
            # Inform the user that the script is being run, including the current attempt number
            print(f"Running {script_name} (attempt {attempt + 1}/{retries})...")
            
            # Execute the script as a subprocess
            # 'check=True' ensures that a CalledProcessError is raised if the script exits with a non-zero status
            subprocess.run(["python", script_name], check=True)
            
            # Inform the user that the script completed successfully
            print(f"{script_name} completed successfully.")
            
            # Exit the function if the script ran successfully
            return
        except subprocess.CalledProcessError as e:
            # Inform the user that an error occurred while running the script
            print(f"Error running {script_name}: {e}")
            
            # Increment the attempt counter
            attempt += 1
            
            # Check if the maximum number of retries has not been reached
            if attempt < retries:
                # Inform the user that the script will be retried after a delay
                print(f"Retrying in {delay} seconds...")
                
                # Wait for the specified delay before retrying
                time.sleep(delay)
            else:
                # Inform the user that the script has failed after all retry attempts
                print(f"{script_name} failed after {retries} attempts.")
                
                # Re-raise the exception to propagate the error
                raise e

def main():
    """
    Main function to orchestrate the execution of multiple scripts in a pipeline.
    
    This function runs a series of Python scripts in a specific order, introducing
    delays between them to ensure that resources are stabilized before the next script runs.
    It handles any exceptions that occur during the execution of the scripts.
    """
    try:
        # Step 1: Run fetch.py
        run_script("fetch.py")

        # Buffer time between scripts to allow resources to stabilize
        print("Waiting for resources to stabilize...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)

        # Step 2: Run process_one_video.py
        run_script("process_one_video.py")

        # Buffer time between scripts to allow resources to stabilize
        print("Waiting for resources to stabilize...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)

        # Step 3: Run mediaconvert_process.py
        run_script("mediaconvert_process.py")

        # Inform the user that all scripts have been executed successfully
        print("All scripts executed successfully.")
    except Exception as e:
        # Inform the user that the pipeline has failed and provide the error details
        print(f"Pipeline failed: {e}")

# Check if this script is being run as the main program
# If so, execute the 'main' function
if __name__ == "__main__":
    main()
