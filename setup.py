from setuptools import setup, find_packages

setup(
    name="cotxe-ptin",
    version="0.3.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        #"PCA9685_smbus2",
        "pyserial",
        "certifi",
        "websockets",
    ],
    entry_points={
        "console_scripts": [
            "cotxe-ptin = cotxe_ptin.main:run_main",
        ],
    },
)
