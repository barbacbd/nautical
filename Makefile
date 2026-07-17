.PHONY: setup install test test-py test-go lint lint-py format format-py format-go format-check format-check-py format-check-go coverage coverage-py coverage-go clean

setup: install
	pre-commit install

install:
	pip install ".[test]" --upgrade

test: test-py test-go

test-py:
	pytest --cov=tests

test-go:
	go test -v ./...

format: format-py format-go

format-py:
	ruff format .
	ruff check --fix .

format-go:
	gofmt -w pkg/ nautical.go

format-check: format-check-py format-check-go

format-check-py:
	ruff format --check .
	ruff check .

format-check-go:
	@test -z "$$(gofmt -l pkg/ nautical.go)" || { echo "gofmt needed on:"; gofmt -l pkg/ nautical.go; exit 1; }

lint: lint-py

lint-py:
	@if [ ! -f .pylintrc ]; then \
		echo "Downloading .pylintrc ..."; \
		curl -sO https://raw.githubusercontent.com/barbacbd/tools/main/lint/python/.pylintrc; \
	fi
	pylint nautical/* --rcfile=.pylintrc

coverage: coverage-py coverage-go

coverage-py:
	pytest --cov=tests --cov-report=term-missing

coverage-go:
	go test -v -race -coverprofile=coverage.out -covermode=atomic ./...
	go tool cover -func=coverage.out

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage coverage.out
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
