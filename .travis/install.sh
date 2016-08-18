#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then

    # Install some custom requirements on OS X
    # e.g. brew install pyenv-virtualenv
    stty rows 40 columns 80 # set rows, columns in terminal
    wget https://distfiles.macports.org/MacPorts/MacPorts-2.3.3.tar.bz2
    tar xvfj MacPorts-2.3.3.tar.bz2
    cd MacPorts-2.3.3
    ./configure && sudo make install
    export PATH=/opt/local/bin:$PATH
    sudo port -v selfupdate
    cp /opt/local/etc/macports/sources.conf .
    echo "https://leanprover.github.io/macports/ports.tar" >> sources.conf
    sudo mv -f sources.conf /opt/local/etc/macports/sources.conf

    case "${TOXENV}" in
        py33)
            # Install some custom Python 3.3 requirements on OS X
            sudo port install py33-poppler-pyqt4
            ;;
        py34)
            sudo port install py34-poppler-pyqt4
            ;;
        py35)
            sudo port install py35-poppler-pyqt4
            ;;
    esac
else
    sudo add-apt-repository "deb http://us.archive.ubuntu.com/ubuntu wily main universe"
    sudo rm /etc/dpkg/dpkg.cfg.d/multiarch
    sudo dpkg --configure -a
    sudo apt-get install -f
    sudo apt-get update -q
    sudo apt-get install python3-poppler-pyqt4
    # Install some custom requirements on Linux
    sudo apt-get install python3-sip-dev
fi