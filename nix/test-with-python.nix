{ lib
, uv
, writeShellApplication

, python
}:

writeShellApplication {
  name = "test-with-py${lib.replaceStrings [ "." ] [ "" ] python.pythonVersion}";
  runtimeInputs = [
    python
    uv
  ];
  text = ''
    export UV_PYTHON_DOWNLOADS="never"

    echo "=== Python ${python.pythonVersion}"
    uv run --isolated --python ${python.interpreter} python -m unittest
  '';
}
