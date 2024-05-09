from .Questions.Questions_Class import Questions
from .Ssh.Auth import SshAuth


def main():

    ask = Questions().ask()

    SshAuth(ssh_directory=ask["ssh_directory"], key=ask["key"], delete=ask["delete"])


if __name__ == "__main__":
    main()
