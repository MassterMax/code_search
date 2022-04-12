import pathlib
import pkg_resources
from setuptools import setup, find_packages
from setuptools.command.develop import develop

try:
    from post_setup import main as post_install
except ImportError:
    post_install = lambda: None

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        post_install()


setup(
    name='codesearch',
    version='0.1.0',
    packages=find_packages(include='codesearch'),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'cs = codesearch.cmd.run:cs',
        ],
    },
    cmdclass={
        'develop': PostDevelopCommand,
    },
)