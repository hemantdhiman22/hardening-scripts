import os
import subprocess

working_dir="/opt"

os.chdir(working_dir)
log_file="/opt/sshd_upgrade.log"

commands = [
    "sudo yum group install -y 'Development Tools'",
    "sudo yum install -y zlib-devel openssl-devel",
    "sudo yum install -y pam-devel libselinux-devel",
    "wget -c https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-9.9p1.tar.gz",
    "tar -xzf openssh-9.9p1.tar.gz",
    "cd openssh-9.9p1 && ./configure --with-md5-passwords --with-pam --with-selinux --with-privsep-path=/var/lib/sshd/ --sysconfdir=/etc/ssh",
    "cd openssh-9.9p1 && make",
    "cd openssh-9.9p1 && sudo make install"
]

def run_command(command):
    """Executes a shell command with optional directory change"""
    try:
        with open(log_file, "a") as log:
            subprocess.run(command, shell=True, check=True,stdout=log, stderr=log)
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {command}\n{e}")


for cmd in commands:
    run_command(cmd)

print("OpenSSH upgrade completed!")

