from os.path import exists

from setuptools import find_packages, setup

if exists("README.md"):
    with open("README.md") as f:
        long_description = f.read()
else:
    long_description = ""

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Education",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Scientific/Engineering :: Atmospheric Science",
]

setup(
    maintainer="Aaron Spring",
    maintainer_email="aaron.spring@mpimet.mpg.de",
    description="intake catalogs for climate data sources on the internet for python",
    install_requires=install_requires,
    python_requires=">=3.7",
    license="MIT",
    long_description=long_description,
    classifiers=CLASSIFIERS,
    name="remote_climate_data",
    packages=find_packages(),
    test_suite="tests",
    tests_require=["pytest"],
    url="https://github.com/aaronspring/remote_climate_data/",
    use_scm_version={"version_scheme": "post-release", "local_scheme": "dirty-tag"},
    zip_safe=False,
    # extras_require=extras_require,
)
