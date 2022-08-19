# Install poetry
# Use poetry to install and setup a virtual env for shepherd
# Create a script for running poetry

echo "Running shepherd-2 installer"

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

# Can be used with --debug for hot reload
touch run.sh
echo "poetry run uvicorn app:app" > run.sh

echo "installing python dependancies using poetry"
if poetry install; then
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
echo "SOLUTION: install.sh is able to install python3.10 do you want to try [y/n] "
echo "-------------------------------------------------------------------------------------"
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

# Taken from https://rnealpython.com/installing-python/#how-to-build-python-from-source-code
echo "We need sudo to install packages with apt to build python with"
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
       libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
       libncurses5-dev libncursesw5-dev xz-utils tk-dev
wget https://www.python.org/ftp/python/3.10.6/Python-3.10.6.tgz
tar xvf Python-3.10.6.tgz
cd Python-3.10.6
./configure --enable-optimizations --with-ensurepip=install
make -j4
sudo make altinstall
cd ..

if poetry install; then
    echo "========================================"
    echo "INSTALL COMPLETE: Use 'sh run.sh' to run"
    echo "========================================"
    exit
else
    echo "'poetry install' failed :("
fi
