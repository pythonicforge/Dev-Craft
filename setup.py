from setuptools import setup, find_packages

setup(
    name='dev-craft',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',  # Add any other dependencies here
	'hugchat',
	'distro',
	'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'dev-craft=dev_craft.cli:main',
        ],
    },
)
