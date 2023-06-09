#/bin/bash

for file in returned_object_examples/*.json
do
    python3 -m json.tool "$file" > "$file.1"
    mv "$file.1" "$file"
done
