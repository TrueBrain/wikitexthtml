import setuptools
import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wikitexthtml",
    version=version.get_version(),
    author="Patric 'TrueBrain' Stout",
    author_email="truebrain@truebrain.nl",
    description="Convert wikitext to HTML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TrueBrain/wikitexthtml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "python-slugify",
        "ply",
        "wikitextparser",
    ],
)
