# SSH Py Manager

This library manages SSH keys that git uses for authentication with repositories

## Install

```bash
pip install ssh-py-manager
```

## Use Guide

```bash
ssh-py-manager
```

## Workflow

lists the different keys saved in the `~/.ssh` folder. Simply select one, press enter, set your password and that's it.

## Dependencies

```
prompt-toolkit==3.0.36
questionary==2.0.1
wcwidth==0.2.13
```