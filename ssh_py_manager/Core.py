from enum import Enum
import os
import re
from typing import List
import questionary
from subprocess import run


class Choice(Enum):
    SELECT_KEY = "Select a SSH Key to work with"
    ADD_KEY = "Add a new SSH Key"
    REMOVE_KEY = "Remove a SSH Key"
    EXIT = "Exit"


class Core:
    algorithm_choices: List[str] = ["rsa", "dsa", "ecdsa", "ed25519"]
    add_questions = []

    def __init__(self) -> None:
        self.ssh_directory: str = os.path.join(os.path.expanduser("~"), ".ssh")
        self.keys: List[str] = []
        self.__load_keys()

    def ask(self):
        todo = questionary.select(
            message="What do you want to do?",
            choices=[
                Choice.SELECT_KEY.value,
                Choice.ADD_KEY.value,
                Choice.REMOVE_KEY.value,
                Choice.EXIT.value,
            ],
            default=Choice.SELECT_KEY.value,
        ).ask()

        if todo == Choice.EXIT.value:
            print("Exiting...")
            return
        if todo == Choice.SELECT_KEY.value:
            self.__select_a_key()
            return
        if todo == Choice.ADD_KEY.value:
            self.__add_new_key()
            return
        if todo == Choice.REMOVE_KEY.value:
            self.__remove_a_key()
            return
        print("Invalid choice. Exiting...")
        return

    def __check_directory(self):
        if not os.path.exists(self.ssh_directory):
            return False
        if not os.path.isdir(self.ssh_directory):
            return False
        return True

    def __check_file(self, key: str):
        key_path = os.path.join(self.ssh_directory, key)
        if not os.path.exists(key_path):
            return False
        if not os.path.isfile(key_path):
            return False
        return True

    def __load_keys(self):
        self.keys = []
        if not self.__check_directory():
            print(f"SSH directory '{self.ssh_directory}' does not exist. Exiting...")
            return

        files_in_ssh_directory = os.listdir(self.ssh_directory)
        for file in files_in_ssh_directory:
            if file.endswith(".pub"):
                key = file.replace(".pub", "")
                self.keys.append(key)

    def __select_a_key(self):
        key = questionary.select(
            message="Select a SSH Key",
            choices=self.keys,
        ).ask()

        if type(key) is not str:
            print("No key selected. Exiting...")
            return
        if not self.__check_file(key):
            print("Selected key does not exist. Exiting...")
            return
        ssh_key_path = os.path.join(self.ssh_directory, key)
        run(["ssh-add", "-D"])
        run(["ssh-add", ssh_key_path])

    def __add_new_key(self):
        key_pattern = r"^[a-zA-Z0-9_\-]+$"
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        questions = [
            {
                "type": "input",
                "name": "key_name",
                "message": "Enter a name for the new SSH Key (my_new_key_for_github):",
                "validate": lambda text: (
                    True
                    if (
                        isinstance(text, str)
                        and len(text.strip()) > 0
                        and re.match(key_pattern, text)
                    )
                    else "Error: Key name must be a non-empty string containing only letters, numbers, underscores, or hyphens."
                ),
            },
            {
                "type": "input",
                "name": "email",
                "message": "Enter an email for the new SSH Key (my.email@example.com):",
                "validate": lambda text: (
                    True
                    if (
                        isinstance(text, str)
                        and len(text.strip()) > 0
                        and re.match(email_pattern, text)
                    )
                    else "Error: Invalid email format."
                ),
            },
            {
                "type": "select",
                "name": "algorithm",
                "message": "Select the algorithm for the new SSH Key (e.g., ed25519):",
                "choices": self.algorithm_choices,
                "default": "ed25519",
            },
            {
                "type": "input",
                "name": "passphrase",
                "message": "Enter a passphrase for the new SSH Key:",
                "validate": lambda text: type(text) is str
                and len(text.strip()) > 0
                or "Error: Passphrase cannot be empty.",
            },
            {
                "type": "input",
                "name": "repeat_passphrase",
                "message": "Repeat the passphrase for the new SSH Key:",
                "validate": lambda text: type(text) is str
                and len(text.strip()) > 0
                or "Error: Repeat passphrase cannot be empty.",
            },
        ]
        data = questionary.prompt(questions=questions)
        key_name = data.get("key_name")
        email = data.get("email")
        algorithm = data.get("algorithm")
        passphrase = data.get("passphrase")
        repeat_passphrase = data.get("repeat_passphrase")

        if type(key_name) is not str or len(key_name.strip()) == 0:
            print("Invalid key name. Exiting...")
            return
        if not re.match(key_pattern, key_name):
            print("Invalid key name. Exiting...")
            return

        if type(email) is not str or len(email.strip()) == 0:
            print("Invalid email. Exiting...")
            return
        if not re.match(email_pattern, email):
            print("Invalid email. Exiting...")
            return

        if type(algorithm) is not str or len(algorithm.strip()) == 0:
            print("Invalid algorithm. Exiting...")
            return
        if algorithm not in self.algorithm_choices:
            print("Invalid algorithm. Exiting...")
            return

        if type(passphrase) is not str or len(passphrase.strip()) == 0:
            print("Invalid passphrase. Exiting...")
            return
        if type(repeat_passphrase) is not str or len(repeat_passphrase.strip()) == 0:
            print("Invalid repeat passphrase. Exiting...")
            return

        if passphrase != repeat_passphrase:
            print("Passphrases do not match. Exiting...")
            return
        ssh_key_path = os.path.join(self.ssh_directory, key_name)
        if self.__check_file(key_name):
            print(f"A key with the name '{key_name}' already exists. Exiting...")
            return
        run(
            [
                "ssh-keygen",
                "-t",
                algorithm,
                "-C",
                email,
                "-f",
                ssh_key_path,
                "-N",
                passphrase,
            ]
        )
        run(["ssh-add", "-D"])
        run(["ssh-add", ssh_key_path])
        print(
            f"SSH Key '{key_name}' added successfully. Copy the public key to your clipboard:\n"
        )
        run(["cat", ssh_key_path + ".pub"])

    def __remove_a_key(self):
        questions = [
            {
                "type": "select",
                "name": "key",
                "message": "Select a SSH Key to remove",
                "choices": self.keys,
            },
            {
                "type": "confirm",
                "name": "confirm",
                "message": "Are you sure you want to remove this SSH Key?",
                "default": False,
            },
        ]
        data = questionary.prompt(questions=questions)
        key = data.get("key")
        confirm = data.get("confirm", False)

        if not confirm:
            print("Operation cancelled. Exiting...")
            return
        if type(key) is not str:
            print("No key selected. Exiting...")
            return
        if not self.__check_file(key):
            print("Selected key does not exist. Exiting...")
            return
        ssh_key_path = os.path.join(self.ssh_directory, key)
        run(["ssh-add", "-d", ssh_key_path])
        run(["rm", ssh_key_path])
        run(["rm", ssh_key_path + ".pub"])
        print(f"SSH Key '{key}' removed successfully.")
