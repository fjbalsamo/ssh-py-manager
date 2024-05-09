import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = "0.0.1"
PACKAGE_NAME = "ssh_py_manager"
AUTHOR = "Franco Balsamo"
AUTHOR_EMAIL = "fjbalsamo@gmail.com"
URL = "https://github.com/fjbalsamo"

LICENSE = "MIT"
DESCRIPTION = "SSH git manager"
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding="utf-8")
LONG_DESC_TYPE = "text/markdown"

with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

INSTALL_REQUIRES = required_packages

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ssh-py-manager=ssh_py_manager.main:main",
        ],
    },
)
