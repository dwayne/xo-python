.PHONY: build check clean

build: clean
	uv build --offline --no-cache

check: build
	uv run python -W error -m compileall -q -f xo tests
	uv run python -m unittest
	uv run validate-pyproject pyproject.toml
	uv run twine check dist/*

clean:
	rm -rf dist
