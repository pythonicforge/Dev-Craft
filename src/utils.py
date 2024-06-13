# has all the helper functions to help automate the process


import subprocess


class Utility:
    def __init__(self) -> None:
        pass

    def is_vscode_installed(self):
        try:
            subprocess.run(["code", "--version"], check=True)
            return True
        except Exception as e:
            return False

    def install_vscode(self):
        distribution = distro.name().lower()
        if distribution == 'ubuntu':
            subprocess.run(["wget", "-qO-", "https://packages.microsoft.com/keys/microsoft.asc", "|", "gpg", "--dearmor", "|", "sudo", "tee", "/etc/apt/trusted.gpg.d/microsoft.asc.gpg"], shell=True)
            subprocess.run(["sudo", "sh", "-c", "\"echo 'deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main' > /etc/apt/sources.list.d/vscode.list\""], shell=True)
            subprocess.run(["sudo", "apt-get", "install", "apt-transport-https"], shell=True)
            subprocess.run(["sudo", "apt-get", "update"], shell=True)
            subprocess.run(["sudo", "apt-get", "install", "code", "-y"], shell=True)
        elif distribution == 'fedora':
            subprocess.run(["sudo", "rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc"], shell=True)
            subprocess.run(["sudo", "sh", "-c", "\"echo -e '[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc' > /etc/yum.repos.d/vscode.repo\""], shell=True)
            subprocess.run(["sudo", "dnf", "check-update"], shell=True)
            subprocess.run(["sudo", "dnf", "install", "code", "-y"], shell=True)
        elif distribution == 'arch':
            subprocess.run(["sudo", "pacman", "-Syu", "--noconfirm"], shell=True)
            subprocess.run(["sudo", "pacman", "-S", "code", "--noconfirm"], shell=True)
        elif distribution == 'opensuse':
            subprocess.run(["sudo", "rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc"], shell=True)
            subprocess.run(["sudo", "sh", "-c", "\"zypper ar -f https://packages.microsoft.com/yumrepos/vscode vscode\""], shell=True)
            subprocess.run(["sudo", "zypper", "ref"], shell=True)
            subprocess.run(["sudo", "zypper", "install", "code", "-y"], shell=True)
        else:
            raise NotImplementedError(f"Installation for {distribution} is not supported.")
        print("Visual Studio Code is installed successfully")

    def is_git_installled():
        try:
            subprocess.run(["git", "--version"], check=True)
            return True
        except Exception as e:
            return False

    def install_git(self):
        distribution = distro.name().lower()
        if distribution == 'ubuntu' or distribution == 'debian':
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "git", "-y"], check=True)
        elif distribution == 'fedora':
            subprocess.run(["sudo", "dnf", "install", "git", "-y"], check=True)
        elif distribution == 'arch':
            subprocess.run(["sudo", "pacman", "-Syu", "--noconfirm"], check=True)
            subprocess.run(["sudo", "pacman", "-S", "git", "--noconfirm"], check=True)
        elif distribution == 'opensuse':
            subprocess.run(["sudo", "zypper", "refresh"], check=True)
            subprocess.run(["sudo", "zypper", "install", "git", "-y"], check=True)
        else:
            raise NotImplementedError(f"Installation for {distribution} is not supported.")
        print("Git is installed successfully")

    def generateTemplate(self):
        pass

    def generateDocumentation(self):
        pass

    def github_init(self):
        pass