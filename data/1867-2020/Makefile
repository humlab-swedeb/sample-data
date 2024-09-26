ifndef PROJECT_NAME
PROJECT_NAME :=  $(shell basename $(dir $(abspath $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST)))))
endif

include .env

SHELL := /bin/bash

DATA_FOLDER=.
PREFERE_COPY=yes
SKIP_SUBSETTING=yes
GLOBAL_FOLDER=/data/riksdagen_corpus_data
GLOBAL_CORPUS_FOLDER=$(GLOBAL_FOLDER)/riksdagen-records/data

ifndef SWEDEB_TAG
$(error environment variable SWEDEB_TAG is undefined)
endif

ifndef CWB_REGISTRY_FOLDER
CWB_REGISTRY_FOLDER=/usr/local/share/cwb/registry
endif

all: dataset vrt-data cwb-data cwb-data-manual-compress

dataset: parlaclarin-corpus word-frequencies tag-protocols tagged-speech-corpora text-corpora dtm-corpora

parlaclarin-corpus:
	@echo "info: generating parlaclarin & metadata..."
	@echo "   target: $(SWEDEB_TAG)/parlaclarin"
	@echo "   script: pyriksprot.scripts.subset-corpus:main"
	@if [ "$(SKIP_SUBSETTING)" == "yes" ] ; then \
		echo "info: skipping subsetting...copying data..." ; \
		rm -rf $(SWEDEB_TAG)/parlaclarin ;  \
		mkdir -p $(SWEDEB_TAG)/parlaclarin/protocols ;  \
		cp -r $(GLOBAL_CORPUS_FOLDER)/* $(SWEDEB_TAG)/parlaclarin/protocols/ ; \
		cp -r $(GLOBAL_FOLDER)/metadata/$(SWEDEB_TAG) $(SWEDEB_TAG)/parlaclarin/metadata ; \
		cp -f  $(GLOBAL_FOLDER)/metadata/riksprot_metadata.$(SWEDEB_TAG).db $(SWEDEB_TAG)/riksprot_metadata.db ; \
	else \
		subset-corpus ./opts/subset-config.yml ./protocols.txt ./v1.1.0 --skip-download ; \
	fi

word-frequencies:
	@echo "info: generating word frequencies..."
	@echo "   script: pyriksprot.scripts.riksprot2tfs:main"
	@echo "   source: $(SWEDEB_TAG)/parlaclarin"
	@echo "   target: $(SWEDEB_TAG)/dehyphen/word-frequencies.pkl"
	@mkdir -p $(SWEDEB_TAG)/dehyphen
	@if [ "$(SKIP_SUBSETTING)" == "yes" ] ; then \
		cp -r $(GLOBAL_FOLDER)/$(SWEDEB_TAG)/dehyphen/word-frequencies.pkl $(SWEDEB_TAG)/dehyphen/word-frequencies.pkl ; \
	else \
		riksprot2tfs $(SWEDEB_TAG)/parlaclarin $(SWEDEB_TAG)/dehyphen/word-frequencies.pkl ; \
	fi

tag-protocols:
	@echo "info: generating tagged frames (VRT) corpus..."
	@echo "   script: pyriksprot_tagger.scripts.tag:main"
	@echo "   target: $(SWEDEB_TAG)/tagged_frames"
	@if [ "$(PREFERE_COPY)" == "yes" ] ; then \
		if [ "$(SKIP_SUBSETTING)" == "yes" ] ; then \
			cp -r $(GLOBAL_FOLDER)/$(SWEDEB_TAG)/tagged_frames $(SWEDEB_TAG)/tagged_frames ; \
		else \
			subset-vrt-corpus /data/riksdagen_corpus_data/$(SWEDEB_TAG)/tagged_frames \
				$(SWEDEB_TAG)/parlaclarin/protocols $(SWEDEB_TAG)/tagged_frames ; \
		fi \
	else \
		pos_tag opts/tagger-config.yml $(SWEDEB_TAG)/parlaclarin/protocols $(SWEDEB_TAG)/tagged_frames ; \
	fi

tagged-speech-corpora: ./opts/tagged-speeches/*.yml
	@echo "info: generating tagged speeches corpora..."
	@echo "   script: pyriksprot.scripts.riksprot2speech:main"
	@echo "   source: $(SWEDEB_TAG)/parlaclarin/protocols"
	@rm -rf $(SWEDEB_TAG)/speeches && mkdir -p $(SWEDEB_TAG)/speeches
	@for file in $^ ; do \
		echo "    target: $(SWEDEB_TAG)/speeches/$$(basename $${file%.yml})" ; \
		echo "   options: $${file}" ; \
		riksprot2speech \
			--options-filename $${file} --force \
			$(SWEDEB_TAG)/tagged_frames \
				$(SWEDEB_TAG)/riksprot_metadata.db \
					$(SWEDEB_TAG)/speeches/$$(basename $${file%.yml}) ; \
	done

text-corpora: ./opts/plain-text-speeches/*.yml
	@echo "info: generating text speech corpora..."
	@echo "   script: pyriksprot.scripts.riksprot2speech_text:main"
	@echo "   source: $(SWEDEB_TAG)/parlaclarin/protocols"
	@mkdir -p $(SWEDEB_TAG)/speeches
	@for file in $^ ; do \
		echo "   target: $(SWEDEB_TAG)/speeches/$$(basename $${file%.yml})" ; \
		echo "  options: $${file}" ; \
		riksprot2speech_text \
			--options-filename $${file} --force \
			$(SWEDEB_TAG)/parlaclarin/protocols \
				$(SWEDEB_TAG)/riksprot_metadata.db \
					$(SWEDEB_TAG)/speeches/$$(basename $${file%.yml}).zip ; \
	done

dtm-corpora: ./opts/dtm/*.yml
	@echo "info: generating DTM corpora..."
	@echo "note: humlab-penelope (vectorize-id) must be installed in current environment"
	@echo "   script: penelope.vectorize-id"
	@echo "   source: $(SWEDEB_TAG)/speeches/tagged_frames_speeches_$${tag}.feather"
	@rm -rf $(SWEDEB_TAG)/dtm && mkdir -p $(SWEDEB_TAG)/dtm
	@for file in $^ ; do \
	 	tag=$$(basename $${file%.yml}) ; \
		echo "   target: $(SWEDEB_TAG)/dtm/$${tag}" ; \
		echo "  options: $${file}" ; \
		vectorize-id \
		    --create-subfolder \
			--options-filename $${file} \
			--corpus-source $(SWEDEB_TAG)/speeches/tagged_frames_speeches_$${tag}.feather \
			--output-folder $(SWEDEB_TAG)/dtm \
			--output-tag $${tag} ; \
	done

vrt-data:
	@echo "info: generating CWB extended VRT corpora..."
	@echo "   script: riksprot2vrt"
	@echo "   source: $(SWEDEB_TAG)/tagged_frames"
	@echo "   target: $(SWEDEB_TAG)/vrt"
	@riksprot2vrt \
		--source-folder $(SWEDEB_TAG)/tagged_frames \
		--target-folder $(SWEDEB_TAG)/vrt \
		--metadata-filename $(SWEDEB_TAG)/riksprot_metadata.db \
		--merge-strategy chain \
		--structural-tag protocol \
		--structural-tag speech \
		--batch-tag year


ifndef CWB_REGISTRY_ENTRY
# use the project name to create a CWB registry entry name (lowercase)
LOWER_PROJECT_NAME := $(shell X="$(PROJECT_NAME)"; echo $${X^^^})
CWB_REGISTRY_ENTRY := riksprot_$(LOWER_PROJECT_NAME)_$(SWEDEB_TAG)
CWB_REGISTRY_ENTRY := $(subst .,,$(CWB_REGISTRY_ENTRY))
CWB_REGISTRY_ENTRY := $(subst -,_,$(CWB_REGISTRY_ENTRY))
endif

CWB_CORPUS_NAME := $(shell X="${CWB_REGISTRY_ENTRY}"; echo $${X^^})
CWB_TARGET_FOLDER=`pwd`/$(SWEDEB_TAG)/cwb

cwb-make-exists = $(if $(shell which cwb-make 2> /dev/null),true,false)

.PHONY: cwb-info
cwb-info:
	@echo "      Project: $(PROJECT_NAME)"
	@echo "     Registry: $(CWB_TARGET_FOLDER)"
	@echo "   Entry name: $(CWB_REGISTRY_ENTRY)"
	@echo "  Corpus name: $(CWB_CORPUS_NAME)"
	@echo "Target folder: $(CWB_TARGET_FOLDER)"
	@cwb-describe-corpus $(CWB_CORPUS_NAME)

.PHONY: cwb-data
cwb-data:
	@echo "info: generating CWB extended VRT corpora..."
	@echo "   script: cwb-encode"
	@echo "   source: $(SWEDEB_TAG)/vrt"
	@echo "   target: $(SWEDEB_TAG)/cwb"
	@echo "   CWB name: $(CWB_REGISTRY_ENTRY)"
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
