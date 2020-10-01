from setuptools import setup, find_packages


setup(
    name="dba_metrics",
    version="0.0.1a",
    packages=find_packages(),
    description="Script to run check queries on postgres",
    author="Thomas Yager-Madden",
    author_email="tym@benchprep.com",
    install_requires=[
        "apscheduler",
        "inflection",
        "nerium",
        "pg8000",
        "records",
        "slackclient",
    ],
    entry_points={"console_scripts": ["dbamtx = dba_metrics.__main__:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
