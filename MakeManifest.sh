#!/bin/bash
# Remove comments '#' and empty lines from Apiary.Manifest.$EXT file
# for proper apiary.io documentation.
# Example of using: ./MakeManifest.sh all

grep -v "#" apiary.manifest.$1 | grep -v -e '^$' > apiary.manifest
