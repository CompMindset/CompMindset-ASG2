from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rostering-app",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Flask-based rostering application for staff management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rostering-app",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Flask",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.1",
            "coverage",
        ],
    },
    entry_points={
        "console_scripts": [
            "rostering-app=wsgi:app",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)