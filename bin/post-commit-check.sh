#! /usr/bin/env bash
set -e

#
# Requires OPENAI_API_KEY to be set in the environment
#

echo
echo "----------------------------------------"
echo "Sanity using pip"
echo "----------------------------------------"
WORK_DIR=`mktemp -d -t debaser`
cd $WORK_DIR
echo "WORK_DIR: $WORK_DIR"

mkdir debaser
cp -r $DEBASER_DIR debaser
cd debaser
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python debaser.py topic
cd ~
rm -rf $WORK_DIR

echo
echo "----------------------------------------"
echo "Sanity using pip"
echo "----------------------------------------"
WORK_DIR=`mktemp -d -t debaser`
cd $WORK_DIR
echo "WORK_DIR: $WORK_DIR"

mkdir debaser
cp -r $DEBASER_DIR debaser
cd debaser
poetry install
poetry run python debaser.py topic
cd ~
rm -rf $WORK_DIR
