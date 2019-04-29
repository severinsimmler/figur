import io
import os
import shutil
import sys
import setuptools


NAME = "figur"
DESCRIPTION = "Figurenerkennung for German literary texts"
URL = "https://github.com/severinsimmler/figur"
AUTHOR = "Severin Simmler"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.6"
REQUIRED = ["flair>=0.4.1",
            "spacy>=2.0.18",
            "pandas>=0.24.1",
            "wget>=3.2",
            "requests>=2.21.0"]


with io.open("README.md", encoding="utf-8") as readme:
    long_description = f"\n{readme.read()}"


class UploadCommand(setuptools.Command):
    description = "Build and publish the package."
    user_options = list()

    @staticmethod
    def status(s):
        print(f"\033[1m{s}\033[0m")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            shutil.rmtree("dist")
        except OSError:
            pass

        self.status("Building source and wheel distribution...")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel")

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags...")
        os.system(f"git tag v{VERSION}")
        os.system("git push --tags")

        sys.exit()


setuptools.setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=REQUIRED,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    cmdclass={
        "upload": UploadCommand,
    },
)
