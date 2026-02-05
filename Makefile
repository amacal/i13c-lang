.PHONY: install
install:
	@pipx install poetry==2.3.1 --force

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
	@export PYTHONPATH="./i13c-lang/src"
	@poetry run pytest -vo python_files='*.py' -o python_functions="can_*" src/tests

.PHONY: asm
asm:
	@ndisasm -b 64 -k0,120 a.out

.PHONY: dump-lowering
dump-lowering:
	@find ./src/i13c/lowering -type f -name '*.py' -print0 \
	| xargs -0 -I{} sh -c 'echo "{}"; cat "{}"; echo' > dump


.PHONY: dump-semantic
dump-semantic:
	@find ./src/i13c/sem -type f -name '*.py' -print0 \
	| xargs -0 -I{} sh -c 'echo "{}"; cat "{}"; echo' > dump
