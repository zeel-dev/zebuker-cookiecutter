#/bin/bash

# This file is a quick and dirty way to check that the Pipfile hasn't changed
# since the last time pipenv install was run. All it does is shasum the Pipfile
# and save it to a file within the .venv directory.

# Check to see what the checksum of Pipfile was last time install was run
INSTALLED_SUM_PATH=".venv/LastInstallPipfileSum"
INSTALLED_ARG_PATH=".venv/LastInstallPipfileArg"

# Check for presence of Pipfile.lock
if ! [ -f Pipfile.lock ]; then
    pipenv install $@

    CURRENT_ARG="$@"
    CURRENT_SUM=`cksum Pipfile Pipfile.lock | awk '{print $1}'`

    echo "$CURRENT_SUM" > "$INSTALLED_SUM_PATH"
    echo "$CURRENT_ARG" > "$INSTALLED_ARG_PATH"
    exit 0
fi

# Get checksum of current Pipfile
CURRENT_ARG="$@"
CURRENT_SUM=`cksum Pipfile Pipfile.lock | awk '{print $1}'`

# Sets to null value if LastInstallPipfileSum/Arg doesn't exist
INSTALLED_SUM=`[ -f $INSTALLED_SUM_PATH ] && cat $INSTALLED_SUM_PATH || echo`
INSTALLED_ARG=`[ -f $INSTALLED_ARG_PATH ] && cat $INSTALLED_ARG_PATH || echo`

if ! [[ "$INSTALLED_SUM" == "$CURRENT_SUM" ]] || ! [[ "$INSTALLED_ARG" == "$CURRENT_ARG" ]]; then
    # Run install again if the last install sum or args doesn't match current
    pipenv install $@
    # Save the current sum back to LastInstallSum/Arg path
    echo "$CURRENT_SUM" > "$INSTALLED_SUM_PATH"
    echo "$CURRENT_ARG" > "$INSTALLED_ARG_PATH"
fi