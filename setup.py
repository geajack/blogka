import setuptools
from shutil import rmtree

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="blogka",
    version="1.0.0",
    description="Minimalist blogging platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geajack/charlotte",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
    ],
    python_requires='>=3.6',
    install_requires = [
        "Flask==1.0.2",
        "Markdown==3.0.1",
        "python-markdown-math"
    ]
)