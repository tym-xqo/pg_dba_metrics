from setuptools import setup, find_packages


setup(
    name="dba_metrics",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["nri_metrics"],
    description="Script to run check queries on postgres",
    author="Thomas Yager-Madden",
    author_email="tym@benchprep.com",
    install_requires=[
        "inflection",
        "psycopg2-binary",
        "pyyaml",
        "sqla-raw==1.0.0rc1",
    ],
    entry_points={
        "console_scripts": [
            "nri = nri_metrics:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
