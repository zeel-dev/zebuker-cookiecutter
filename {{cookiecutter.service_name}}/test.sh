#/bin/bash

./install_dependencies.sh --dev
find . | grep -E "(__pycache__|\.pytest_cache)" | xargs rm -rf
pipenv run python3 -m pytest $@