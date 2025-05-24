
include .env
include ../Makefile

DATA_FOLDER=.
PARLACLARIN_MODE=copy
METADATA_MODE=create
TAGGING_MODE=tag
WORD_FREQUENCY_MODE=create

dataset-temp: word-frequencies tagged-speech-corpora text-corpora dtm-corpora

copy-swedeb-global:
	@echo "info: copying global data..."
	@echo "info:    source: $(SWEDEB_TAG)"
	@echo "info:    target: /data/swedeb/$(SWEDEB_TAG)"
	@rm -rf /data/swedeb/$(SWEDEB_TAG)
	@cp -r $(SWEDEB_TAG) /data/swedeb/ 
	@ln -s /data/swedeb/$(SWEDEB_TAG)/dehyphen /data/swedeb/$(SWEDEB_TAG)/dehyphen_datadir
	@ln -s /data/swedeb/$(SWEDEB_TAG)/riksprot_metadata.db /data/swedeb/$(SWEDEB_TAG)/riksprot_metadata.$(SWEDEB_TAG).db
