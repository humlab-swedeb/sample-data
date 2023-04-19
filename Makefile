include .env

.ONESHELL: edit-mode
edit-mode:
	@poetry add --editable ../../welfare-state-analytics/pyriksprot_tagger

.ONESHELL: prod-mode
prod-mode:
	@poetry remove pyriksprot_tagger
	@poetry add pyriksprot_tagger
