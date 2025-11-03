"""
NETRA Facial Recognition System - Setup Configuration
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="netra-facial-recognition",
    version="1.0.0",
    author="NETRA Team",
    author_email="support@netra.ai",
    description="Enterprise-grade facial recognition using Siamese Neural Networks",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/NETRA-Facial-Recognition-system",
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'scripts']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'dev': read_requirements('requirements-dev.txt'),
    },
    entry_points={
        'console_scripts': [
            'netra-server=app.main:run_server',
            'netra-train=app.train:main',
            'netra-client=app.inference_client:main',
        ],
    },
    include_package_data=True,
    package_data={
        'app': ['*.yaml', '*.yml'],
        'configs': ['*.yaml', '*.yml'],
    },
    zip_safe=False,
    keywords='facial-recognition siamese-network deep-learning computer-vision fastapi',
    project_urls={
        'Documentation': 'https://docs.netra.ai',
        'Source': 'https://github.com/your-org/NETRA-Facial-Recognition-system',
        'Bug Reports': 'https://github.com/your-org/NETRA-Facial-Recognition-system/issues',
    },
)
