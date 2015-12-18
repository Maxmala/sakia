#!/usr/bin/env bash

brew update
brew install libsodium
## Ensure your brew QT version is up to date. (brew install qt -> qt 4.8)
brew install qt5
brew link --force qt5
brew install pyenv-virtualenv

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv activate sakia-env
if [ $? -ne 0 ]
then
    echo "Sakia env cache cleared, rebuilding it..."
    env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install $PYENV_PYTHON_VERSION

    pyenv shell $PYENV_PYTHON_VERSION
    pyenv virtualenv sakia-env

    cd $HOME

    wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.17/sip-4.17.tar.gz
    tar xzf sip-4.17.tar.gz
    cd sip-4.17/
    pyenv activate sakia-env
    python configure.py
    make && make install
    pyenv rehash

    cd $HOME

    wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt-gpl-5.5.1.tar.gz
    tar xzf PyQt-gpl-5.5.1.tar.gz
    cd PyQt-gpl-5.5.1/
    pyenv activate sakia-env
    python configure.py --confirm-license
    make -j 2 && make install
    pyenv rehash

fi