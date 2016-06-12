from setuptools import setup

setup(
    name='urt',
    version='0.1.2',
    description='Urban Terror Server Monitor',
    url='http://github.com/masnun/urt',
    author='Abu Ashraf Masnun',
    author_email='masnun@gmail.com',
    license='MIT',
    packages=['urt'],
    install_requires=[
        'urwid',
    ],
    scripts=['urt/urt'],
    long_description=open("README.md").read()
)
