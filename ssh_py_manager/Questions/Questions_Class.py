from os import path, listdir
from questionary import prompt
from typing import List


class Questions:
    def __init__(self) -> None:
        home_directory = path.expanduser("~")
        ssh_directory = path.join(home_directory, ".ssh")

        self.ssh_directory = ssh_directory

        key_collector: List[str] = []

        if path.exists(ssh_directory) and path.isdir(ssh_directory):
            files_in_ssh_directory = listdir(ssh_directory)
            for file in files_in_ssh_directory:
                if file.endswith(".pub"):
                    key = file.replace(".pub", "")
                    key_collector.append(key)

        self.keys = key_collector

    def ask(self):
        questions = [
            {
                "type": "select",
                "name": "key",
                "message": "Select a SSH Key",
                "choices": self.keys,
            },
            {
                "type": "confirm",
                "name": "delete",
                "message": "Do you want Remove Others identities?",
                "default": False,
            },
        ]
        response = prompt(questions=questions)
        return {**response, "ssh_directory": self.ssh_directory}
