from setuptools import setup

setup(
    name="cotxe-virtual",
    version="0.3.0",
    packages=["src"],
    py_modules=["src.main_vehicle"],
    install_requires=[
        "websockets",
    ],
    entry_points={
        "console_scripts": [
            "cotxe-virtual = src.main_vehicle:run_main",
        ],
    },
)
