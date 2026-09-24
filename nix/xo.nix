{
  lib,
  buildPythonApplication,
  uv-build,
  unittestCheckHook
}:

let
  pyprojectToml = lib.importTOML ../pyproject.toml;
in
buildPythonApplication {
  pname = "xo";
  inherit (pyprojectToml.project) version;
  pyproject = true;

  src = lib.fileset.toSource {
    root = ../.;
    fileset = lib.fileset.unions [
      ../tests
      ../xo
      ../LICENSE
      ../pyproject.toml
      ../README.md
    ];
  };

  build-system = [ uv-build ];

  nativeCheckInputs = [ unittestCheckHook ];
  pythonImportsCheck = [ "xo" ];

  meta = {
    inherit (pyprojectToml.project) description;
    homepage = "https://github.com/dwayne/xo-python";
    license = lib.licenses.mit;
    mainProgram = "xo";
  };
}
