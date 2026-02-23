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

When you run `ssh-py-manager`, you'll be presented with a menu-driven interface offering four main options:

### 1. Select a SSH Key to work with (selected by default)
- Lists all SSH keys found in your `~/.ssh` folder (detects `.pub` files)
- Select a key to activate it in your SSH agent
- Clears any existing keys from ssh-agent and adds your selected key
- Perfect for switching between different SSH keys for different repositories

### 2. Add a new SSH Key  
- Prompts for key details:
  - **Key name**: Alphanumeric name for your key (e.g., `github_work_key`)
  - **Email**: Associated email address for the key
  - **Algorithm**: Choose from rsa, dsa, ecdsa, or ed25519 (ed25519 recommended)
  - **Passphrase**: Enter twice for confirmation
- Generates the SSH key pair using `ssh-keygen`
- Automatically adds the new key to ssh-agent
- Displays the public key content so you can copy it to your Git provider

### 3. Remove a SSH Key
- Shows list of existing SSH keys
- Requires confirmation before deletion
- Removes the key from ssh-agent and deletes both private and public key files
- **Warning**: This permanently deletes the key files

### 4. Exit
- Safely exits the program

The interface uses interactive prompts with validation to ensure all inputs are correct before proceeding with any operations.

## Dependencies

```
prompt-toolkit==3.0.36
questionary==2.0.1
wcwidth==0.2.13
```