#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from enum import Enum

class VersionType(Enum):
    """Enums for all available bump types.

    Args:
        Enum (str): The bump type.
    """    

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    BUILD = "build"

class GenericVersion:
    """Class responsible for managing and bumping the version number of 
    VERSION text files. It only expects the VERSION file to exists on the 
    root directory, so it works for multiple project types.

    It work for version numbers with and without build version. Examples:

        1.0.0
        1.0.0+1
    """    

    def __init__(self):
        """Performs the class initialization.
        """        

        self.filename = 'VERSION'
        self.bump_type : VersionType | None
        self.current_version = self._get_current_version()
        self.next_version : str | None

    def set_bump_type(self, bump_type: str) -> None:
        """Sets the bump type for processing. If you set `bump_type` as `build` and 
        your build version does not have, an error will occur later.

        Args:
            bump_type (str): Values accepted are `['major', 'minor', 'patch', 'build']`.

        Raises:
            ValueError: Raises if invalid `bump_type` is provided.
        """        

        if bump_type not in VersionType._value2member_map_:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        self.bump_type = VersionType(bump_type)


    def _get_current_version(self) -> str:
        """Gets the current version from VERSION file.

        Returns:
            str: The version number.
        """        

        with open(self.filename, 'w') as f:
            return f.read().strip()
    

    def get_next_version(self) -> str:
        """Decides if version have a build version or not and call the appropriate 
        processing function accordingly.

        Returns:
            str: The next version.
        """        

        if self.current_version.find('+') > 0:
            return self._get_next_version_with_build()
        else:
            return self._get_next_version_without_build()
    
    def _get_next_version_with_build(self) -> str:
        """Get the next version. Assumes there is a build version. Ex: 1.0.0+1

        Returns:
            str: The next version.
        """        

        build_str = self.current_version.split("+")[1]
        major_str, minor_str, patch_str = self.current_version.split("+")[0].split(".")
        
        major = int(major_str)
        minor = int(minor_str)
        patch = int(patch_str)
        build = int(build_str)

        match self.bump_type:
            case VersionType.BUILD:
                build += 1
            case VersionType.PATCH:
                patch += 1
                build = 1
            case VersionType.MINOR:
                minor += 1
                patch = 0
                build = 1
            case VersionType.MAJOR:
                major += 1
                minor = 0
                patch = 0
                build = 1

        self.next_version = f"{major}.{minor}.{patch}+{build}"
        return self.next_version
    
    def _get_next_version_without_build(self) -> str:
        """Get the next version. Assumes there is not a build version. Ex: 1.0.0

        Returns:
            str: The next version.
        """   

        major_str, minor_str, patch_str = self.current_version.split(".")
        
        major = int(major_str)
        minor = int(minor_str)
        patch = int(patch_str)

        match self.bump_type:
            case VersionType.PATCH:
                patch += 1
            case VersionType.MINOR:
                minor += 1
                patch = 0
            case VersionType.MAJOR:
                major += 1
                minor = 0
                patch = 0

        self.next_version = f"{major}.{minor}.{patch}"
        return self.next_version

    def write_new_version(self) -> None:
        """Writes the next version on the pubspec.yaml file.
        """        

        with open(self.filename, 'w') as f:
            f.write(self.next_version)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Bump version script")
    parser.add_argument("version_type", choices=["major", "minor", "patch", "build"], help="Type of version bump")
    args = parser.parse_args()
    version_type = args.version_type

    version_handler = GenericVersion()
    version_handler.set_bump_type(version_type)
    next_version = version_handler.get_next_version()
    version_handler.write_new_version()

    print(next_version)