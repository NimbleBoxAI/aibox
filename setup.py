import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nbox",
    version="0.1.10",
    author="NimbleBox.ai",
    author_email="admin@nimblebox.ai",
    description="Make inference chill again!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NimbleBoxAI/nbox",
    project_urls={
        "Bug Tracker": "https://github.com/NimbleBoxAI/nbox/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD 3-Clause",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "nbox"},
    packages=setuptools.find_packages(where="nbox"),
    python_requires=">=3.6",
)
