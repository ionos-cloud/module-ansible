echo "copying files to run them from top package cause relative imports do not work..."
cp docs_utils/docs_generator.py docs_generator.py
cp docs_utils/update_ansible_documentation.py update_ansible_documentation.py
cp docs_utils/update_descriptions.py update_descriptions.py
cp docs_utils/update_examples.py update_examples.py

echo "deleting cached swagger files to see description changes for watched parameters..."
rm update_description_utils/swaggers/*

echo "updating parameter descriptions from the swaggers..."
python3 update_descriptions.py

echo "update examples from tests"
python3 update_examples.py

echo "updating DOCUMENTATION and EXAMPLES fields from OPTIONS and EXAMPLES_PER_STATE..."
python3 update_ansible_documentation.py

echo "generating md files..."
python3 docs_generator.py

echo "cleanup"
rm docs_generator.py update_ansible_documentation.py update_descriptions.py update_examples.py
