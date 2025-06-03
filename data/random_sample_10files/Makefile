include .env
include ../Makefile

SHELL := /bin/bash

DATA_FOLDER=.
PARLACLARIN_MODE=protocols
METADATA_MODE=create
TAGGING_MODE=subset
WORD_FREQUENCY_MODE=create
GLOBAL_FOLDER=/data/swedeb
GLOBAL_CORPUS_FOLDER=$(GLOBAL_FOLDER)/riksdagen-records/data

ifndef CORPUS_VERSION
$(error environment variable CORPUS_VERSION is undefined)
endif
