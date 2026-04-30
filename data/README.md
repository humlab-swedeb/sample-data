# Sample Data Makefile

This Makefile automates the generation of Swedish parliamentary debate datasets (Swedeb) from ParlaCLARIN XML data. It handles the complete pipeline from raw corpus data to CWB-indexed corpora suitable for linguistic analysis.

## Prerequisites

### Required Tools
- **CWB Core** (Corpus Workbench): `cwb-encode`, `cwb-makeall`, `cwb-huffcode`, `cwb-compress-rdx`
- **CWB/Perl toolkit**: `cwb-make`, `cwb-describe-corpus`
- **Python packages**: `pyriksprot`, `pyriksprot-tagger`, `penelope`

### Installation

Install CWB Core:
```bash
wget -O cwb-3.5.0-src.tar.gz https://master.dl.sourceforge.net/project/cwb/cwb/cwb-3.5/source/cwb-3.5.0-src.tar.gz?viasf=1
tar xvf cwb-3.5.0-src.tar.gz
cd cwb-3.5.0-src
sudo ./install-scripts/install-linux
```

Install CWB/Perl toolkit:
```bash
curl -L https://cpanmin.us | perl - --sudo App::cpanminus
sudo cpan install CWB
```

## Configuration

### Environment Variables (.env file)
Create a `.env` file in the data folder with:

```bash
CORPUS_VERSION=v1.4.1          # Corpus version tag
METADATA_VERSION=v1.1.3        # Metadata version tag
PROJECT_NAME=5files            # Project identifier (used for CWB registry)

# Processing modes (copy|create|skip|tag|subset|protocols)
PARLACLARIN_MODE=protocols     # How to obtain corpus XML files
METADATA_MODE=create           # How to generate metadata
TAGGING_MODE=tag               # How to generate POS-tagged data
WORD_FREQUENCY_MODE=create     # How to generate word frequencies

# Optional overrides
CWB_REGISTRY_FOLDER=./v1.4.1/registry
CWB_REGISTRY_ENTRY=riksprot_5files_v141
```

### Processing Modes

**PARLACLARIN_MODE**:
- `copy` - Copy from global data folder
- `protocols` - Copy specific protocols from list
- `subset` - Generate subset using `subset-corpus`
- `skip` - Use existing data

**METADATA_MODE**:
- `copy` - Copy from global folder
- `create` - Generate from source metadata
- `skip` - Use existing database

**TAGGING_MODE**:
- `copy` - Copy tagged frames from global
- `subset` - Generate subset from global tagged frames
- `tag` - Run POS tagging (slow)
- `skip` - Use existing tagged data

**WORD_FREQUENCY_MODE**:
- `copy` - Copy from global folder
- `create` - Generate from corpus
- `skip` - Use existing frequencies

## Main Targets

### Complete Pipeline
```bash
make all          # Full pipeline: dataset + vrt-data + cwb-data + compression
make dataset      # Generate all intermediate datasets
```

### Individual Stages

#### 1. Configuration
```bash
make config       # Generate config file from .env
make info         # Display current configuration
```

#### 2. Corpus Data
```bash
make parlaclarin-corpus    # Download/copy ParlaCLARIN XML files
make metadata              # Generate metadata database
make speech-index          # Create speech index (CSV/Feather)
make word-frequencies      # Generate word frequency data
```

#### 3. Tagging & Processing
```bash
make tag-protocols         # POS-tag protocols to VRT format
make tagged-speech-corpora # Generate tagged speech corpora
make text-corpora          # Generate plain text speech corpora
make dtm-corpora           # Generate document-term matrices
```

#### 4. CWB Corpus
```bash
make vrt-data              # Generate extended VRT files for CWB
make cwb-data              # Encode VRT to CWB binary format
make cwb-data-manual-compress  # Manually compress CWB data
make cwb-info              # Display CWB corpus information
make describe-corpus       # Describe indexed CWB corpus
```

