from setuptools import setup, find_packages
import os.path

version = "2.0b1"


def read(name):
    """Read a file in cwd."""
    with open(name) as f:
        return f.read()

setup(
    name="z3c.caching",
    version=version,
    description="Caching infrastructure for web apps",
    long_description="\n\n".join([
        read("README.txt"),
        read(os.path.join("docs", "HISTORY.txt"))]),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="zope caching",
    author="Wichert Akkerman",
    author_email="zope-dev@zope.org",
    url="https://github.com/zopefoundation/z3c.caching",
    license="ZPL",
    namespace_packages=["z3c"],
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "zope.interface",
        "zope.component",
        "zope.event",
        "zope.lifecycleevent",
        "zope.browser",
    ],
    extras_require={
        "zcml": ("zope.configuration", )
    },
    tests_require="nose >=0.10.0b1",
    test_suite="nose.collector",
)
