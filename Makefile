all:
	noop

coverage:
	coverage erase
	COVERAGE_FILE="$(shell pwd)/.coverage" coverage run --source wikitexthtml -m pytest tests
	coverage report -m
	coverage html

.PHONY: all coverage
