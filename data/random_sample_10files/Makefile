ifndef PROJECT_NAME
PROJECT_NAME :=  $(shell basename $(dir $(abspath $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST)))))
endif

include .env

SHELL := /bin/bash

DATA_FOLDER=.
PARLACLARIN_MODE=subset
METADATA_MODE=create
TAGGING_MODE=skip
WORD_FREQUENCY_MODE=create
GLOBAL_FOLDER=/data/riksdagen_corpus_data
GLOBAL_CORPUS_FOLDER=$(GLOBAL_FOLDER)/riksdagen-records/data

ifndef SWEDEB_TAG
$(error environment variable SWEDEB_TAG is undefined)
endif

ifndef CWB_REGISTRY_FOLDER
CWB_REGISTRY_FOLDER=/usr/local/share/cwb/registry
endif

all: dataset vrt-data cwb-data cwb-data-manual-compress

dataset: parlaclarin-corpus metadata word-frequencies tag-protocols tagged-speech-corpora text-corpora dtm-corpora

dataset-temp: word-frequencies tagged-speech-corpora text-corpora dtm-corpora

parlaclarin-corpus:
	@echo "info: generating parlaclarin & metadata..."
	@echo "info:    target: $(SWEDEB_TAG)/parlaclarin"
	@echo "info:    script: pyriksprot.scripts.subset-corpus:main"
	@echo "info:      mode: $(PARLACLARIN_MODE)"
	@if [ "$(PARLACLARIN_MODE)" == "copy" ] ; then \
		echo "info: copying global data..." ; \
		rm -rf $(SWEDEB_TAG)/parlaclarin ;  \
		mkdir -p $(SWEDEB_TAG)/parlaclarin/protocols ;  \
		cp -r $(GLOBAL_CORPUS_FOLDER)/* $(SWEDEB_TAG)/parlaclarin/protocols/ ; \
	elif [ "$(PARLACLARIN_MODE)" == "subset" ] ; then \
		subset-corpus ./opts/subset-config.yml ./protocols.txt . --skip-download ; \
	elif [ "$(PARLACLARIN_MODE)" == "skip" ] ; then \
		echo "info: skipping protocols update..." ; \
	else \
		echo "error: unknown PARLACLARIN_MODE $(PARLACLARIN_MODE) " ; \
		exit 64 ; \
	fi

metadata:
	@echo "info: generating metadata..."
	@echo "info:    script: pyriksprot.scripts.riksprot2metadata:main"
	@echo "info:    source: $(SWEDEB_TAG)/parlaclarin/protocols"
	@echo "info:    target: $(SWEDEB_TAG)/riksprot_metadata.db"
	@echo "info:      mode: $(METADATA_MODE)"
	@if [ "$(PARLACLARIN_MODE)" == "subset" ] ; then \
	    echo "info: skipping metadata (created in subset-corpus call)..." ; \
	elif [ "$(METADATA_MODE)" == "copy" ] ; then \
		\
		echo "info: copying global data..." ; \
		rm -rf $(SWEDEB_TAG)/parlaclarin/metadata ;  \
		mkdir -p $(SWEDEB_TAG)/parlaclarin ;  \
		cp -r $(GLOBAL_FOLDER)/metadata/$(SWEDEB_TAG) $(SWEDEB_TAG)/parlaclarin/metadata ; \
		cp -f  $(GLOBAL_FOLDER)/metadata/riksprot_metadata.$(SWEDEB_TAG).db $(SWEDEB_TAG)/riksprot_metadata.db ; \
		\
	elif [ "$(METADATA_MODE)" == "create" ] ; then \
		\
		echo "info: generating $(SWEDEB_TAG)/riksprot_metadata.db using source $(SWEDEB_TAG)/parlaclarin/metadata" ; \
		rm -f $(SWEDEB_TAG)/riksprot_metadata.db ; \
		metadata2db  database  \
			--target-filename=$(SWEDEB_TAG)/riksprot_metadata.db \
			--force \
			--source-folder=$(SWEDEB_TAG)/parlaclarin/metadata  opts/subset-config.yml ; \
		\
	elif [ "$(METADATA_MODE)" == "skip" ] ; then \
	    echo "info: skipping metadata..." ; \
	fi

word-frequencies:
	@echo "info: generating word frequencies..."
	@echo "info:    script: pyriksprot.scripts.riksprot2tfs:main"
	@echo "info:    source: $(SWEDEB_TAG)/parlaclarin"
	@echo "info:    target: $(SWEDEB_TAG)/dehyphen/word-frequencies.pkl"
	@echo "info:      mode: $(WORD_FREQUENCY_MODE)"
	@mkdir -p $(SWEDEB_TAG)/dehyphen
	@if [ "$(WORD_FREQUENCY_MODE)" == "copy" ] ; then \
		cp -r $(GLOBAL_FOLDER)/$(SWEDEB_TAG)/dehyphen/word-frequencies.pkl $(SWEDEB_TAG)/dehyphen/word-frequencies.pkl ; \
	elif [ "$(WORD_FREQUENCY_MODE)" == "create" ] ; then \
		subset-corpus ./opts/subset-config.yml ./protocols.txt . --skip-download ; \
		riksprot2tfs $(SWEDEB_TAG)/parlaclarin $(SWEDEB_TAG)/dehyphen/word-frequencies.pkl ; \
	elif [ "$(WORD_FREQUENCY_MODE)" == "skip" ] ; then \
		echo "info: skipping word frequency generation " ; \
	else \
		echo "error: unknown WORD_FREQUENCY_MODE $(WORD_FREQUENCY_MODE) " ; \
		exit 64 ; \
	fi

tag-protocols:
	@echo "info: generating tagged frames (VRT) corpus..."
	@echo "info:    script: pyriksprot_tagger.scripts.tag:main"
	@echo "info:    target: $(SWEDEB_TAG)/tagged_frames"
	@echo "info:      mode: $(TAGGING_MODE)"
	@if [ "$(TAGGING_MODE)" == "skip" ] ; then \
		echo "info: skipping tagging" ; \
	 elif [ "$(TAGGING_MODE)" == "copy" ] ; then \
		rm -rf $(SWEDEB_TAG)/tagged_frames ; \
		cp -r $(GLOBAL_FOLDER)/$(SWEDEB_TAG)/tagged_frames $(SWEDEB_TAG)/tagged_frames ; \
	 elif [ "$(TAGGING_MODE)" == "subset" ] ; then \
		subset-vrt-corpus /data/riksdagen_corpus_data/$(SWEDEB_TAG)/tagged_frames \
			$(SWEDEB_TAG)/parlaclarin/protocols $(SWEDEB_TAG)/tagged_frames ; \
	 elif [ "$(TAGGING_MODE)" == "tag" ] ; then \
		rm -rf $(SWEDEB_TAG)/tagged_frames ; \
		pos_tag opts/tagger-config.yml $(SWEDEB_TAG)/parlaclarin/protocols $(SWEDEB_TAG)/tagged_frames ; \
	 else \
		echo "error: uknown tagging mode $(TAGGING_MODE) " ; \
		exit 64 ; \
	 fi

tagged-speech-corpora: ./opts/tagged-speeches/*.yml
	@echo "info: generating tagged speeches corpora..."
	@echo "info:    script: pyriksprot.scripts.riksprot2speech:main"
	@echo "info:    source: $(SWEDEB_TAG)/parlaclarin/protocols"
	@for file in $^ ; do \
		echo "info:     target: $(SWEDEB_TAG)/speeches/$$(basename $${file%.yml})" ; \
		echo "info:    options: $${file}" ; \
		riksprot2speech \
			--options-filename $${file} --force \
			$(SWEDEB_TAG)/tagged_frames \
				$(SWEDEB_TAG)/riksprot_metadata.db \
					$(SWEDEB_TAG)/speeches/$$(basename $${file%.yml}) ; \
	done

text-corpora: ./opts/plain-text-speeches/*.yml
	@echo "info: generating text speech corpora..."
	@echo "info:    script: pyriksprot.scripts.riksprot2speech_text:main"
	@echo "info:    source: $(SWEDEB_TAG)/parlaclarin/protocols"
	@mkdir -p $(SWEDEB_TAG)/speeches
	@for file in $^ ; do \
		echo "info:    target: $(SWEDEB_TAG)/speeches/$$(basename $${file%.yml})" ; \
		echo "info:   options: $${file}" ; \
		riksprot2speech_text \
			--options-filename $${file} --force \
			$(SWEDEB_TAG)/parlaclarin/protocols \
				$(SWEDEB_TAG)/riksprot_metadata.db \
					$(SWEDEB_TAG)/speeches/$$(basename $${file%.yml}).zip ; \
	done

dtm-corpora: ./opts/dtm/*.yml
	@echo "info: generating DTM corpora..."
	@echo "note: humlab-penelope (vectorize-id) must be installed in current environment"
	@echo "info:    script: penelope.vectorize-id"
	@echo "info:    source: $(SWEDEB_TAG)/speeches/tagged_frames_speeches_$${tag}.feather"
	@rm -rf $(SWEDEB_TAG)/dtm && mkdir -p $(SWEDEB_TAG)/dtm
	@for file in $^ ; do \
	 	tag=$$(basename $${file%.yml}) ; \
		echo "info:    target: $(SWEDEB_TAG)/dtm/$${tag}" ; \
		echo "info:   options: $${file}" ; \
		vectorize-id \
		    --create-subfolder \
			--options-filename $${file} \
			--corpus-source $(SWEDEB_TAG)/speeches/tagged_frames_speeches_$${tag}.feather \
			--output-folder $(SWEDEB_TAG)/dtm \
			--output-tag $${tag} ; \
	done

vrt-data:
	@echo "info: generating CWB extended VRT corpora..."
	@echo "info:    script: riksprot2vrt"
	@echo "info:    source: $(SWEDEB_TAG)/tagged_frames"
	@echo "info:    target: $(SWEDEB_TAG)/vrt"
	@rm -rf $(SWEDEB_TAG)/vrt && mkdir -p $(SWEDEB_TAG)/vrt
	@riksprot2vrt \
		--source-folder $(SWEDEB_TAG)/tagged_frames \
		--target-folder $(SWEDEB_TAG)/vrt \
		--metadata-filename $(SWEDEB_TAG)/riksprot_metadata.db \
		--merge-strategy chain \
		--structural-tag protocol \
		--structural-tag speech \
		--batch-tag year

copy-swedeb-global:
	@echo "info: copying global data..."
	@echo "info:    source: $(SWEDEB_TAG)"
	@echo "info:    target: /data/swedeb/$(SWEDEB_TAG)"
	@rm -rf /data/swedeb/random_sample_10files
	@cp -r ../random_sample_10files /data/swedeb/random_sample_10files


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
	@echo "     Registry: $(CWB_REGISTRY_FOLDER)"
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
	@if [ ! -d "$(CWB_REGISTRY_FOLDER)" ] ; then \
		mkdir -p $(CWB_REGISTRY_FOLDER) ; \
	fi
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
	@if [ ! -f "$(SWEDEB_TAG)/registry/$(CWB_REGISTRY_ENTRY)" ] ; then \
		mkdir -p $(SWEDEB_TAG)/registry ; \
		cp $(CWB_REGISTRY_FOLDER)/$(CWB_REGISTRY_ENTRY) $(SWEDEB_TAG)/registry/$(CWB_REGISTRY_ENTRY) ; \
	fi

cwb-data-manual-compress:
	@echo "info: compressing CWB $(CWB_CORPUS_NAME) manually"
	@cwb-makeall -V $(CWB_CORPUS_NAME);
	@echo rm $(cwb-huffcode -A $(CWB_CORPUS_NAME) | grep "You can delete" | cut -d '<' -f2 | cut -d '>' -f1)
	@echo rm $(cwb-compress-rdx -A $(CWB_CORPUS_NAME) | grep "You can delete" | cut -d '<' -f2 | cut -d '>' -f1)
