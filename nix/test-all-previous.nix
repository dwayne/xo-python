{ python311
, python312
, python313
, uv
, writeShellApplication
}:

writeShellApplication {
  name = "test-all-previous";
  runtimeInputs = [
    python311
    python312
    python313
    uv
  ];
  text = ''
    export UV_PYTHON_DOWNLOADS="never"

    for v in 3.11 3.12 3.13; do
      echo "=== Python $v"
      uv run --isolated --python "$v" python -m unittest
    done
  '';
}
