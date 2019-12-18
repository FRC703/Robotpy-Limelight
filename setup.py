from distutils.core import setup
import os


setup(
    name="RobotPy-Limelight",
    version="2020.0.3",
    author="Josh Bacon",
    author_email="bacon.josh09@gmail.com",
    packages=["limelight"],
    url="https://pypi.org/project/robotpy-limelight",
    license="LICENSE",
    description="RobotPy Limelight utilities",
    long_description=open("README.rst").read(),
    install_requires=["pynetworktables >= 2019"],
)
