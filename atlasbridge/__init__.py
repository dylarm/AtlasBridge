import logging
from typing import Dict, Any

_package_data = dict(
    full_package_name="atlasbridge",
    version_info=(0, 0, 0),
    __version__="0.0.0",
    author="Dylan Armitage",
    author_email="dylanjarmitage@gmail.com",
    description="AtlasBridge processes grades exported from different services, allowing them to be uploaded to ATLAS",  # NOQA
    since=2021,
    keywords="yaml 1.2 parser round-trip preserve quotes order config",
    read_the_docs="yaml",
    supported=[(3, 6)],  # minimum tested
    python_requires=">=3",
)  # type: Dict[Any, Any]


version_info = _package_data["version_info"]
__version__ = _package_data["__version__"]
__author__ = _package_data["author"]
__email__ = _package_data["author_email"]


def main() -> None:
    pass


if __name__ == "__main__":
    main()
