.PHONY: install
install:
	@sudo apt update
	@sudo apt install -y nasm
	@pipx install poetry==2.3.3 --force

.PHONY: deps
deps:
	@poetry install --no-root

.PHONY: update
update:
	@poetry update

.PHONY: lint
lint:
	@poetry run isort src/i13c src/tests
	@poetry run pyright src/i13c src/tests
	@poetry run ruff check src/i13c src/tests --fix

.PHONY: test
test:
	@poetry run pytest -vvo python_files='*.py' -o python_functions="can_*" src/tests

.PHONY: asm
asm:
	@ndisasm -b 64 -k0,120 a.out

.PHONY: dump-llvm
dump-llvm:
	@find ./src/i13c/llvm -type f -name '*.py' -print0 \
	| xargs -0 -I{} sh -c 'echo "{}"; cat "{}"; echo' > dump


.PHONY: dump-semantic
dump-semantic:
	@find ./src/i13c/semantic -type f -name '*.py' -print0 \
	| xargs -0 -I{} sh -c 'echo "{}"; cat "{}"; echo' > dump
