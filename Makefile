.PHONY: install test test-py test-go lint lint-py coverage coverage-py coverage-go clean

install:
	pip install ".[test]" --upgrade

test: test-py test-go

test-py:
	pytest --cov=tests

test-go:
	go test -v ./...

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
