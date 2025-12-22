.PHONY: deps
deps:
	@poetry install --no-root

.PHONY: update
update:
	@poetry update

.PHONY: install
install:
	@poetry install --only-root

.PHONY: lint
lint:
	@poetry run black src/i13c src/tests
	@poetry run isort src/i13c src/tests

.PHONY: run
run:
	@poetry run i13c

.PHONY: test
test:
	@poetry run pytest -o python_files='*.py' -o python_functions="can_*" src/tests


.PHONY: disasm
disasm:
	@ndisasm -b 64 -k0,120 a.out
