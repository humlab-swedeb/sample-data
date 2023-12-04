include .env

SHELL := /bin/bash

DATA_FOLDER=.

dataset: parlaclarin-corpus word-frequencies tag-protocols tagged-speech-corpora text-corpora dtm-corpora

parlaclarin-corpus:
	@echo "Target(s): 1) subset of Parla-CLARIN corpus 2) processed metadata"
	@echo "Script(s): pyriksprot.scripts.subset-corpus:main"
	@subset-corpus ./protocols.txt ./ $(SWEDEB_TAG)

word-frequencies:
	@echo "Target(s): global term frequencies (TF)"
	@echo "Script(s): pyriksprot.scripts.riksprot2tfs:main"
	@mkdir -p $(SWEDEB_TAG)/dehyphen_datadir
	@riksprot2tfs $(SWEDEB_TAG)/parlaclarin $(SWEDEB_TAG)/dehyphen_datadir/word-frequencies.pkl

tag-protocols:
	@echo "Target(s): tagged parlaclarin protocols (tagged frames)"
	@echo "Script(s): pyriksprot_tagger.scripts.tag:main"
	@pos_tag opts/tagger-config.yml $(SWEDEB_TAG)/parlaclarin/protocols $(SWEDEB_TAG)/tagged_frames

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
	@echo "Script(s): pyriksprot.scripts.riksprot2speech_text:main"
	@echo "     Note: penelope must be installed in current environment"
	@rm -rf $(SWEDEB_TAG)/dtm && mkdir -p $(SWEDEB_TAG)/dtm
	 for file in $^ ; do \
	 	tag=$$(basename $${file%.yml})
		echo " => $(SWEDEB_TAG)/speeches/$${tag}" ; \
		vectorize-id \
		    --create-subfolder \
			--options-filename $${file} \
			--corpus-source $(SWEDEB_TAG)/speeches/tagged_frames_speeches_$${tag}.feather \
			--output-folder $(SWEDEB_TAG)/dtm \
			--output-tag $${tag} ; \
    done

vrt-data:
	@PYTHONPATH=. poetry run riksprot2vrt \
		--source-folder $(SWEDEB_TAG)/tagged_frames --target-folder $(SWEDEB_TAG)/vrt \
		-t protocol -t speech --batch-tag year

CWB_TARGET_FOLDER=`pwd`/$(SWEDEB_TAG)/cwb
CWB_REGISTRY_ENTRY := riksprot_$(subst .,,$(SWEDEB_TAG))_test
CWB_CORPUS_NAME := $(shell X="${CWB_REGISTRY_ENTRY}"; echo $${X^^})

cwb-make-exists = $(if $(shell which cwb-make 2> /dev/null),true,false)

.PHONY: cwb-data
cwb-data:
	@rm -rf $(CWB_TARGET_FOLDER) && mkdir -p $(CWB_TARGET_FOLDER)
	@cwb-encode -d $(CWB_TARGET_FOLDER) -s -x -B -c utf8 \
		-F `pwd`/$(SWEDEB_TAG)/vrt \
		-R /usr/local/share/cwb/registry/$(CWB_REGISTRY_ENTRY) \
		-P lemma -P pos -P xpos \
		-S year:0+title+date \
		-S protocol:0+title+date \
		-S speech:0+id+title+who+name+date+party_id+gender_id+office_type_id+sub_office_type_id+name+page_number
	@if [ "$(cwb-make-exists)" == "true" ]; then \
		cwb-make -V $(CWB_CORPUS_NAME); \
	else \
		echo "info: cwb-make not found, skipping corpus creation"; \
		echo "info: run 'sudo cpan install CWB' to install the CWB/Perl toolkit"
	fi
	@cwb-describe-corpus $(CWB_CORPUS_NAME)
