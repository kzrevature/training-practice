
#!/bin/bash

cd $(dirname $0)

# python 3.11 environment
py -V:3.11 -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt