# SweDeb Sample Data

This repository contains sample datasets used for Swe-DEB testing and quality control.

## Description

Each dataset is structured as follows:

```
├── dehyphen_datadir
│   └── word-frequencies.pkl
├── logs
│   ├── ...
│   └── log of options used when creating data
├── Makefile
├── opts
│   ├── corpus-configs
│   │   ├── ... corpus configuration files for generating model(s)
│   │   └── corpus-config.yml
│   ├── dtm
│   │   ├── ... each file contains options for creating a DTM
│   │   ├── XYZ.yml ==> assumes existens of ./speeches/tagged_frames_speeches_XYZ.feather
│   │   └── text.yml
│   ├── plain-text-speeches
│   │   ├── ... each file contains options for creating a plain text speech corpus
│   │   ├── text_speeches_base.yml
│   │   └── text_speeches_dedent_dehyphen.yml
│   ├── tagged-speeches
│   │   ├── ... each file contains options for creating a PoS-tagged speech corpus
│   │   └── tagged_frames_speeches_text.feather.yml
│   └── tagger-config.yml
│         => ... specifies options for PoS tagging and lemmatization
├── protocols.txt
└── v0.6.0
    ├── dehyphen_datadir
    ├── dtm
    │   ├── dtm_base_text
    │   │   ├── dtm_base_text_document_index.csv.gz => document index
    │   │   ├── dtm_base_text_token2id.json.gz => vocabulary
    │   │   ├── dtm_base_text_vector_data.npz => DTM sparse matrix
    │   │   └── dtm_base_text_vectorizer_data.json => stored options
    │   └── ... DTMs generated from options above
    ├── parlaclarin
    │   ├── metadata
    │   │   ├── ... => riksprot metadata downloaded from Github
    │   │   ├── ...  * generated data
    │   │   ├── alias.csv
    │   │   ├── government.csv
    │   │   ├── location_specifier.csv
    │   │   ├── member_of_parliament.csv
    │   │   ├── minister.csv
    │   │   ├── name.csv
    │   │   ├── name_location_specifier.csv
    │   │   ├── party_abbreviation.csv
    │   │   ├── party_affiliation.csv
    │   │   ├── person.csv
    │   │   ├── protocols.csv*
    │   │   ├── speaker.csv
    │   │   ├── speaker_notes.csv*
    │   │   ├── twitter.csv
    │   │   ├── unknowns.csv
    │   │   ├── utterances.csv
    │   │   └── * is generated data
    │   └── protocols
    │       ├── ...
    │       └── ParlaCLARIN protocol structure that mirrors Github
    ├── riksprot_metadata.db
    │       └── ... processed Sqlite3 metadata database
    ├── speeches
    │   ├── ... => speech corpora generated from options above
    │   ├── text_speeches_base.zip
    │   └── text_speeches_dedent_dehyphen.zip
    └── tagged_frames
        └── ... tagged version of ParlaCLARIN protocols

```

## How to generate a new dataset



