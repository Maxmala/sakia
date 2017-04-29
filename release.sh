#!/bin/bash

#__version_info__ = ('0', '20', '0dev6')
current=`grep -P "__version_info__ = \(\'\d+\', \'\d+\', \'\d+(\w*)\'\)" src/sakia/__init__.py | grep -oP "\'\d+\', \'\d+\', \'\d+(\w*)\'"`
echo "Current version: $current"

if [[ $1 =~ ^[0-9]+.[0-9]+.[0-9]+[0-9A-Za-z]*$ ]]; then
  IFS='.' read -r -a array <<< "$1"
  sed -i "s/__version_info__\ = ($current)/__version_info__ = ('${array[0]}', '${array[1]}', '${array[2]}')/g" src/sakia/__init__.py
  sed -i "s/#define MyAppVerStr .*/#define MyAppVerStr \"$1\"/g" ci/appveyor/sakia.iss
  sed -i "s/Version: .*/Version: $1/g" ci/travis/debian/DEBIAN/control
  sed -i "s/Version=.*/Version=$1/g" ci/travis/debian/usr/share/applications/sakia.desktop
  git commit src/sakia/__init__.py ci/appveyor/sakia.iss ci/travis/debian/DEBIAN/control ci/travis/debian/usr/share/applications/sakia.desktop -m "$1"
  git tag "$1" -a -m "$1"
else
  echo "Wrong version format"
fi
