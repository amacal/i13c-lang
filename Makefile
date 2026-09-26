.PHONY: install
install:
	@sudo apt update
	@sudo apt install -y nasm
	@pipx install poetry==2.5.1 --force

.PHONY: deps
deps:
	@poetry install --no-root

.PHONY: update
update:
	@poetry update

.PHONY: lint
lint:
	@poetry run pyright src/i13c src/tests
	@poetry run ruff check src/i13c src/tests --fix

.PHONY: test
test: test-core test-inline test-syntax test-semantic test-encoding
	@echo "All tests passed!"

.PHONY: test-inline
test-inline:
	@poetry run pytest -vvo python_files='*.py' -o python_functions="can_*" src/i13c/

.PHONY: test-core
test-core:
	@poetry run pytest -vvo python_files='*.py' -o python_functions="can_*" src/tests/core/

.PHONY: test-syntax
test-syntax:
	@poetry run pytest -vvo python_files='*.py' -o python_functions="can_*" src/tests/syntax/

.PHONY: test-semantic
test-semantic:
	@poetry run pytest -vvo python_files='*.py' -o python_functions="can_*" src/tests/semantic/

.PHONY: test-encoding
test-encoding:
	@poetry run pytest -vvo python_files='*.py' -o python_functions="can_*" src/tests/encoding/

.PHONY: asm
asm:
	@ndisasm -b 64 -k0,120 a.out


.PHONY: ai-commit
ai-commit:
	@bash scripts/ai-commit

.PHONY: ai-amend
ai-amend:
	@bash scripts/ai-amend

.PHONY: ai-help
ai-help:
	@bash scripts/ai-help

.PHONY: ai-typos
ai-typos:
	@bash scripts/ai-typos $(BASE)

.PHONY: ai-review
ai-review:
	@bash scripts/ai-review $(BASE)
