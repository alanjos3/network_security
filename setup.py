from setuptools import setup,find_packages


def get_requirements(file_path:str)->list:
    """
    This function returns a list of requirements from the given file path.
    """
    requirements = []
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements
    
setup(
    name="network_security",
    version="0.0.1",
    author='Alan Jose',
    author_email='alanunni3@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt'),
    description="A Network security project"
)