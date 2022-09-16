from setuptools import setup

setup(
    name='chris-plugin-graphicsmagick',
    version='0.1.0',
    description='GraphicsMagick plugin for ChRIS medical imaging',
    author='Jiri Stransky and FNNDSC',
    author_email='dev@babyMRI.org',
    url='https://github.com/rh-impact/pl-graphicsmagick',
    py_modules=['app'],
    install_requires=['chris_plugin'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'chris-gm = app:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.1',
            'pytest-mock~=3.8'
        ]
    }
)
