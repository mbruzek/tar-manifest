#!/usr/bin/env python3

"""
tar_manifest is a Python 3 program that creates a comma separated value (CSV)
manifest of the files in a TAR file.

Copyright 2018 Matthew Bruzek

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
import datetime
import os
import sys
import tarfile
import traceback
import xml.etree.ElementTree as ET

DESCRIPTION = 'Create a CSV manifest from a TAR file.'
DEFAULT_OUTPUT = 'manifest.csv'
HEADER = 'Name,Size,Modification date,Checksum,URL'
LICENSE = 'The relative path to the XML file containing the license mapping'
NEWLINE = '\n'
OUTPUT = 'The path and name of the file to store the output'
REPOSITORY = 'The URL to the source repository'
TAR_FILE = 'The name of the TAR file to process'
URL = 'The URL for the JAR license'


def create_manifest(tar_file, license, repository):
    """Create a CSV manifest from the files in a TAR file."""
    manifest = ""
    # Open the TAR file for reading.
    with tarfile.open(tar_file, 'r:gz') as tar_reader:
        # Extract the license report file to an in memory reader.
        xml_reader = tar_reader.extractfile(license)
        # Get the dictionary of jar file to license url.
        jar_files = jar_to_license(xml_reader)
        # Write the column header.
        manifest += HEADER + NEWLINE
        # Loop through the files and directories in the TAR file.
        for tarinfo in tar_reader:
            if tarinfo.isfile():
                name = tarinfo.name
                basename = os.path.basename(name)
                # Create a date from the last modified timestamp.
                modified = datetime.datetime.fromtimestamp(tarinfo.mtime)
                url = ""
                if basename.endswith('.jar') and basename in jar_files:
                    # Add a url link to the license for one JAR file.
                    url = jar_files[basename]
                elif repository:
                    # Add a url link to the repository for one other file type.
                    url = repository
                    repository = None
                # Create the CSV line for this file inside the TAR.
                manifest += '{0},{1},{2},{3},{4}'.format(
                                name, tarinfo.size, modified.strftime('%c'),
                                tarinfo.chksum, url)
                manifest += NEWLINE
    return manifest

def jar_to_license(license_report):
    """Create a mapping from JAR file basename to license url based on the
    license-report.xml file."""
    # Parse the xml file.
    tree = ET.parse(license_report)
    licenses = tree.getroot()
    jar_to_license = {}
    for license in licenses:
        url = license.attrib['url']
        if url:
            for dependency in license:
                name = dependency.attrib['jar']
                if name:
                    jar_to_license[name] = url
    return jar_to_license

def handle_output(output_file, output):
    """Write the output to a file, or standard output."""
    if output_file:
        # When there is an output file write the output to a file.
        with open(output_file, 'w') as writer:
            writer.write(output)
    else:
        # Otherwise print the output to standard out.
        print(output)


def command_line():
    """Parse the arguments from the command line."""
    try:
        # Create an object to parse the command line arguments.
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument('-l', '--license', help=LICENSE)
        parser.add_argument('-o', '--output',  help=OUTPUT)
        parser.add_argument('-r', '--repository', help=REPOSITORY)
        parser.add_argument('-t', '--tar', help=TAR_FILE)
        arguments, extra = parser.parse_known_args()

        manifest = create_manifest(arguments.tar, arguments.license,
                                   arguments.repository)
        handle_output(arguments.output, manifest)
    except Exception:
        print('An exception occurred parsing the command-line arguments.')
        print(traceback.print_exc())
        exit(1)


def interactive():
    """Interactively prompt the user for the program options."""
    tar = input('{0}: '.format(TAR_FILE))
    license = input('{0}: '.format(LICENSE))
    repository = input('{0}: '.format(REPOSITORY))
    out = input('{0} [{1}]: '.format(OUTPUT, DEFAULT_OUTPUT)) or DEFAULT_OUTPUT
    manifest = create_manifest(tar, license, repository)
    handle_output(out, manifest)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command_line()
    else:
        interactive()
