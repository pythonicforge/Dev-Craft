import os
import distro
import subprocess
from hugchat import hugchat
from hugchat.login import Login
import requests
import shlex
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class Utility:
    def __init__(self) -> None:
        """
        Initializes the Utility class.

        Parameters:
        None

        Returns:
        None
        """
        pass

    def is_vscode_installed(self):
        """
        Checks if Visual Studio Code is installed on the system.

        Parameters:
        None

        Returns:
        bool: True if Visual Studio Code is installed, False otherwise
        """
        return self.is_installed("code", "--version")

    def install_vscode(self):
        """
        Installs Visual Studio Code on the system based on the detected operating system.

        Parameters:
        None

        Returns:
        None
        """
        distribution = distro.name().lower()
        if distribution == 'ubuntu':
            # Download Microsoft GPG key with curl and save to a temporary file
            self.run_command("curl -fsSL https://packages.microsoft.com/keys/microsoft.asc > microsoft.asc")
            
            # Import GPG key from the temporary file and save to trusted GPG keys
            self.run_commands([
                "sudo gpg --dearmor microsoft.asc",
                "sudo mv microsoft.asc.gpg /etc/apt/trusted.gpg.d/microsoft.asc.gpg",
                "rm microsoft.asc",  # Clean up the temporary file
                "echo 'deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main' | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null",
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
        """
        Checks if Git is installed on the system.

        Parameters:
        None

        Returns:
        bool: True if Git is installed, False otherwise
        """
        return self.is_installed("git", "--version")

    def install_git(self):
        """
        Installs Git on the system based on the detected operating system.

        Parameters:
        None

        Returns:
        None
        """
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
        """
        Checks if Python and pip are installed on the system.

        Parameters:
        None

        Returns:
        bool: True if Python and pip are installed, False otherwise
        """
        return self.is_installed("python3", "--version") and self.is_installed("pip3", "--version")

    def install_python(self):
        """
        Installs Python and pip on the system based on the detected operating system.

        Parameters:
        None

        Returns:
        None
        """
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

    def create_python_env(self, project_name):
        """
        Creates a Python virtual environment inside the specified project directory.

        Parameters:
        project_name (str): The name of the project directory

        Returns:
        None
        """
        env_path = os.path.join(project_name)

        # Now create the virtual environment inside the 'env' directory
        self.run_command(
            f"""
            pip install virtualenv
            cd {env_path}
            virtualenv env
            """
        )
        logging.info("Python virtual environment created successfully")

    def get_github_token(self):
        """
        Retrieves the GitHub token from the environment variables.

        Parameters:
        None

        Returns:
        str: The GitHub token
        """
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")
        return token

    def create_github_repo(self, repo_name, description, private):
        """
        Creates a new GitHub repository using the provided repository name, description, and privacy setting.

        Parameters:
        repo_name (str): The name of the repository
        description (str): The description of the repository
        private (bool): True if the repository should be private, False otherwise

        Returns:
        str: The clone URL of the newly created repository
        """
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
            return response.json()['clone_url']
        else:
            raise Exception(f"Failed to create repository: {response.status_code} {response.text}")

    def generate_readme(self, project_name, title, template, description):
        """
        Generates a README file for the project using the provided information and a chatbot.

        Parameters:
        project_name (str): The name of the project directory
        title (str): The title of the project
        template (str): The template type of the project
        description (str): The description of the project

        Returns:
        str: The generated README content
        """
        try:
            # Ensure cookies directory is created inside the project directory
            cookie_path_dir = os.path.join(project_name, "cookies")
            os.makedirs(cookie_path_dir, exist_ok=True)

            # Use the correct path when calling Login from hugchat
            sign = Login(os.getenv('EMAIL_ADDRESS'), os.getenv('PASSWORD'))
            cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
            prompt = (f"Generate a comprehensive README file for a project named {title} which is a {template} type project with the following description:\n\n"
                      f"{description}\n\n"
                      f"The README should include sections like Project Title, Description, Installation, Usage, Contributing, License, and Contact Information.")
            
            return chatbot.chat(prompt)
        except Exception as e:
            logging.error(f"Error generating README: {e}")
            return ""

    def create_project_folder(self, project_name):
        """
        Creates a new project folder with the specified name.

        Parameters:
        project_name (str): The name of the project folder

        Returns:
        None
        """
        os.makedirs(project_name, exist_ok=True)
        logging.info(f"Project folder '{project_name}' created successfully")

    def create_subfolders(self, project_path, template):
        """
        Creates subfolders for the project based on the specified template.

        Parameters:
        project_path (str): The path of the project folder
        template (str): The template type of the project

        Returns:
        None
        """
        subfolders = ["src", "tests", "docs"]  # Example subfolders, can be adjusted based on template
        for folder in subfolders:
            os.makedirs(os.path.join(project_path, folder), exist_ok=True)
        logging.info(f"Subfolders for template '{template}' created successfully")

    def initialize_git_repo(self, project_path, clone_url):
        """
        Initializes a new Git repository in the project folder and pushes it to GitHub.

        Parameters:
        project_path (str): The path of the project folder
        clone_url (str): The clone URL of the GitHub repository

        Returns:
        None
        """
        token = self.get_github_token()
        clone_url_with_token = clone_url.replace('https://', f'https://{token}@')
	# os.system(f"cd {os.path.abspath(project_path)}")
        commands = [
            ["git", "init"],
            ["git", "remote", "add", "origin", clone_url_with_token],
            ["git", "add", "."],
            ["git", "commit", "-m", "Initial commit"],
            ["git", "push", "-u", "origin", "master"]
        ]

        for command in commands:
            subprocess.run(command, cwd=os.path.abspath(project_path), check=True)
        logging.info("Git repository initialized and pushed to GitHub successfully")

    def install_base_packages(self, project_path, template):
        """
        Installs base packages for the project based on the specified template.

        Parameters:
        project_path (str): The path of the project folder
        template (str): The template type of the project

        Returns:
        None
        """
        requirements = {
            "web application": ["flask", "requests"],
            "data science": ["numpy", "pandas", "matplotlib"],
            "machine learning": ["scikit-learn", "tensorflow", "keras"]
        }
        packages = requirements.get(template, [])
        if packages:
            env_path = os.path.join(project_path, "env")  # Assuming env directory is inside project_path
            pip_command = os.path.join(env_path, "bin", "pip")  # Constructing the full path to pip inside the virtual environment

            try:
                logging.info(f"Installing base packages for template '{template}'...")
                subprocess.run([pip_command, "install"] + packages, check=True)
                logging.info(f"Base packages for template '{template}' installed successfully")
            except Exception as e:
                logging.error(f"Error installing base packages: {e}")

    def open_vscode(self, project_name):
        """
        Opens Visual Studio Code in the specified project folder.

        Parameters:
        project_name (str): The name of the project folder

        Returns:
        None
        """
        folder_path = os.path.join(project_name)
        self.run_command(f"code {folder_path}")
        logging.info("VSCode opened in project directory successfully")


    def is_installed(self, command, version_arg):
        """
        Checks if a command-line tool is installed on the system.

        Parameters:
        command (str): The command to check for installation
        version_arg (str): The argument to check the version of the command

        Returns:
        bool: True if the command is installed, False otherwise
        """
        try:
            subprocess.run([command, version_arg], check=True)
            return True
        except Exception:
            return False

    def run_commands(self, commands):
        """
        Runs a list of command-line commands.

        Parameters:
        commands (list): A list of command-line commands to run

        Returns:
        None
        """
        for command in commands:
            subprocess.run(shlex.split(command), check=True)

    def run_command(self, command):
        """
        Runs a single command-line command.

        Parameters:
        command (str): The command-line command to run

        Returns:
        None
        """
        subprocess.run(command, shell=True, check=True)

def create_file(filepath, content):
    """
    Creates a new file with the specified filepath and writes the given content to it.

    Parameters:
    filepath (str): The path of the file to be created.
    content (str): The content to be written into the file.

    Returns:
    None

    Raises:
    IOError: If there is an error while opening or writing to the file.

    Example:
    >>> create_file('example.txt', 'Hello, World!')
    """
    try:
        with open(filepath, 'w') as file:
            file.write(str(content))
    except IOError as e:
        print(f"An error occurred while creating the file: {e}")

# hello
# hiii

