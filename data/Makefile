# 
SHELL := /bin/bash

# include env from current working folder (i.e. from which this Makefile is included)

# DATA_FOLDER=.
# PARLACLARIN_MODE=skip
# TAGGING_MODE=skip
# WORD_FREQUENCY_MODE=skip

include $(shell pwd)/.env

GLOBAL_FOLDER=/data/riksdagen_corpus_data
GLOBAL_CORPUS_FOLDER=$(GLOBAL_FOLDER)/riksdagen-records

ifndef CORPUS_VERSION
$(error environment variable CORPUS_VERSION must be defined in .env)
endif

ifndef METADATA_VERSION
$(error environment variable METADATA_VERSION must be defined in .env)
endif

ifndef PROJECT_NAME
PROJECT_NAME :=  $(shell basename $(dir $(abspath $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST)))))
endif

ifndef CWB_REGISTRY_FOLDER
CWB_REGISTRY_FOLDER=/usr/local/share/cwb/registry
endif

ifndef CWB_REGISTRY_ENTRY
# use the project name to create a CWB registry entry name (lowercase)
LOWER_PROJECT_NAME := $(shell X="$(PROJECT_NAME)"; echo $${X^^^})
CWB_REGISTRY_ENTRY := riksprot_$(LOWER_PROJECT_NAME)_$(CORPUS_VERSION)
CWB_REGISTRY_ENTRY := $(subst .,,$(CWB_REGISTRY_ENTRY))
CWB_REGISTRY_ENTRY := $(subst -,_,$(CWB_REGISTRY_ENTRY))
endif

CWB_CORPUS_NAME := $(shell X="${CWB_REGISTRY_ENTRY}"; echo $${X^^})
CWB_TARGET_FOLDER=`pwd`/$(CORPUS_VERSION)/cwb

.PHONY: dataset dataset-temp parlaclarin-corpus metadata speech-index word-frequencies tag-protocols tagged-speech-corpora text-corpora
.PHONY: dtm-corpora vrt-data copy-swedeb-global cwb-data cwb-data-manual-compress cwb-info clean

CONFIG_FILENAME=opts/config_$(CORPUS_VERSION)_$(METADATA_VERSION).yml
CORPUS_FOLDER=$(CORPUS_VERSION)/riksdagen-records
METADATA_FILENAME=metadata/riksprot_metadata.$(METADATA_VERSION).db

info:
	@echo "info: generating $(CORPUS_VERSION) data"
	@echo "info:    project:                 $(PROJECT_NAME)"
	@echo "info:    corpus version:          $(CORPUS_VERSION)"
	@echo "info:    global corpus folder:    $(GLOBAL_CORPUS_FOLDER)"
	@echo "info:    corpus folder:           $(CORPUS_FOLDER)"
	@echo "info:    metadata version:        $(METADATA_VERSION)"
	@echo "info:    metadata filename:       $(METADATA_FILENAME)"
	@echo "info:    config filename:         $(CONFIG_FILENAME)"
	@echo "info:    parlaclarin mode:        $(PARLACLARIN_MODE)"
	@echo "info:    metadata mode:           $(METADATA_MODE)"
	@echo "info:    tagging mode:            $(TAGGING_MODE)"
	@echo "info:    word frequency mode:     $(WORD_FREQUENCY_MODE)"
	@echo "info:    CWB registry folder:     $(CWB_REGISTRY_FOLDER)"
	@echo "info:    CWB registry entry name: $(CWB_REGISTRY_ENTRY)"
	@echo "info:    CWB corpus name:         $(CWB_CORPUS_NAME)"
	@echo "info:    CWB target folder:       $(CWB_TARGET_FOLDER)"


all: dataset vrt-data cwb-data cwb-data-manual-compress

dataset: parlaclarin-corpus metadata speech-index word-frequencies tag-protocols tagged-speech-corpora text-corpora dtm-corpora

config: $(CONFIG_FILENAME)
	@echo "info: config file $(CONFIG_FILENAME) generated"

apa:
	@make-config --help

clean:
	@rm -rf $(CORPUS_VERSION)

reset-corpus-folder:
	@mkdir -p $(CORPUS_FOLDER) && rm -rf $(CORPUS_FOLDER)

reset-metadata-folder:
	@rm -rf metadata/$(METADATA_VERSION)
	@perl -MCWB -e 'print $CWB::VERSION,"\n"'

