# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-09-23

### Added

- Support for Python 3.11, 3.12, 3.13 and 3.14.

### Changed

- Python 3.11 or later is now required.
- The package is built from `pyproject.toml` with uv instead of `setup.py`.
- The README and changelog are now written in Markdown.
- The README examples now match the library's actual output and are checked with doctest.
- Renamed `LICENSE.txt` to `LICENSE`.

### Removed

- Support for Python 3.5.
- `xo.__version__` and `xo.__author__`.

### Fixed

- An invalid escape sequence in the CLI's move parsing that caused a `SyntaxWarning` on Python 3.12 and later.
- The README imported `isempty` from `xo.board` instead of `xo.token`.

## [1.0.0] - 2016-09-09

### Added

- A board data structure.
- An arbiter.
- A game engine.
- An AI based on the Minimax algorithm.
- A CLI.

## [0.0.1] - 2016-09-05

Birth!

[Unreleased]: https://github.com/dwayne/xo-python/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/dwayne/xo-python/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/dwayne/xo-python/compare/v0.0.1...v1.0.0
[0.0.1]: https://github.com/dwayne/xo-python/releases/tag/v0.0.1
