include .env
include ../Makefile

SHELL := /bin/bash

ifndef CORPUS_VERSION
$(error environment variable CORPUS_VERSION is undefined)
endif

DATA_FOLDER=.
PARLACLARIN_MODE=protocols
METADATA_MODE=create
TAGGING_MODE=tag
WORD_FREQUENCY_MODE=create
CWB_REGISTRY_FOLDER=$(shell pwd)/$(CORPUS_VERSION)/registry

