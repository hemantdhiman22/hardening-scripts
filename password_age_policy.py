import os 
import shutil
import subprocess


login_def="/etc/login.defs"
backup_file="/etc/login.defs.backup"

SETTING={ "PASS_MAX_DAYS": "90",
         "PASS_MIN_DAYS": "1",
         "PASS_WARN_AGE": "7"
        }

def backup_config():
    if os.path.exists(login_def):
        if os.path.exists(backup_file):
            print("Backup file already exist")
        else:
            shutil.copy(login_def, backup_file)
            print("Backup file created")
    else:
        print(f"{login_def} file does not exists")

def check_existing_parameters():
    existing_config={}
    if os.path.exists(login_def):
        with open(login_def, "r") as file:
            for line in file:
                new_line=line.strip()
                if new_line and not new_line.startswith("#"):
                    part=new_line.split(maxsplit=1)
                    if len(part) == 2:
                        a = part[0]
                        b = part[1]
                        if a in SETTING:
                            existing_config[a]=b
    else:
        print("file does not exist")
    print(existing_config)
    return existing_config

def update_config():
    call_existing_config=check_existing_parameters()
    update_config_line=[]

    with open(login_def, "r") as login_def_file:
        for line in login_def_file:
            new_line=line.strip()
            if new_line and not new_line.startswith("#"):
                part=new_line.split(maxsplit=1)
                if len(part) == 2:
                    a,b=part
                    if a in SETTING:
                        update_config_line.append(f"{a} {SETTING[a]}\n")
                    else:
                        update_config_line.append(line)
                else:
                    update_config_line.append(line)
            else:
                update_config_line.append(line)

    for key, value in SETTING.items():
        if key not in call_existing_config:
            update_config_line.append(f"{key} {value}\n")

    with open(login_def, "w") as login_def_file:
        login_def_file.writelines(update_config_line)


def main():
    backup_config()
    update_config()

if __name__ == "__main__":
    main()



    
