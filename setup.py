from setuptools import setup

def readme():
    """Import the README.md Markdown file and try to convert it to RST format."""
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError):
        with open('README.md') as readme_file:
            return readme_file.read()
setup(
    name='petadoption',
    version='0.1',
    description='Analysis of the pet adoption,
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    url='https://github.com/hanh-nguyen/petadoption',
    author='Hanh Nguyen',  
    author_email='myhanh.nguyen1211@gmail.com',  
    license='MIT',
    packages=['petadoption'],
    install_requires=[]
)