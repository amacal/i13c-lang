.PHONY: deps
deps:
	@poetry install --no-root

.PHONY: install
install:
	@poetry install --only-root

.PHONY: run
run:
	@poetry run i13c
