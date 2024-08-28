from setuptools import setup, find_packages

setup(
    name='aitools',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "openai==1.30.4",
        "tabulate==0.9.0",
    ],
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