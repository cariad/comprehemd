from pathlib import Path

from setuptools import setup  # pyright: reportMissingTypeStubs=false

from comprehemd import __version__

readme_path = Path(__file__).parent / "README.md"

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Typing :: Typed",
]

if "a" in __version__:
    classifiers.append("Development Status :: 3 - Alpha")
elif "b" in __version__:
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")

classifiers.sort()

setup(
    author="Cariad Eccleston",
    author_email="cariad@cariad.earth",
    classifiers=classifiers,
    description="Markdown parser",
    include_package_data=True,
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="comprehemd",
    packages=[
        "comprehemd",
        "comprehemd.blocks",
        "comprehemd.code_patterns",
    ],
    package_data={
        "comprehemd": ["py.typed"],
        "comprehemd.blocks": ["py.typed"],
        "comprehemd.code_patterns": ["py.typed"],
    },
    python_requires=">=3.8",
    url="https://github.com/cariad/comprehemd",
    version=__version__,
)
