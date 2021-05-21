## Ubuntu 20.04
sudo apt update
sudo apt upgrade
sudo apt install python3-pip
sudo apt install -y build-essential \
                    libssl-dev \
                    zlib1g-dev \
                    libbz2-dev \
                    libreadline-dev \
                    libsqlite3-dev \
                    llvm \
                    libncurses5-dev \
                    xz-utils \
                    tk-dev \
                    libxml2-dev \
                    libxmlsec1-dev \
                    libffi-dev \
                    liblzma-dev

## Install pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
touch ~/.bash_profile
echo -e "# pyenv paths" >> ~/.bash_profile
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
echo -e "# Load .bashrc" >> ~/.bash_profile
echo 'source ~/.bashrc' >> ~/.bash_profile

## Install python for pyenv
pyenv install 3.6.9
pyenv install 3.7.5
pyenv install 3.8.3

## Install packages for 3.6.9
pyenv global 3.6.9
pip install --upgrade pip
pip install -r requirements.txt

## Install waymo dataset
rm -rf waymo-od > /dev/null
git clone https://github.com/waymo-research/waymo-open-dataset.git waymo-od
cd waymo-od && git branch -a
cd waymo-od && git checkout remotes/origin/r1.0
pip install waymo-open-dataset
pip install waymo-od-tf2-0
