# This repository contains sample data user fpr Swe-Deb Q&A

## Installation

1. Make sure Python 3.11 is install and activated (e.g. via `pyenv`)

2. Create a new virtual environment and install `pyriksprot-tagger`.

```bash
% python -m venv .venv
% . .venv/bin/activate
% pip install pyriksprot_tagger
```

3. Create a text file with name of protocols that you want to be included in sample dataset.

4. Generate sample dataset `subset-corpus DOCUMENTS_FILENAME TARGET_FOLDER TAG`

```bash
% subset-corpus filenames.txt ./data/v0.6.0/dataset-01 v0.6.0
```


