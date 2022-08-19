# Install poetry
# Use poetry to install and setup a virtual env for shepherd
# Create a script for running poetry

echo "Running shepherd-2 installer"

if ! command -v poetry
then
    echo "Poetry not found. Downloading and installing."
    curl -sSL https://install.python-poetry.org | python3 - || exit
    export PATH="~/.local/bin:$PATH"
    echo "WARNING: Ensure that '~/.local/bin:$PATH' is added to the path"
    if ! command -v poetry
    then
        echo "Poetry install failed please follow steps at: "
        echo "https://python-poetry.org/docs/master/#installing-with-the-official-installer"
    fi
fi

# Can be used with --debug for hot reload
touch run.sh
echo "poetry run uvicorn app:app" > run.sh

echo "installing python dependancies using poetry"
if poetry install; then
    echo "========================================"
    echo "INSTALL COMPLETE: Use 'sh run.sh' to run"
    echo "========================================"
else
    echo "-------------------------------------------------------------------------------------"
    echo "FAILED: Poetry failed to install dependancies. Maybe there is no good python version."
    echo "Download and build python:"
    echo "  - Guide: https://realpython.com/installing-python/#how-to-build-python-from-source-code"
    echo "  - Offical python docs: https://docs.python.org/3/using/unix.html"
    echo "-------------------------------------------------------------------------------------"
    exit
fi

