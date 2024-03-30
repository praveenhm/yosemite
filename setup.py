import setuptools

setuptools.setup(
    name="yosemite",
    version="0.1.12",
    author="Hammad Saeed",
    author_email="hammad@supportvectors.com",
    description="yosemite",
    entry_points={
        'console_scripts': [
            'yosemite = yosemite.__cli__.cli:cli',
        ],
    },
    long_description="""
Yosemite
    """,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.8',
    install_requires=[
"argparse",
"art",
'customtkinter',
"prompt_toolkit",
"wcwidth",
'annoy',
'anthropic',
'ebooklib',
'instructor',
'mistralai',
'pandas',
'pdfminer.six',
'PyPDF2',
'rich',
'sentence-transformers',
'spacy',
'wheel',
"Whoosh",
"xai-sdk",
    ],
)