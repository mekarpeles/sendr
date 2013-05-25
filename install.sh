#!/bin/bash

sudo pip install --upgrade .
git clone https://github.com/mekarpeles/sendr_stdlib stdlib
cd sendr
rm stdlib
ln -s ../stdlib stdlib