rsync-to-global:
	@echo "info: syncing $(CORPUS_VERSION) /data/swedeb/$(CORPUS_VERSION)/"
	@rsync -av --delete $(CORPUS_VERSION)/ /data/swedeb/$(CORPUS_VERSION)/
	@rsync -av --delete metadata/$(METADATA_VERSION)/ /data/swedeb/metadata/$(METADATA_VERSION)/
	@rsync -av --delete $(METADATA_FILENAME) /data/swedeb/$(METADATA_FILENAME)

tools:
	@echo "info: install CWB Core:"
	@echo " wget -O cwb-3.5.0-src.tar.gz https://master.dl.sourceforge.net/project/cwb/cwb/cwb-3.5/source/cwb-3.5.0-src.tar.gz?viasf=1" 
	@echo " tar xvf cwb-3.5.0-src.tar.gz"
	@echo " cd cwb-3.5.0-src"
	@echo " sudo ./install-scripts/install-linux"
	@echo "info: install CWB/Perl toolkit:"
	@echo " curl -L https://cpanmin.us | perl - --sudo App::cpanminus' to install cpanminus"
	@echo " sudo cpan install CWB"

####################################################################################################
# Generate config file
####################################################################################################

$(CONFIG_FILENAME): .env
	@make-config \
		--corpus-version $(CORPUS_VERSION) \
		--metadata-version $(METADATA_VERSION) \
		--root-folder . \
		--corpus-folder $(CORPUS_FOLDER) \
		--stanza-datadir /data/sparv/models/stanza $(CONFIG_FILENAME)

parlaclarin-corpus: reset-corpus-folder
	@echo "info: generating parlaclarin & metadata..."
	@echo "info:    target: $(CORPUS_FOLDER)"
	@echo "info:    script: pyriksprot.scripts.subset-corpus:main"
	@echo "info:      mode: $(PARLACLARIN_MODE)"
	@if [ "$(PARLACLARIN_MODE)" == "copy" ] ; then \
		echo "info: copying global data..." ; \
		rm -rf $(CORPUS_FOLDER) ;  \
		mkdir -p $(CORPUS_FOLDER) ;  \
		cp -r $(GLOBAL_CORPUS_FOLDER)/data/* $(CORPUS_FOLDER)/ ; \
		for file in $(CORPUS_VERSION)/riksdagen-records/* ; do \
			echo "info:    copied: $${file}" ; \
		done ; \
	elif [ "$(PARLACLARIN_MODE)" == "protocols" ] ; then \
		../../bin/cp-protocols --config-filename $(CONFIG_FILENAME) --protocols ./protocols.txt ; \
	elif [ "$(PARLACLARIN_MODE)" == "subset" ] ; then \
		subset-corpus $(CONFIG_FILENAME) ./protocols.txt . --skip-download ; \
	elif [ "$(PARLACLARIN_MODE)" == "skip" ] ; then \
		echo "info: skipping protocols update..." ; \
	else \
		echo "error: unknown PARLACLARIN_MODE $(PARLACLARIN_MODE) " ; \
		exit 64 ; \
	fi

metadata: reset-metadata-folder $(CONFIG_FILENAME)
	@echo "info: generating metadata..."
	@echo "info:    script: pyriksprot.scripts.riksprot2metadata:main"
	@echo "info:    corpus: $(CORPUS_FOLDER)"
	@echo "info:    source: metadata/$(METADATA_VERSION)"
	@echo "info:    target: $(METADATA_FILENAME)"
	@echo "info:      mode: $(METADATA_MODE)"
	@echo "info:    config: $(CONFIG_FILENAME)"
	@if [ "$(PARLACLARIN_MODE)" == "subset" ] ; then \
	    echo "info: skipping metadata (created in subset-corpus call)..." ; \
	elif [ "$(METADATA_MODE)" == "copy" ] ; then \
		\
		echo "info: copying global data..." ; \
		cp -r $(GLOBAL_FOLDER)/metadata/$(METADATA_VERSION) metadata/$(METADATA_VERSION) ; \
		cp -f  $(GLOBAL_FOLDER)/metadata/riksprot_metadata.$(METADATA_VERSION).db $(METADATA_FILENAME) ; \
		\
	elif [ "$(METADATA_MODE)" == "create" ] ; then \
		\
		echo "info: generating $(METADATA_FILENAME) using source metadata/$(METADATA_VERSION)" ; \
		rm -f $(METADATA_FILENAME) ; \
		metadata2db  database  \
			--target-filename=$(METADATA_FILENAME) \
			--force \
			--source-folder=metadata/$(METADATA_VERSION) \
			$(CONFIG_FILENAME) ; \
		\
	elif [ "$(METADATA_MODE)" == "skip" ] ; then \
	    echo "info: skipping metadata..." ; \
	fi

speech-index:
	@echo "info: creating default speech index..."
	@echo "info:    script: pyriksprot.scripts.riksprot2speech_index:main"
	@echo "info:    source: $(CORPUS_VERSION)/tagged_frames"
	@echo "info:    target: $(CORPUS_VERSION)/speech-index.csv.gz (and .feather)"
	@speech-index $(CORPUS_VERSION)/tagged_frames \
		$(CORPUS_VERSION)/speech-index.csv.gz \
		$(METADATA_FILENAME) \
		--multiproc-processes 4

metadata-refresh:
	@echo "info: creating new metadata db using existing data (no download, no index update)"
	@metadata2db database \
		--target-filename=$(METADATA_FILENAME) \
		--skip-create-index \
		--skip-download-metadata \
		--source-folder=metadata/$(METADATA_VERSION) \
		$(CONFIG_FILENAME) 

word-frequencies:
	@echo "info: generating word frequencies..."
	@echo "info:    script: pyriksprot.scripts.riksprot2tfs:main"
	@echo "info:    source: $(CORPUS_VERSION)/riksdagen-records"
	@echo "info:    target: $(CORPUS_VERSION)/dehyphen/word-frequencies.pkl"
	@echo "info:      mode: $(WORD_FREQUENCY_MODE)"
	@mkdir -p $(CORPUS_VERSION)/dehyphen
	@if [ "$(WORD_FREQUENCY_MODE)" == "copy" ] ; then \
		cp -r $(GLOBAL_FOLDER)/$(CORPUS_VERSION)/dehyphen/word-frequencies.pkl $(CORPUS_VERSION)/dehyphen/word-frequencies.pkl ; \
	elif [ "$(WORD_FREQUENCY_MODE)" == "create" ] ; then \
		echo "skipping: subset-corpus $(CONFIG_FILENAME) ./protocols.txt . --skip-download" ; \
		riksprot2tfs $(CORPUS_VERSION)/riksdagen-records $(CORPUS_VERSION)/dehyphen/word-frequencies.pkl ; \
	elif [ "$(WORD_FREQUENCY_MODE)" == "skip" ] ; then \
		echo "info: skipping word frequency generation " ; \
	else \
		echo "error: unknown WORD_FREQUENCY_MODE $(WORD_FREQUENCY_MODE) " ; \
		exit 64 ; \
	fi

tag-protocols:
	@echo "info: generating tagged frames (VRT) corpus..."
	@echo "info:    script: pyriksprot_tagger.scripts.tag:main"
	@echo "info:    config: $(CONFIG_FILENAME)"
	@echo "info:    source: $(CORPUS_VERSION)/riksdagen-records"
	@echo "info:    target: $(CORPUS_VERSION)/tagged_frames"
	@echo "info:      mode: $(TAGGING_MODE)"
	@if [ "$(TAGGING_MODE)" == "skip" ] ; then \
		echo "info: skipping tagging" ; \
	 elif [ "$(TAGGING_MODE)" == "copy" ] ; then \
		rm -rf $(CORPUS_VERSION)/tagged_frames ; \
		cp -r $(GLOBAL_FOLDER)/$(CORPUS_VERSION)/tagged_frames $(CORPUS_VERSION)/tagged_frames ; \
	 elif [ "$(TAGGING_MODE)" == "subset" ] ; then \
		subset-vrt-corpus $(GLOBAL_FOLDER)/$(CORPUS_VERSION)/tagged_frames \
			$(CORPUS_VERSION)/riksdagen-records $(CORPUS_VERSION)/tagged_frames ; \
	 elif [ "$(TAGGING_MODE)" == "tag" ] ; then \
		rm -rf $(CORPUS_VERSION)/tagged_frames ; \
		pos_tag --skip-version-check $(CONFIG_FILENAME) $(CORPUS_VERSION)/riksdagen-records $(CORPUS_VERSION)/tagged_frames ; \
	 else \
		echo "error: unknown tagging mode $(TAGGING_MODE) " ; \
		exit 64 ; \
	 fi

tagged-speech-corpora: ./opts/tagged-speeches/*.yml
	@echo "info: generating tagged speeches corpora..."
	@echo "info:    script: pyriksprot.scripts.riksprot2speech:main"
	@echo "info:    source: $(CORPUS_VERSION)/riksdagen-records"
	@rm -rf $(CORPUS_VERSION)/speeches && mkdir -p $(CORPUS_VERSION)/speeches
	@for file in $^ ; do \
		echo "info:     target: $(CORPUS_VERSION)/speeches/$$(basename $${file%.yml})" ; \
		echo "info:    options: $${file}" ; \
		riksprot2speech \
			--options-filename $${file} --force \
			$(CORPUS_VERSION)/tagged_frames \
				metadata/riksprot_metadata.${METADATA_VERSION}.db \
					$(CORPUS_VERSION)/speeches/$$(basename $${file%.yml}) ; \
	done

text-corpora: ./opts/plain-text-speeches/*.yml
	@echo "info: generating text speech corpora..."
	@echo "info:    script: pyriksprot.scripts.riksprot2speech_text:main"
	@echo "info:    source: $(CORPUS_VERSION)/riksdagen-records"
	@mkdir -p $(CORPUS_VERSION)/speeches
	@for file in $^ ; do \
		echo "info:    target: $(CORPUS_VERSION)/speeches/$$(basename $${file%.yml})" ; \
		echo "info:   options: $${file}" ; \
		riksprot2speech_text \
			--options-filename $${file} --force \
			$(CORPUS_VERSION)/riksdagen-records \
				metadata/riksprot_metadata.${METADATA_VERSION}.db \
					$(CORPUS_VERSION)/speeches/$$(basename $${file%.yml}).zip ; \
	done

dtm-corpora: ./opts/dtm/*.yml
	@echo "info: generating DTM corpora..."
	@echo "note: humlab-penelope (vectorize-id) must be installed in current environment"
	@echo "info:    script: penelope.vectorize-id"
	@mkdir -p $(CORPUS_VERSION)/dtm
	@for file in $^ ; do \
	 	tag=$$(basename $${file%.yml}) ; \
		echo "info:    source: $(CORPUS_VERSION)/speeches/tagged_frames_speeches_$${tag}.feather" \
		echo "info:    target: $(CORPUS_VERSION)/dtm/$${tag}" ; \
		echo "info:   options: $${file}" ; \
		rm -rf $(CORPUS_VERSION)/dtm/$${tag} ; \
		vectorize-id \
		    --create-subfolder \
			--options-filename $${file} \
			--corpus-source $(CORPUS_VERSION)/speeches/tagged_frames_speeches_$${tag}.feather \
			--output-folder $(CORPUS_VERSION)/dtm \
			--output-tag $${tag} ; \
	done

vrt-data:
	@echo "info: generating CWB extended VRT corpora..."
	@echo "info:    script: riksprot2vrt"
	@echo "info:    source: $(CORPUS_VERSION)/tagged_frames"
	@echo "info:    target: $(CORPUS_VERSION)/vrt"
	@rm -rf $(CORPUS_VERSION)/vrt && mkdir -p $(CORPUS_VERSION)/vrt
	@riksprot2vrt \
		--source-folder $(CORPUS_VERSION)/tagged_frames \
		--target-folder $(CORPUS_VERSION)/vrt \
		--metadata-filename metadata/riksprot_metadata.${METADATA_VERSION}.db \
		--merge-strategy chain \
		--structural-tag protocol \
		--structural-tag speech \
		--batch-tag year

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
	@echo "   source: $(CORPUS_VERSION)/vrt"
	@echo "   target: $(CORPUS_VERSION)/cwb"
	@echo "   CWB name: $(CWB_REGISTRY_ENTRY)"
	@rm -rf $(CWB_TARGET_FOLDER) && mkdir -p $(CWB_TARGET_FOLDER)
	@if [ ! -d "$(CWB_REGISTRY_FOLDER)" ] ; then \
		mkdir -p $(CWB_REGISTRY_FOLDER) ; \
	fi
	@cwb-encode -d $(CWB_TARGET_FOLDER) -sxBC9 -c utf8 \
		-F `pwd`/$(CORPUS_VERSION)/vrt \
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
	@if [ ! -f "$(CORPUS_VERSION)/registry/$(CWB_REGISTRY_ENTRY)" ] ; then \
		mkdir -p $(CORPUS_VERSION)/registry ; \
		cp $(CWB_REGISTRY_FOLDER)/$(CWB_REGISTRY_ENTRY) $(CORPUS_VERSION)/registry/$(CWB_REGISTRY_ENTRY) ; \
	fi

cwb-data-manual-compress:
	@echo "info: compressing CWB $(CWB_CORPUS_NAME) manually"
	@cwb-makeall -V $(CWB_CORPUS_NAME);
	@echo rm $(cwb-huffcode -A $(CWB_CORPUS_NAME) | grep "You can delete" | cut -d '<' -f2 | cut -d '>' -f1)
	@echo rm $(cwb-compress-rdx -A $(CWB_CORPUS_NAME) | grep "You can delete" | cut -d '<' -f2 | cut -d '>' -f1)


# FIXME: VERSION CHECKS
# METADATA_GIT_FOLDER=$(shell yq '.metadata.github.local_folder' $(CONFIG_FILENAME))
# CORPUS_FOLDER=$(shell yq '.corpus.folder' $(CONFIG_FILENAME))

# ifeq ($(wildcard $(CORPUS_FOLDER)/.git),)
# CHECKED_OUT_TAG := $(CORPUS_VERSION)
# else
# CHECKED_OUT_TAG=$(shell git -C $(CORPUS_FOLDER) describe --tags)
# endif

# ifeq ($(wildcard $(METADATA_GIT_FOLDER)/.git),)
# CHECKED_OUT_METADATA_TAG := $(METADATA_VERSION)
# else
# CHECKED_OUT_METADATA_TAG=$(shell git -C $(METADATA_GIT_FOLDER) describe --tags)
# endif

# ifneq ($(CORPUS_VERSION),$(CHECKED_OUT_TAG))
# 	$(error repository tag $(CHECKED_OUT_TAG) and .env tag $(CORPUS_VERSION) mismatch)
# endif
# ifneq ($(METADATA_VERSION),$(CHECKED_OUT_METADATA_TAG))
# 	$(error repository tag $(CHECKED_OUT_TAG) and .env tag $(METADATA_VERSION) mismatch)
# endif

# MOVED FROM PYRIKSPROT/Makefile
# verify-metadata-filenames:
# 	@echo "info: checking metadata filenames for $(METADATA_VERSION)"
# 	@PYTHONPATH=. poetry run python pyriksprot/scripts/metadata2db.py filenames $(CONFIG_FILENAME) $(METADATA_VERSION)

# verify-metadata-columns:
# 	@PYTHONPATH=. poetry run python pyriksprot/scripts/metadata2db.py columns $(CONFIG_FILENAME) $(METADATA_VERSION)

# .PHONY: metadata-database-vacuum
# metadata-database-vacuum:
# 	@sqlite3 metadata/$(METADATA_DATABASE_NAME) "VACUUM;"

# LIGHT_METADATA_DB_NAME=riksprot_metadata.$(METADATA_VERSION).light.db

# .PHONY: metadata-light-database
# metadata-light-database:
# 	@cp -f metadata/$(METADATA_DATABASE_NAME) metadata/$(LIGHT_METADATA_DB_NAME)
# 	@sqlite3 metadata/$(LIGHT_METADATA_DB_NAME) < ./metadata/10_make_light.sql
# 	@sqlite3 metadata/$(LIGHT_METADATA_DB_NAME) "VACUUM;"
# 	@cp -f metadata/$(LIGHT_METADATA_DB_NAME) $(shell yq '.root_folder' $(CONFIG_FILENAME))/metadata

# TEST_METADATA=tests/test_data/source/$(CORPUS_VERSION)/riksprot_metadata.db

# .PHONY: metadata-dump-schema
# metadata-dump-schema:
# 	@echo -e ".output riksprot_metadata_testdata_$(METADATA_VERSION).sql\n.dump\n.exit" | sqlite3 $(TEST_METADATA)
# 	@echo -e ".output riksprot_metadata_testdata_schema_$(METADATA_VERSION).sql\n.schema\n.exit" | sqlite3 $(TEST_METADATA)
