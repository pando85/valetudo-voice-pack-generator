#!/bin/bash

# Default values
src_dir="data/split_audio"
dest_dir="data/piper/commandos/speaker1"

# Check if START and END parameters are provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <START> <END> [SRC_DIR] [DEST_DIR]"
    echo "Example: $0 1 123 /path/to/source /path/to/destination"
    exit 1
fi

# Set the start and end variables
START="$1"
END="$2"

# Override source directory if provided as an argument
if [ "$#" -ge 3 ]; then
    src_dir="$3"
fi

# Override destination directory if provided as an argument
if [ "$#" -ge 4 ]; then
    dest_dir="$4"
fi

wavs_dir="$dest_dir/wavs"
# Create the destination directory if it doesn't exist
mkdir -p "$wavs_dir"

txt_file="$dest_dir/metadata.csv"
rm -f "$txt_file"
touch "$txt_file"

# Copy files from ${START}.wav to ${END}.wav
for ((i=START; i<=END; i++)); do
    filename="${i}.wav"
    txt_filename="${i}.txt"
    cp "${src_dir}/${filename}" "${wavs_dir}/${filename}"
    echo "${filename}|$(cat "${src_dir}/${txt_filename}")" >> "$txt_file"
done

echo "Files copied from ${START}.wav to ${END}.wav to ${dest_dir}"
echo "Filenames and contents saved to ${txt_file}"

zip_file="$(basename ${dest_dir}).zip"
zip -r "$zip_file" "$dest_dir"
