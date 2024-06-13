import os
import distro
import subprocess
import requests
import shlex
import logging
from dotenv import load_dotenv
from hugchat import hugchat
from hugchat.login import Login

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Utility:
    def __init__(self):
        pass

    def is_vscode_installed(self):
        return self.is_installed("code", "--version")

    def install_vscode(self):
        distribution = distro.name().lower()
        if distribution == 'ubuntu':
            self.run_commands([
                "wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc.gpg",
                "sudo sh -c \"echo 'deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main' > /etc/apt/sources.list.d/vscode.list\"",
                "sudo apt-get install apt-transport-https -y",
                "sudo apt-get update",
                "sudo apt-get install code -y"
            ])
        elif distribution == 'fedora':
            self.run_commands([
                "sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc",
                "sudo sh -c \"echo -e '[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc' > /etc/yum.repos.d/vscode.repo\"",
                "sudo dnf check-update",
                "sudo dnf install code -y"
            ])
        elif distribution == 'arch':
            self.run_commands([
                "sudo pacman -Syu --noconfirm",
                "sudo pacman -S code --noconfirm"
            ])
        elif distribution == 'opensuse':
            self.run_commands([
                "sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc",
                "sudo sh -c \"zypper ar -f https://packages.microsoft.com/yumrepos/vscode vscode\"",
                "sudo zypper ref",
                "sudo zypper install code -y"
            ])
        else:
            raise NotImplementedError(f"Installation for {distribution} is not supported.")
        logging.info("Visual Studio Code is installed successfully")

    def is_git_installed(self):
        return self.is_installed("git", "--version")

    def install_git(self):
        distribution = distro.name().lower()
        if distribution in ['ubuntu', 'debian']:
            self.run_commands([
                "sudo apt-get update",
                "sudo apt-get install git -y"
            ])
        elif distribution == 'fedora':
            self.run_commands([
                "sudo dnf install git -y"
            ])
        elif distribution == 'arch':
            self.run_commands([
                "sudo pacman -Syu --noconfirm",
                "sudo pacman -S git --noconfirm"
            ])
        elif distribution == 'opensuse':
            self.run_commands([
                "sudo zypper refresh",
                "sudo zypper install git -y"
            ])
        else:
            raise NotImplementedError(f"Installation for {distribution} is not supported.")
        logging.info("Git is installed successfully")

    def is_python_installed(self):
        return self.is_installed("python3", "--version") and self.is_installed("pip3", "--version")

    def install_python(self):
        distribution = distro.name().lower()
        if distribution in ['ubuntu', 'debian']:
            self.run_commands([
                "sudo apt-get update",
                "sudo apt-get install python3 python3-pip -y"
            ])
        elif distribution == 'fedora':
            self.run_commands([
                "sudo dnf install python3 python3-pip -y"
            ])
        elif distribution == 'arch':
            self.run_commands([
                "sudo pacman -Syu --noconfirm",
                "sudo pacman -S python python-pip --noconfirm"
            ])
        elif distribution == 'opensuse':
            self.run_commands([
                "sudo zypper refresh",
                "sudo zypper install python3 python3-pip -y"
            ])
        else:
            raise NotImplementedError(f"Installation for {distribution} is not supported.")
        logging.info("Python and pip are installed successfully")

    def create_python_env(self):
        self.run_commands([
            "python3 -m pip install --user virtualenv",
            "python3 -m virtualenv env"
        ])
        logging.info("Python virtual environment created successfully")

    def get_github_token(self):
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")
        return token

    def create_github_repo(self, repo_name, description, private):
        token = self.get_github_token()
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        data = {
            'name': repo_name,
            'description': description,
            'private': private
        }
        response = requests.post('https://api.github.com/user/repos', headers=headers, json=data)
        if response.status_code == 201:
            logging.info(f"Repository '{repo_name}' created successfully.")
            return response.json().clone_url
        else:
            raise Exception(f"Failed to create repository: {response.status_code} {response.text}")

    def generate_readme(self, title, template, description):
        try:
            # Login to Hugging Face chatbot and generate README
            EMAIL = os.getenv("EMAIL_ADDRESS")
            PASSWD = os.getenv("PASSWORD")
            cookie_path_dir = "./cookies/"
            sign = Login(EMAIL, PASSWD)
            cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"
            prompt = (
                f"Generate a comprehensive README file for a project named {title} which is a {template} type project with the following description:\n\n"
                f"{description}\n\n"
                f"The README should include sections like Project Title, Description, Installation, Usage, Contributing, License, and Contact Information."
            )
            
            return chatbot.chat(prompt)
        except Exception as e:
            logging.error(f"Error generating README: {e}")
            return None

    def is_installed(self, command, version_arg):
        try:
            subprocess.run([command, version_arg], check=True)
            return True
        except Exception:
            return False

    def run_commands(self, commands):
        for command in commands:
            subprocess.run(shlex.split(command), check=True)

def create_file(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)

