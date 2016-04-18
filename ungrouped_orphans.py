#!/usr/bin/env python

"""
Usage: ungrouped_orphans.py [GROUP1] [GROUP2] ...

Lists all installed orphan RPM packages that don't belong to the provided
packages groups or environments.

Requires dnf and rpmorphan.
"""

from sys import argv
from subprocess import check_output
from re import match

def main():
    groups = set(argv[1:])
    installed_packages = set()
    required_packages = set()
    add_item = False

    # Get installed packages that aren't dependencies of another installed package

    for line in check_output(["rpmorphan", "-all"]).split("\n"):
        installed_packages.add(line)

    # This first run of dnf group info is to get the complete set of groups from
    # the supplied environments and groups

    cmd = "dnf group info".split()
    cmd.extend(groups)
    for line in check_output(cmd).split("\n"):
        if match(' [^ ]', line):
            if line == " Mandatory Groups:" or line == " Default Groups:":
                add_item = True
            else:
                add_item = False
        if add_item and match('   [^ ]', line):
            groups.add(line.strip())

    # Now we run dnf group info with all of the groups to get the list of all
    # required packages

    cmd = "dnf group info".split()
    cmd.extend(groups)
    for line in check_output(cmd).split("\n"):
        if match(' [^ ]', line):
            if line == " Mandatory Packages:" or line == " Default Packages:":
                add_item = True
            else:
                add_item = False
        if add_item and match('   [^ ]', line):
            required_packages.add(line.strip())

    installed_packages.difference_update(required_packages)
    for package in sorted(list(installed_packages)):
        print package

if __name__ == "__main__":
    main()
