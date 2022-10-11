# Importing all required modules
import os
import sys
from time import sleep
from tkinter import *
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class WorkSpace:
    def __init__(self):

        # Base app with instance variables
        self.root = Tk()
        self.Var1 = IntVar()

        # App title
        self.root.title("WorkSpace Automater")

        # Set the window to unmaximisable
        self.root.resizable(False, False)

        # App dimensiosn and screen dimesnions
        self.app_width, self.app_height = 455, 380
        self.screen_width, self.screen_height = self.root.winfo_screenwidth(
        ), self.root.winfo_screenheight()

        # Set app geometry
        self.root.geometry(
            f"{self.app_width}x{self.app_height}+{(self.screen_width-self.app_width)//2}+{(self.screen_height-self.app_height)//2}")

        # Set app heading
        self.heading = Label(self.root, text="WorkSpace Automater")
        self.heading.config(font=("Segoe UI", 24))
        self.heading.pack()

        # Set app username label
        self.usernameLabel = Label(
            self.root, text="Github Username", font=("Courier", 10, "bold"))
        self.username = Entry(self.root, width=40)
        self.usernameLabel.place(x=30, y=67)
        self.username.place(x=160, y=70)

        # Set app password label
        self.passwordLabel = Label(
            self.root, text="Github Password", font=("Courier", 10, "bold"))
        self.password = Entry(self.root, width=40, show='*')
        self.passwordLabel.place(x=30, y=107)
        self.password.place(x=160, y=110)

        # Set app repository label
        self.repoLabel = Label(
            self.root, text="Repository Name", font=("Courier", 10, "bold"))
        self.repo = Entry(self.root, width=40)
        self.repoLabel.place(x=30, y=147)
        self.repo.place(x=160, y=150)

        # Set decsription label
        self.descriptionLabel = Label(
            self.root, text="Description", font=("Courier", 10, "bold"))
        self.description = Entry(self.root, width=40)
        self.descriptionLabel.place(x=30, y=187)
        self.description.place(x=160, y=190)

        # Set app path label
        self.pathLabel = Label(
            self.root, text="Folder Path", font=("Courier", 10, "bold"))
        self.path = Entry(self.root, width=35)
        self.pathLabel.place(x=30, y=227)
        self.path.place(x=130, y=230)

        # set destination folder button
        self.folderSelect = Button(
            self.root, text="Choose Folder", command=self.select)
        self.folderSelect.place(x=350, y=227)

        # Selectthe public / private option
        self.visibilityLabel = Label(
            self.root, text="Visibility", font=("Courier", 10, "bold"))
        self.RBttn = Radiobutton(self.root, text="Public", variable=self.Var1,
                                 value=1)
        self.RBttn.place(x=140, y=267)
        self.RBttn1 = Radiobutton(self.root, text="Private", variable=self.Var1,
                                  value=2)
        self.RBttn1.place(x=220, y=267)
        self.visibilityLabel.place(x=30, y=267)

        # Create enter button
        self.button = Button(self.root, text="Enter", command=self.Automate)
        self.button.place(x=self.app_width//2-20, y=305)

        # Set app copyright label
        self.copyright = Label(self.root, text="Copyright-2022 by Hardik Jaiswal",
                               font=("Times New Roman", 10, "italic"), relief=SUNKEN)
        self.copyright.place(x=130, y=345)

    def Automate(self):

        # Get values from all text inputs
        self.usrname = self.username.get()
        self.passw = self.password.get()
        self.repoName = self.repo.get()
        self.descriptionName = self.description.get()
        self.folderpath = self.path.get()

        # Initailse the default web-driver
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(
            chrome_options=options, executable_path=r'chromedriver.exe')

        # Set driver and go to github.com
        self.driver.get("https://www.github.com")

        # Click login
        loginElem = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/header/div/div[2]/div/div/div[2]/a')
        loginElem.click()

        # Delay the program for 4 seconds
        sleep(4)

        # Enter username
        usernameElem = self.driver.find_element(By.XPATH,
                                                '/html/body/div[3]/main/div/div[4]/form/input[2]')
        usernameElem.send_keys(self.usrname)

        # Enter password
        passwordElem = self.driver.find_element(
            By.XPATH, '/html/body/div[3]/main/div/div[4]/form/div/input[1]')
        passwordElem.send_keys(self.passw)

        # Click login again
        loginButton = self.driver.find_element(By.XPATH,
                                               '/html/body/div[3]/main/div/div[4]/form/div/input[11]')
        loginButton.click()

        # Wait for 6 sec
        self.driver.implicitly_wait(6)

        # Click on new repository
        newButton = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, '/html/body/div[5]/div/aside/div/loading-context/div/div[1]/div/h2/a')))
        newButton.click()

        # Enter the repository name
        repositoryName = self.driver.find_element(
            By.XPATH, '/html/body/div[5]/main/div/form/div[2]/auto-check/dl/dd/input')
        repositoryName.send_keys(self.repoName)

        # Enter the repository descriptory
        descName = self.driver.find_element(
            By.XPATH, '/html/body/div[5]/main/div/form/div[5]/dl/dd/input')
        descName.send_keys(self.descriptionName)

        # Click the public/private radio option
        buttonCode = self.getOption()
        if(buttonCode == 1):
            self.driver.find_element(
                By.XPATH, '/html/body/div[5]/main/div/form/div[5]/div[1]/label/input').click()
        else:
            self.driver.find_element(
                By.XPATH, '/html/body/div[5]/main/div/form/div[5]/div[2]/label/input').click()

        # Wait for 6 sec again
        self.driver.implicitly_wait(6)

        # Click on enabled create button
        createButton = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, '/html/body/div[5]/main/div/form/div[5]/button')))
        createButton.click()

        # wait for 10 seconds again
        self.driver.implicitly_wait(10)

        # Copy the remote file origin url
        copyButton = self.driver.find_element(
            By.XPATH, '/html/body/div[5]/div/main/turbo-frame/div/div/git-clone-help/div[1]/div/div[4]/div/span/span/clipboard-copy')
        copyButton.click()

        # Get the remote origin file url
        self.remoteFile = self.root.clipboard_get()

        # Push the code to github, create files and folders
        os.mkdir(f"{self.folderpath}/{self.repoName}")
        os.chdir(f"{self.folderpath}/{self.repoName}")
        os.system(f'echo # _{self.repoName}_ >> README.md')
        os.system("git init")
        os.system('git add README.md')
        os.system('git commit -m "first commit"')
        os.system('git branch -M main')
        os.system(f'git remote add origin {self.remoteFile}')
        os.system('git push -u origin main')
        os.system('touch .gitignore')
        os.mkdir('tests')
        os.mkdir('src')
        os.chdir('src')
        os.mkdir('model')
        os.mkdir('view')
        os.mkdir('controller')
        os.system('git add .')
        os.system('git commit -m "added directories"')
        os.system('git push')
        os.chdir(f"{self.folderpath}/{self.repoName}")
        os.system('virtualenv env')

        # Refresh the repository
        refreshButton = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, '/html/body/div[5]/div/main/div/div[1]/div/div/strong/a')))
        refreshButton.click()

        # Open VS Code
        os.system('code .')

        # Exit program
        sys.exit()

    def select(self):

        # Ask for directory
        folder_path = filedialog.askdirectory()
        self.path.delete(0, END)
        self.path.insert(0, folder_path)

    def getOption(self):

        # Get the radio button which is checked
        return self.Var1.get()

    def run(self):

        # run the app
        self.root.mainloop()


if __name__ == '__main__':

    # Run the app finally
    WorkSpace().run()
