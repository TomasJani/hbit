#!/usr/bin/env bash

set -e

# Variables
URL="https://cwe.mitre.org/data/xml/cwec_latest.xml.zip"
OUTPUT_ZIP="cwec_latest.xml.zip"
OUTPUT_DIR="hbit_data/data/"

# Download the ZIP file
echo "Downloading file..."
curl -o "$OUTPUT_ZIP" "$URL"

# Check if the file was downloaded successfully
if [ $? -eq 0 ]; then
    echo "Download completed: $OUTPUT_ZIP"
else
    echo "Failed to download the file."
    exit 1
fi

# Unzip the file
echo "Unzipping file..."
unzip -o "$OUTPUT_ZIP" -d "$OUTPUT_DIR"

# Check if unzipping was successful
if [ $? -eq 0 ]; then
    echo "File unzipped to directory: $OUTPUT_DIR"
else
    echo "Failed to unzip the file."
    exit 1
fi

mv hbit_data/data/cwec*.xml hbit_data/data/cwes.xml

# Cleanup
echo "Cleaning up..."
rm -f "$OUTPUT_ZIP"

echo "Done."