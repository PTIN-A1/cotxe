from setuptools import setup, find_packages

setup(
    name="cotxe-ptin",
    version="0.3.0",
    packages=find_packages(where=["src"]), # Busca a dins de src
    package_dir={"": "src"}, # El paquet arrel és el directori src
    py_modules=["main", "car", "peripherals"],
    install_requires=[
        "PCA9685_smbus2",
        "pyserial",
        "certifi",
        "websockets",
    ],
    entry_points={
        "console_scripts": [
            "cotxe-ptin = main:run_main",
        ],
    },
)
