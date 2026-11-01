from setuptools import setup, find_packages

setup(
    name="token-saver",
    version="1.0.0",
    description="Dual-Mode Token Optimizer & Active Session Ledger for AI Coding Workflows",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Tanush Garg & Community",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # Pure standard library by default; optional packages for exact token counts
    ],
    entry_points={
        "console_scripts": [
            "session-log=token_saver.session_cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)

