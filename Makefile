.PHONY: build check check-all clean

build: clean
	uv build --offline --no-cache

check: build
	uv run python -W error -m compileall -q -f xo tests
	uv run python -m unittest
	uv run python -m doctest -f README.md
	uv run validate-pyproject pyproject.toml
	uv run twine check dist/*
	nix flake check -L
	actionlint

check-all: check
	nix run .#test-all-previous

clean:
	rm -rf dist
