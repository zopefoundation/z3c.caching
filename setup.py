from setuptools import find_packages
from setuptools import setup


version = '3.1'


def read(name):
    """Read a file in cwd."""
    with open(name) as f:
        return f.read()


setup(
    name="z3c.caching",
    version=version,
    description="Caching infrastructure for web apps",
    long_description="\n\n".join([
        read("README.rst"),
        read("CHANGES.rst")]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="zope caching",
    author="Wichert Akkerman",
    author_email="zope-dev@zope.dev",
    url="https://github.com/zopefoundation/z3c.caching",
    license="ZPL",
    namespace_packages=["z3c"],
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=[
        "setuptools",
        "zope.browser",
        "zope.component",
        "zope.event",
        "zope.interface>=3.8.0",
        "zope.schema",
        "zope.lifecycleevent",
    ],
    extras_require={
        "zcml": ("zope.configuration", ),
        "test": ("zope.configuration", ),
    },
)
