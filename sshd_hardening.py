import os 
import shutil
import subprocess

sshd_config="/etc/ssh/sshd_config"
sshd_config_backup="/etc/ssh/sshd_config.back"

HARDENED_SETTINGS = {
    "Protocol": "2",
    "PermitRootLogin": "no",
    "PasswordAuthentication": "no",
    "PermitEmptyPasswords": "no",
    "ChallengeResponseAuthentication": "no",
    "UsePAM": "yes",
    "X11Forwarding": "no",
    "AllowTcpForwarding": "no",
    "MaxAuthTries": "5",
    "LoginGraceTime": "30",
    "ClientAliveInterval": "600",
    "ClientAliveCountMax": "0",
    "IgnoreRhosts": "yes",
    "HostbasedAuthentication": "no",
    "MACs": "hmac-sha2-512,hmac-sha2-256",
    "Ciphers": "aes256-gcm@openssh.com,aes128-gcm@openssh.com",
    "KexAlgorithms": "curve25519-sha256,curve25519-sha256@libssh.org"
}

def backup_config():
    if os.path.exists(sshd_config):
        if os.path.exists(sshd_config_backup):
            print("Backup file already exists")
        else:
            shutil.copy(sshd_config,sshd_config_backup)
            print("Backup created. Path: {sshd_config_backup}")
    else:
        print(f"file {sshd_config} does not exits, check file path and file name.")

def check_existing_parameters():
    existing_config={}
    if os.path.exists(sshd_config):
        print("file exists")
        with open(sshd_config, "r") as sshd_file:
            for line in sshd_file:
                new_line=line.strip()
                if new_line and not new_line.startswith("#"):
                    part=new_line.split(maxsplit=1)
                    if len(part) == 2:
                        a = part[0]
                        b = part[1]
                        if a in HARDENED_SETTINGS:
                           existing_config[a]=b
    else:
        print("path not exists")
    return existing_config

def update_config():
    call_existing_config = check_existing_parameters()
    update_config_line=[]

    striped_lines = []
    with open(sshd_config, "r") as sshd_file:
        for i in sshd_file:
            striped_lines=i.strip()
            if striped_lines and not striped_lines.startswith("#"):
                part=striped_lines.split(maxsplit=1)
                if len(part) == 2:
                    a,b=part
                    if a in HARDENED_SETTINGS:
                        update_config_line.append(f"{a} {HARDENED_SETTINGS[a]}\n")
                    else:
                        update_config_line.append(i)
                else:
                    update_config_line.append(i)
            else:
                update_config_line.append(i)

    for key, value in HARDENED_SETTINGS.items():
        if key not in call_existing_config:
            update_config_line.append(f"{key} {value}\n")
    
    with open(sshd_config, "w") as sshd_file:
        sshd_file.writelines(update_config_line)


def restart_ssh_service():
    """Restart the SSH service to apply the new configuration."""
    try:
        print("Restarting SSH service...")
        subprocess.run(["systemctl", "restart", "sshd"], check=True)
        print("SSH service restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error restarting SSH service: {e}")

def main():
    backup_config()
    update_config()

if __name__ == "__main__":
    main()
