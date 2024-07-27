from setuptools import find_packages,setup
from typing import List

HYPE_E_DOT = "-e ."

def get_requirements(file_path:str)->List[str]:
    requirements =[]
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPE_E_DOT in requirements:
            requirements.remove(HYPE_E_DOT)

        return requirements

setup(
    name='DiamondPricePredictions',
    version='1.0.0',
    author='Akash',
    author_email='iamakash652@gmail.com',
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()
)