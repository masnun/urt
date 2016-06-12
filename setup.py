from setuptools import setup

setup(
    name='urt',
    version='0.1',
    description='Urban Terror Server Monitor',
    url='http://github.com/masnun/urt',
    author='Abu Ashraf Masnun',
    author_email='masnun@gmail.com',
    license='MIT',
    packages=['pyurt'],
    install_requires=[
        'urwid',
    ],
    scripts=['pyurt/urt.py']
)
