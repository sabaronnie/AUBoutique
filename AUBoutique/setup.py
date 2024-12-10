from setuptools import setup, find_packages

setup(
    name="AUBoutique",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt5",
        # Add other dependencies if needed
    ],
    entry_points={
        'console_scripts': [
            'aub-s = AUBoutique.BackEnd.server',
            'aub = AUBoutique.FrontEnd.firstpage',
        ],
    },
)