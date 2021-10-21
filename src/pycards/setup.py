from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas>=1.3.0", "Pillow>=8.3.1"]

setup(
    name="pycards",
    version="0.0.1",
    author="Jussi Kujala",
    author_email="jussi.kujala@iki.fi",
    description="A package to help create card games.",
    long_description=readme,
    long_description_content_type="text/markdown",
    #url="https://github.com/jukujala/tgc-utils",
    #package_dir={"": "src"},
    #packages=find_packages(where="src"),
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
    ],
)
