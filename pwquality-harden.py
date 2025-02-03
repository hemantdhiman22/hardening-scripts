import os
import shutil
import subprocess
import logging

# Configure logging
logging.basicConfig(
    filename="pwquality_update.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

pwquality_file = "/etc/security/pwquality.conf"
backup_file = "/etc/security/pwquality.conf.backup"

SETTINGS = {
    "minlen": "12",
    "dcredit": "1",
    "ucredit": "1",
    "lcredit": "1",
    "ocredit": "1"
}

def backup_config():
    """Creates a backup of the configuration file if it doesn't already exist."""
    try:
        if os.path.exists(pwquality_file):
            if os.path.exists(backup_file):
                logging.info(f"Backup already exists: {backup_file}")
                print("Backup already exists.")
            else:
                shutil.copy(pwquality_file, backup_file)
                logging.info(f"Backup created: {backup_file}")
                print("Backup file created.")
        else:
            logging.error(f"Configuration file does not exist: {pwquality_file}")
            print(f"Error: {pwquality_file} does not exist.")
            exit(1)  # Exit script if the config file is missing
    except Exception as e:
        logging.error(f"Failed to create backup: {str(e)}")
        print(f"Error: Failed to create backup. {e}")
        exit(1)

def update_config_with_sed():
    """Updates configuration values using sed, with error handling."""
    try:
        for key, value in SETTINGS.items():
            # Use sed to update existing values
            sed_cmd = f"sed -i -E 's|^#?\\s*{key}\\s*=.*|{key} = {value}|' {pwquality_file}"
            result = subprocess.run(sed_cmd, shell=True, check=True, stderr=subprocess.PIPE)

            if result.returncode == 0:
                logging.info(f"Updated: {key} = {value}")
            else:
                logging.warning(f"Sed command failed for key: {key}")

            # Check if the key was updated; if not, append it
            grep_cmd = f"grep -q '^{key} =' {pwquality_file} || echo '{key} = {value}' >> {pwquality_file}"
            subprocess.run(grep_cmd, shell=True, check=True, stderr=subprocess.PIPE)

        logging.info("Configuration updated successfully.")
        print("Configuration updated successfully.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to update configuration using sed: {e.stderr.decode().strip()}")
        print(f"Error: Failed to update configuration using sed. {e.stderr.decode().strip()}")
        exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"Error: {e}")
        exit(1)

# Run the script
backup_config()
update_config_with_sed()

