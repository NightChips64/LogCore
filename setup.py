import setuptools

with open("README.md","r") as file:
    long_description=file.read()

setuptools.setup(
    name="logcore-nightchips",
    version="0.0.1",
    author="NightChips",
    description="Advanced logging package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)