from os import path

import setuptools

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="side-kick",
    version="0.2.0",
    author="Natoora Technology",
    author_email="technology@natoora.com",
    description="Cron-based task runner for django with easy admin controls",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Natoora/sidekick",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
