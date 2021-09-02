from setuptools import setup, find_packages

setup(
    name='clean_folder',
    vesion='1',
    description='Script help you working with contacts, notes and help you sort files in folder',
    packages=find_packages(),
    install_requires=['fuzzywuzzy'],
    entry_points={'console_scripts': ['smartbot = smartbot.app:main']}
)