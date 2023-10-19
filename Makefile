all: help
SHELL=/bin/bash
ANNOREPO_PATH=~/workspaces/annorepo/annorepo

.PHONY: pdoc
pdoc:
	pdoc --html --force --output-dir docs annorepo

.PHONY: install
install:
	poetry lock
	poetry install

.PHONY: annorepo-grpc
annorepo-grpc:
	python -m grpc_tools.protoc \
	-I $(ANNOREPO_PATH)/common/src/main/proto \
	--python_out=annorepo/grpc \
	--pyi_out=annorepo/grpc \
	--grpc_python_out=annorepo/grpc \
	$(ANNOREPO_PATH)/common/src/main/proto/*.proto

.PHONY: help
help:
	@echo "make-tools for annorepo-client"
	@echo
	@echo "Please use \`make <target>', where <target> is one of:"
	@echo "  install       - to install the necessary requirements"
	@echo "  pdoc          - generate pdoc html pages in docs"
	@echo "  annorepo-grpc - generate annorepo/grpc files based on the .proto in annorepo"
	@echo
