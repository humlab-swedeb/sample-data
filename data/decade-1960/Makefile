include .env

SHELL := /bin/bash

DATA_FOLDER=.
PREFERE_COPY=yes

all: dataset vrt-data cwb-data cwb-data-manual-compress

dataset: parlaclarin-corpus word-frequencies tag-protocols tagged-speech-corpora text-corpora dtm-corpora

parlaclarin-corpus:
	@echo "Target(s): subset of Parla-CLARIN corpus and processed metadata"
	@echo "Script(s): pyriksprot.scripts.subset-corpus:main"
	@subset-corpus ./protocols.txt ./ $(SWEDEB_TAG) --source-folder /data/riksdagen_corpus_data/riksdagen-corpus

word-frequencies:
	@echo "Target(s): global term frequencies (TF)"
	@echo "Script(s): pyriksprot.scripts.riksprot2tfs:main"
	@mkdir -p $(SWEDEB_TAG)/dehyphen_datadir
	@riksprot2tfs $(SWEDEB_TAG)/parlaclarin $(SWEDEB_TAG)/dehyphen_datadir/word-frequencies.pkl

tag-protocols:
	@echo "Target(s): tagged parlaclarin protocols (tagged frames)"
	@echo "Script(s): pyriksprot_tagger.scripts.tag:main"
ifeq ($(PREFERE_COPY),yes)
	@subset-vrt-corpus /data/riksdagen_corpus_data/$(SWEDEB_TAG)/corpus/tagged_frames $(SWEDEB_TAG)/parlaclarin/protocols $(SWEDEB_TAG)/tagged_frames
else
	@pos_tag opts/tagger-config.yml $(SWEDEB_TAG)/parlaclarin/protocols $(SWEDEB_TAG)/tagged_frames
endif

tagged-speech-corpora: ./opts/tagged-speeches/*.yml
	@echo "Target(s): tagged speech corpora (tagged frames)"
	@echo "Script(s): pyriksprot.scripts.riksprot2speech:main"
	@rm -rf $(SWEDEB_TAG)/speeches && mkdir -p $(SWEDEB_TAG)/speeches
	@for file in $^ ; do \
		echo " => $(SWEDEB_TAG)/speeches/$$(basename $${file%.yml})" ; \
		riksprot2speech \
			--options-filename $${file} --force \
			$(SWEDEB_TAG)/tagged_frames \
				$(SWEDEB_TAG)/riksprot_metadata.db \
					$(SWEDEB_TAG)/speeches/$$(basename $${file%.yml}) ; \
    done

text-corpora: ./opts/plain-text-speeches/*.yml
	@echo "Target(s): speech text corpora (plain text)"
	@echo "Script(s): pyriksprot.scripts.riksprot2speech_text:main"
	@mkdir -p $(SWEDEB_TAG)/speeches
	@for file in $^ ; do \
		echo " => $(SWEDEB_TAG)/speeches/$$(basename $${file%.yml})" ; \
		riksprot2speech_text \
			--options-filename $${file} --force \
			$(SWEDEB_TAG)/parlaclarin/protocols \
				$(SWEDEB_TAG)/riksprot_metadata.db \
					$(SWEDEB_TAG)/speeches/$$(basename $${file%.yml}).zip ; \
    done

dtm-corpora: ./opts/dtm/*.yml
	@echo "Target(s): DTM corpora"
	@echo "Script(s): penelope.vectorize-id"
	@echo "     Note: penelope must be installed in current environment"
	@rm -rf $(SWEDEB_TAG)/dtm && mkdir -p $(SWEDEB_TAG)/dtm
	@for file in $^ ; do \
	 	tag=$$(basename $${file%.yml}) ; \
		echo " => $(SWEDEB_TAG)/speeches/$${tag}" ; \
		vectorize-id \
		    --create-subfolder \
			--options-filename $${file} \
			--corpus-source $(SWEDEB_TAG)/speeches/tagged_frames_speeches_$${tag}.feather \
			--output-folder $(SWEDEB_TAG)/dtm \
			--output-tag $${tag} ; \
    done

vrt-data:
	@riksprot2vrt \
		--source-folder $(SWEDEB_TAG)/tagged_frames \
		--target-folder $(SWEDEB_TAG)/vrt \
		--metadata-filename $(SWEDEB_TAG)/riksprot_metadata.db \
		--merge-strategy chain \
		--structural-tag protocol \
		--structural-tag speech \
		--batch-tag year

CWB_REGISTRY_FOLDER=/usr/local/share/cwb/registry
CWB_TARGET_FOLDER=`pwd`/$(SWEDEB_TAG)/cwb
CWB_REGISTRY_ENTRY := riksprot_$(subst .,,$(SWEDEB_TAG))_test
CWB_CORPUS_NAME := $(shell X="${CWB_REGISTRY_ENTRY}"; echo $${X^^})

cwb-make-exists = $(if $(shell which cwb-make 2> /dev/null),true,false)

.PHONY: cwb-info
cwb-info:
	@echo "     Registry: $(CWB_REGISTRY_ENTRY)"
	@echo "  Corpus name: $(CWB_CORPUS_NAME)"
	@echo "Target folder: $(CWB_TARGET_FOLDER)"
	@cwb-describe-corpus $(CWB_CORPUS_NAME)

.PHONY: cwb-data
cwb-data:
	@rm -rf $(CWB_TARGET_FOLDER) && mkdir -p $(CWB_TARGET_FOLDER)
	@cwb-encode -d $(CWB_TARGET_FOLDER) -sxBC9 -c utf8 \
		-F `pwd`/$(SWEDEB_TAG)/vrt \
		-R $(CWB_REGISTRY_FOLDER)/$(CWB_REGISTRY_ENTRY) \
		-P lemma -P pos -P xpos \
		-S year:0+year+title \
		-S protocol:0+title+date \
		-S speech:0+id+title+who+date+party_id+gender_id+office_type_id+sub_office_type_id+name+page_number
	@if [ "$(cwb-make-exists)" == "true" ]; then \
		cwb-make -V $(CWB_CORPUS_NAME); \
	else \
		echo "info: cwb-make not found, skipping corpus creation"; \
		echo "info: run 'sudo cpan install CWB' to install the CWB/Perl toolkit" ; \
	fi
	@cwb-describe-corpus $(CWB_CORPUS_NAME)
	@echo "FIXME: Check that compression is working!!! (and cwv-buffcode and cwb-compress-rdx are executed)"

cwb-data-manual-compress:
	@echo "info: compressing CWB $(CWB_CORPUS_NAME) manually"
	@cwb-makeall -V $(CWB_CORPUS_NAME);
	@echo rm $(cwb-huffcode -A $(CWB_CORPUS_NAME) | grep "You can delete" | cut -d '<' -f2 | cut -d '>' -f1)
	@echo rm $(cwb-compress-rdx -A $(CWB_CORPUS_NAME) | grep "You can delete" | cut -d '<' -f2 | cut -d '>' -f1)
