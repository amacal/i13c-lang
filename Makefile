.PHONY: deps
deps:
	@poetry install --no-root

.PHONY: update
update:
	@poetry update

.PHONY: lint
lint:
	@poetry run black src/i13c src/tests
	@poetry run isort src/i13c src/tests

.PHONY: test
test:
	@poetry run pytest -o python_files='*.py' -o python_functions="can_*" src/tests


.PHONY: asm
asm:
	@ndisasm -b 64 -k0,120 a.out
