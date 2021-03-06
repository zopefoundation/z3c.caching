from setuptools import setup, find_packages


version = '2.3.dev0'


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
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
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
