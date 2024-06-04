import setuptools
from setuptools import setup
setup(
    name="pytkit",
    version="0.0",
    description="""Python modules that can be shared across projects.""",
    url="",
    author="Vj",
    author_email="venkatesh.jatla@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(""),
    install_requires=[
        'pretty_errors',
        'pytest',
        'scikit-video',
        'opencv-python',
        'matplotlib',
        'pandas',
        'plotly',
        'tqdm',
        'wget',
        'keyboard',
        'openpyxl',
        'torchsummary',
        'scikit-learn'
    ],
    zip_safe=False,
)
