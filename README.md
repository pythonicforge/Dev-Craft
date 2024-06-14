
# _Dev-Craft_

_Dev-Craft is a powerful CLI tool designed to streamline the setup and management of development environments for various types of projects. It ensures that necessary software is installed, creates GitHub repositories, sets up project directories, and generates initial README files using AI._





_Insert gif or link to demo_


### _Features_

- _Automatically installs necessary software (VSCode, Git, Python)_
- _Creates GitHub repositories_
- _Sets up project directories with common subfolders_
- _Generates comprehensive README files using AI_
- _Installs base packages for various project templates_
- _Opens project in VSCode_


### _Installation_

_Prerequisites: Python 3.6+_

1. _**Clone the repository:**_
   ```bash
   git clone https://github.com/yourusername/dev-craft.git
   cd dev-craft
   ```

2. _**Run the install script:**_
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. _**Install dependencies manually (if not using the install script):**_
   ```bash
   pip install .
   ```
### _Usage/Examples_

_After installation, you can use the `dev-craft` command to initialize your projects. The CLI provides various commands to automate the setup process._

```bash
dev-craft create_repo my-new-project "A description of my new project" "web application" --private --env-file /path/to/.env
```

_This command will:_

- _Create a new private GitHub repository named `my-new-project`_
- _Set up a project folder with necessary subfolders_
- _Generate a comprehensive README file_
- _Initialize a Git repository and push the initial commit_
- _Create a Python virtual environment_
- _Install base packages for a web application_
- _Open the project in VSCode_
### _Project Structure_

_After running `dev-craft`, your project directory will look like this:_

```
my-new-project/
├── README.md
├── env/
├── src/
├── tests/
└── docs/
```

### _Run Locally_
_Follow the steps below to run Dev-Craft locally_

1. **_Clone the project_**

```bash
  git clone https://github.com/pythonicforge/Dev-Craft.git
```

2. **_Go to the project directory_**

```bash
  cd Dev-Craft
```

3. **_Install dependencies_**

```bash
  pip install -r reuqirements.txt
```

4. **_Run the App_**

```bash
  python dev_craft/cli.py --help
```


### _Environment Variables_

_Ensure you have a `.env` file in the root of your project or specify its path using the `--env-file` option. The `.env` file should contain the following variables:_

```
GITHUB_TOKEN = <your_github_personal_access_token>
EMAIL_ADDRESS = <your_email_address>
PASSWORD = <your_password>
```


### _Commands_

#### `create_repo`

_Creates a new GitHub repository and sets up the project directory._

_**Arguments:**_
- _`repo_name`: Name of the repository_
- _`description`: Description of the repository_
- _`template`: Project template type (choose from: "web application", "data science", "machine learning")_

**Options:**
- _`--private`: Create a private repository_
- _`--env-file`: Path to the `.env` file (default: `.env`)_
### _Tech Stack_

_**Client:** Python-argparse, Shell scripting_

_**Server:** Python_


### _Contributing_

_We welcome contributions to Dev-Craft! Please follow these steps to contribute:_

1. _Fork the repository_
2. _Create a new branch (`git checkout -b feature-branch`)_
3. _Make your changes_
4. _Commit your changes (`git commit -m 'Add some feature'`)_
5. _Push to the branch (`git push origin feature-branch`)_
6. _Open a pull request_



### License

_This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details._
