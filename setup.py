from setuptools import find_packages

from distutils.core import setup


setup(
    name='acr-protein-viewer',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],
    license="BSD",
    platforms=["Linux", "Mac OS-X", "Unix"],
    install_requires=[],
    packages=find_packages(),
)
