from setuptools import setup, find_packages

setup(
    name="cotxe-ptin",
    version="0.4.0",
    # Buscar paquets a dins del directori src/
    packages=find_packages(where="src"),
    package_dir={
        "": "src"
    },  # Indicar que els paquets del projecte estan a src/ i no a l'arrel del projecte
    install_requires=[
        # "PCA9685_smbus2",
        # "pyserial",
        "certifi",
        "websockets",
    ],
    # entry_points={
    #    "console_scripts": [
    #        "cotxe-ptin = src.main",
    #   ],
    # },
)
