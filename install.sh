# Installs everything which is needed to get up and running with shepherd

echo "Running shepherd-2 installer"

# Poetry needs these to run
sudo apt-get install python3-distutils -y
sudo apt-get install python3-apt -y

if ! command -v poetry
then
    echo "Poetry not found. Downloading and installing."
    curl -sSL https://install.python-poetry.org | python3 - || exit
    echo "WARNING: Ensure that ~/.local/bin is added to the path"
    PATH=$PATH:~/.local/bin
    export PATH
    if ! command -v poetry
    then
        echo "Poetry install failed please follow steps at: "
        echo "https://python-poetry.org/docs/master/#installing-with-the-official-installer"
        exit
    fi
fi


echo "installing python dependancies using poetry"
if poetry install; then
    # Can be used with --debug for hot reload
    touch run.sh
    echo "poetry run uvicorn app:shepherd --host 0.0.0.0" > run.sh
    echo "========================================"
    echo "INSTALL COMPLETE: Use 'sh run.sh' to run"
    echo "========================================"
    exit
fi

echo "-------------------------------------------------------------------------------------"
echo "Poetry failed to install dependancies. Maybe there is no good python version."
echo "You can manually do that here:"
echo "  - Guide: https://realpython.com/installing-python/#how-to-build-python-from-source-code"
echo "  - Offical python docs: https://docs.python.org/3/using/unix.html"
echo "-------------------------------------------------------------------------------------"
echo "SOLUTION: install.sh is able to compile python3.10 from source do you want to try?"
echo "If you are on a pi this will take some hours"
echo "-------------------------------------------------------------------------------------"
echo " [y/n] "
old_stty_cfg=$(stty -g)
stty raw -echo
answer=$( while ! head -c 1 | grep -i '[ny]' ;do true ;done )
stty $old_stty_cfg
if echo "$answer" | grep -iq "^n" ;then
    exit
fi

# This is a problem on Pi's
echo "Please confirm that you are on a system with >2GB of memory+swap (increase swap if not) [y/n] "
old_stty_cfg=$(stty -g)
stty raw -echo
answer=$( while ! head -c 1 | grep -i '[ny]' ;do true ;done )
stty $old_stty_cfg
if echo "$answer" | grep -iq "^n" ;then
    exit
fi

# Install dependencies
echo "Trying to install build tools using apt..."
sudo apt update -y
sudo apt upgrade -y
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
       libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
       libncurses5-dev libncursesw5-dev xz-utils tk-dev

# Get python3.10 tarball
wget https://www.python.org/ftp/python/3.10.6/Python-3.10.6.tgz
tar xvf Python-3.10.6.tgz
cd Python-3.10.6

# Configure and compile
./configure --enable-optimizations --with-ensurepip=install
make -j4
sudo make altinstall
cd ..

rm Python-3.10.6.tgz
sudo rm Python-3.10.6 -rf

echo "python install complete"
echo "Fixing potenitally broken virtual env..."

# Fix the maybe broken virtual env: https://stackoverflow.com/a/63117674/5006710
poetry env remove python3.10
poetry env use python3.10

echo "Installing python dependancies using poetry"

# Try to install the project dependencies again
if poetry install; then
    # Can be used with --debug for hot reload
    touch run.sh
    echo "poetry run uvicorn app:shepherd --host 0.0.0.0" > run.sh
    echo "========================================"
    echo "Make sure to add poetry to your path    "
    echo "PATH=$PATH:~/.local/bin"
    echo "INSTALL COMPLETE: Use 'sh run.sh' to run"
    echo "========================================"
    exit
else
    echo "'poetry install' failed. There is likely some error log above."
fi
