#!/bin/bash
set -e

print_help() {
    echo "Usage: $0 -m MODEL_NAME [-i INPUT_DIR] [-o OUTPUT_DIR]"
}

input_directory="data/original/EN"
txt_directory="${input_directory}_text"
output_directory="data/output/EN"
temp_dir=$(mktemp -d)

while getopts ":m:i:o:" opt; do
    case $opt in
        m)
            model="$OPTARG"
            ;;
        i)
            input_directory="$OPTARG"
            txt_directory="${input_directory}_text"
            ;;
        o)
            output_directory="$OPTARG"
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            print_help
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            print_help
            exit 1
            ;;
    esac
done

if [ -z "$model" ]; then
    echo "Error: --model is required."
    print_help
    exit 1
fi

mkdir -p "$output_directory"

for txt_file in "${txt_directory}"/*.txt; do
    filename=$(basename -- "$txt_file")
    filename_no_ext="${filename%.*}"
    output_path="${output_directory}/${filename_no_ext}.ogg"

    if [ -e "$output_path" ]; then
        echo "${output_path} already exists"
    else
        # if file is empty
        if [ ! -s "$txt_file" ]; then
            cp "${input_directory}/${filename_no_ext}.ogg" "${output_path}"
            echo "Copy original file to ${output_path}"
        else
            wav_file="${temp_dir}/${filename_no_ext}.wav"
            cat "$txt_file" | piper --model "$model" --output_file "$wav_file"
            echo "Text from $filename converted to $output_path"

            ffmpeg -i "$wav_file" -c:a libvorbis -q:a 4 "$output_path" > /dev/null 2>&1
            echo "WAV file $filename converted to $output_path"
        fi
    fi
done
