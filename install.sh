#!/bin/bash

sudo pip install .
git clone https://github.com/mekarpeles/sendr_stdlib stdlib
rm sendr/stdlib
ln -s stdlib sendr/stdlib
#cd stdlib;pip install .