all: help
SHELL=/bin/bash
ANNOREPO_PATH=~/workspaces/annorepo/annorepo

.PHONY: pdoc
pdoc:
	pdoc --html --force --output-dir docs annorepo

.PHONY: install
install:
	poetry lock && poetry install

.PHONY: tests
tests:
	poetry run pytest

docs/requirements.txt: poetry.lock
	poetry export -o docs/requirements.txt --without-hashes

.PHONY: annorepo-grpc
annorepo-grpc:
	python -m grpc_tools.protoc \
	-I $(ANNOREPO_PATH)/common/src/main/proto \
	--python_out=annorepo/grpc \
	--pyi_out=annorepo/grpc \
	--grpc_python_out=annorepo/grpc \
	$(ANNOREPO_PATH)/common/src/main/proto/*.proto

.PHONY: publish
publish: docs/requirements.txt
	make tests
	poetry build && poetry publish

.PHONY: version-update-patch
version-update-patch:
	poetry run version patch

.PHONY: version-update-minor
version-update-minor:
	poetry run version minor

.PHONY: version-update-major
version-update-major:
	poetry run version major

.PHONY: help
help:
	@echo "make-tools for annorepo-client"
	@echo
	@echo "Please use \`make <target>', where <target> is one of:"
	@echo "  install               - to install the necessary requirements"
	@echo "  pdoc                  - generate pdoc html pages in docs"
	@echo "  annorepo-grpc         - generate annorepo/grpc files based on the .proto in annorepo"
	@echo "  clean                 - to remove all generated files and directories"
	@echo "  tests                 - to run the unit tests in tests/"
	@echo
	@echo "  version-update-patch  - to update the project version to the next patch version"
	@echo "  version-update-minor  - to update the project version to the next minor version"
	@echo "  version-update-major  - to update the project version to the next major version"
	@echo
	@echo "  publish               - to publish to pypi"
	@echo "  docs/requirements.txt - to update the requirements.txt based on poetry.lock (required by readthedocs)"
	@echo
