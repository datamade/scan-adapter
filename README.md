# 🦠 scan-adapter

An adapter to retrieve and process gene detection results from wastewater samples, as measured by the SCAN lab in California.

## Requirements

- GNU Make
- wget
- Python 3.6+

## Setup

Install wget, if applicable, and the Python requirements:

```
# Mac (assumes Homebrew install)
brew install wget

# Unix variants
apt-get update && apt-get wget

# All operating systems
python3 -m venv ~/.virtualenvs/scan-adapter
source ~/.virtualenvs/bin/activate
pip install -r requirements.txt
```

## Usage

Make the data:

```
make
```

You should have a fresh version of the processed result data, located at `data/processed/all_plants.csv`. See [SCAN's data dictionary](https://docs.google.com/document/d/1qiNq3wh0H8GrELesgLUrDZF9oTdanI40CZ6tEZSUbic/edit?usp=sharing) for more information about its contents.

To clean up and start over: 

```
make clean
```