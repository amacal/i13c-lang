.PHONY: deps
deps:
	@poetry install --no-root

.PHONY: update
update:
	@poetry update

.PHONY: install
install:
	@poetry install --only-root

.PHONY: run
run:
	@poetry run i13c

.PHONY: test
test:
	@poetry run pytest -o python_files='*.py' -o python_functions="can_*" src/tests


.PHONY: disasm
disasm:
	@ndisasm -b 64 -k0,120 a.out
