from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="groot-quant",
    version="0.1.1",
    author="xiejingxian",
    author_email="xiejingxian@zju.edu.cn",
    description="A quantitative tool that run strategy through a large model semantic filtering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JaneShine/groot",
    packages=find_packages(),
    install_requires=[
        "dash==1.20.0",
        "dash_core_components==1.16.0",
        "dash_html_components==1.1.3",
        "numpy==1.24.4",
        "pandas==2.0.3",
        "plotly==4.14.3",
        "pywencai==0.12.2",
        "setuptools==69.5.1",
        "tqdm==4.66.2",
        "tushare==1.2.62",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'im groot=main:main',
        ],
    },
)
