all: help
SHELL=/bin/bash

.PHONY: pdoc
pdoc:
	pdoc --html --force --output-dir docs annorepo

.PHONY: help
help:
	@echo "make-tools for annorepo-client"
	@echo
	@echo "Please use \`make <target>', where <target> is one of:"
	@echo "pdoc	Generate pdoc html pages in docs"
	@echo
