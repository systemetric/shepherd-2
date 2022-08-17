echo "Running shepherd-2 installer"
set -e
set -o pipefail

if ! command -v poetry
then
    echo "Poetry could not be found running installer"
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="~/.local/bin:$PATH"
    if ! command -v poetry
    then
        echo "Poetry install failed please follow steps at: "
        echo "https://python-poetry.org/docs/master/#installing-with-the-official-installer"
    fi
fi

echo "installing python dependancies using poetry"
poetry install

# Can be used with --debug for hot reload
touch run.sh
echo "poetry run uvicorn app:app" > run.sh

echo "========================================"
echo "INSTALL COMPLETE: Use 'sh run.sh' to run"
echo "========================================"
