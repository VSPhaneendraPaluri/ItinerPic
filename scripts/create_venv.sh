#!/usr/bin/env bash
ENV_NAME="venv"
python3 -m venv "$ENV_NAME"
source "$ENV_NAME/bin/activate"
pip install --upgrade pip
pip install -r ../requirements.txt
echo "Done. Activate with: source $ENV_NAME/bin/activate"