### Utility Targets
```bash
make clean                 # Remove generated corpus version folder
make reset-corpus-folder   # Clear riksdagen-records folder
make reset-metadata-folder # Clear metadata version folder
make rsync-to-global       # Sync to global data directory (/data/swedeb/)
make metadata-database-vacuum  # Compact SQLite metadata database
make metadata-dump-schema  # Export metadata schema to SQL
```

## Directory Structure

After running `make all`, the following structure is created:

```
{CORPUS_VERSION}/               # e.g., v1.4.1/
├── riksdagen-records/          # ParlaCLARIN XML protocols
├── tagged_frames/              # POS-tagged VRT files
├── speeches/                   # Speech corpora (tagged/text/DTM)
├── vrt/                        # CWB-extended VRT files
├── cwb/                        # CWB binary corpus data
├── registry/                   # CWB registry entries
├── dehyphen/
│   └── word-frequencies.pkl    # Word frequency data
└── speech-index.csv.gz         # Speech index (+ .feather)

metadata/
├── {METADATA_VERSION}/         # Source metadata files
└── riksprot_metadata.{METADATA_VERSION}.db  # Metadata SQLite database

opts/
├── config_{CORPUS_VERSION}_{METADATA_VERSION}.yml
├── tagged-speeches/*.yml       # Speech corpus options
├── plain-text-speeches/*.yml   # Text corpus options
└── dtm/*.yml                   # DTM generation options
```

## CWB Corpus Details

The generated CWB corpus includes:

**Positional attributes:**
- `lemma` - Lemmatized word forms
- `pos` - Universal POS tags
- `xpos` - Language-specific POS tags

**Structural attributes:**
- `year` - Year (with `year`, `title`)
- `protocol` - Protocol document (with `title`, `date`, `chamber`)
- `speech` - Individual speech (with `id`, `title`, `who`, `date`, `party_id`, `gender_id`, `office_type_id`, `sub_office_type_id`, `name`, `page_number`)

**Registry naming:**
- Registry entry: `riksprot_{PROJECT_NAME}_{CORPUS_VERSION}` (normalized)
- Corpus name: Uppercase version of registry entry
- Example: `RIKSPROT_5FILES_V141`

## Example Workflows

### Quick Test Dataset (5 files)
```bash
cd 5files
make info        # Verify configuration
make all         # Generate complete dataset with CWB corpus
```

### Large Dataset from Global
```bash
# .env with PARLACLARIN_MODE=copy, METADATA_MODE=copy, etc.
make dataset     # Copy and process from GLOBAL_CORPUS_FOLDER
make vrt-data    # Generate VRT
make cwb-data    # Create CWB corpus
```

### Custom Protocol Subset
```bash
# Create protocols.txt with desired protocol IDs
# .env with PARLACLARIN_MODE=protocols
make parlaclarin-corpus
make metadata
make tag-protocols
make speech-index
```

## Notes

- **Global folder**: `GLOBAL_CORPUS_FOLDER` contains riksdagen-records
- **Parallel builds**: Set `BUILD_TYPE=sequential` or `BUILD_TYPE=parallel` for speech corpora
- **Config generation**: `make-config` utility generates YAML from .env + defaults
- **Speech index**: Used by Swedeb API for fast lookups (Feather format preferred)
- **CWB encoding**: Uses UTF-8, with options `-sxBC9` for size optimization

## Troubleshooting

**CWB tools not found:**
```bash
make tools  # Display installation instructions
```

**Config errors:**
```bash
make config  # Regenerate config file
make info    # Verify environment variables
```

**Metadata issues:**
```bash
make reset-metadata-folder  # Clear and regenerate
make metadata               # Rebuild database
```

**CWB corpus errors:**
```bash
make cwb-info              # Check registry configuration
cwb-describe-corpus -r ./v1.4.1/registry RIKSPROT_5FILES_V141
```

## Related Documentation

- ParlaCLARIN format: Swedish parliamentary XML standard
- CWB documentation: Corpus Workbench encoding guide
- Pyriksprot: `pyriksprot` package for protocol processing
- Swedeb API: Uses generated CWB corpora and speech indices
