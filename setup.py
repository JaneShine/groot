from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="groot-quant",
    version="0.2.1",
    py_modules=['groot_main'],
    author="xiejingxian",
    author_email="xiejingxian@zju.edu.cn",
    description="A quantitative tool that run strategy through a large model semantic filtering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JaneShine/groot",
    packages=find_packages(),
    install_requires=[
        "dash==2.17.1",
        "flask==3.0.3",
        "pywencai==0.12.2",
        "tqdm==4.66.2",
        "tushare==1.4.7",
        "watchdog==4.0.1",
        "pyfolio==0.9.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'imgroot=groot_main:Go',
        ],
    },
)