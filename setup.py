from setuptools import setup
long_description = ""

with open("README.md", "r", encoding="utf8") as f: long_description = f.read()

setup(
    name="Console UI",
    version="0.0.1",
    description = "A library for creating console user interfaces.",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires = [
        "git+https://github.com/neverUsedGithub/Boxpy.git>=0.0.1",
        "getkey>=0.6.5"
    ],
)