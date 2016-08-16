from setuptools import setup, find_packages


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = ''


setup(
    name='winremote',
    version='1.1.4',
    description='Tool to manage your windows machines remotely',
    long_description=long_description,
    url='https://github.com/machacekondra/winremote',
    author='Ondra Machacek',
    author_email='machacek.ondra@gmail.com',
    license='GPLv3+',
    keywords='windows winrm',
    install_requires=['argparse', 'pywinrm'],
    requires=['pypandoc', 'pywinrm', 'argparse'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'winremote = winremote.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
