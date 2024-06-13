import argparse
import logging
from utils import Utility, create_file

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_software_installed(utility):
    # Ensure VSCode is installed
    if not utility.is_vscode_installed():
        logging.info("Installing VSCode...")
        utility.install_vscode()
    else:
        logging.info("VSCode is already installed.")

    # Ensure Git is installed
    if not utility.is_git_installed():
        logging.info("Installing Git...")
        utility.install_git()
    else:
        logging.info("Git is already installed.")

    # Ensure Python is installed
    if not utility.is_python_installed():
        logging.info("Installing Python...")
        utility.install_python()
    else:
        logging.info("Python is already installed.")

def main():
    parser = argparse.ArgumentParser(description="Dev-Craft CLI tool")

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # GitHub repository management
    repo_parser = subparsers.add_parser('create_repo', help='Create a GitHub repository')
    repo_parser.add_argument('repo_name', type=str, help='Name of the repository')
    repo_parser.add_argument('description', type=str, help='Description of the repository')
    repo_parser.add_argument('--private', action='store_true', help='Create a private repository')

    # README generation
    readme_parser = subparsers.add_parser('generate_readme', help='Generate a README file')
    readme_parser.add_argument('title', type=str, help='Project title')
    readme_parser.add_argument('template', type=str, help='Project template type')
    readme_parser.add_argument('description', type=str, help='Project description')

    args = parser.parse_args()
    utility = Utility()

    # Ensure necessary software is installed
    ensure_software_installed(utility)

    if args.command == 'create_repo':
        logging.info(f"Creating GitHub repository '{args.repo_name}'...")
        clone_url = utility.create_github_repo(args.repo_name, args.description, args.private)
        logging.info(f"Repository created. Clone URL: {clone_url}")

    elif args.command == 'generate_readme':
        logging.info("Generating README file...")
        readme_content = utility.generate_readme(args.title, args.template, args.description)
        create_file('README.md', readme_content)
        logging.info("README.md file generated successfully.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
