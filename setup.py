from setuptools import setup, find_packages

setup(
    name="duckdash",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "mysql-connector-python"
    ],
) 