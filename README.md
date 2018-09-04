# tar-manifest

tar-manifest is a Python 3 program that creates a manifest file in CSV format
for all the files in a given TAR file.

## Requirements

This script uses standard libraries from Python version 3.

## Usage

```
usage: tar_manifest.py [-h] [-l LICENSE] [-o OUTPUT] [-r REPOSITORY] [-t TAR]

Create a CSV manifest from a TAR file.

optional arguments:
  -h, --help            show this help message and exit
  -l LICENSE, --license LICENSE
                        The relative path to the XML file containing the license mapping
  -o OUTPUT, --output OUTPUT
                        The path and name of the file to store the output
  -r REPOSITORY, --repository REPOSITORY
                        The URL to the source repository
  -t TAR, --tar TAR     The name of the TAR file to process
```
Running the program with command line arguments:
```
./tar-manifest.py --tar /path/to/archive.tar.gz --license path/to/license-report.xml --repository http://github.com/mbruzek/tar-manifest.git --output manifest.csv
```

Running the program is run with no arguments, will prompt for the options:

```
./tar-manifest.py
The name of the TAR file to process:
```

## License

This program is released under the [Apache 2.0 license](LICENSE.txt).
