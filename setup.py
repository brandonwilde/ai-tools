from setuptools import setup, find_packages

def read_requirements():
    """Read the requirements.txt file and return a list of dependencies."""
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='aitools',
    version='0.1',
    packages=find_packages(),
    install_requires=read_requirements(),
    author='Brandon T Wilde',
    author_email='brandon.t.wilde@gmail.com',
    description='A collection of general-purpose tools for processing text, documents, images, and videos.',
    url='https://github.com/brandonwilde/ai-tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)