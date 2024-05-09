from os import path
from subprocess import run

class SshAuth:
    def __init__(self, ssh_directory:str, key:str, delete:bool) -> None:
        ssh_key_path = path.join(ssh_directory, key)
        if delete:
            run(["ssh-add", "-D"])
        run(["ssh-add", ssh_key_path])
        