{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem(system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          name = "xo-python-dev";

          packages = [
            pkgs.python314
            pkgs.uv
          ];

          env = {
            UV_PYTHON = pkgs.python314.interpreter;
            UV_PYTHON_DOWNLOADS = "never";
          };

          shellHook = ''
            export PROJECT_ROOT="$(git rev-parse --show-toplevel)"
            export PS1="($name)\n$PS1"

            uv sync && . .venv/bin/activate
          '';
        };

        packages = let
          test-all-previous = pkgs.writeShellApplication {
            name = "test-all-previous";
            runtimeInputs = with pkgs; [
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
          };
        in
        { inherit test-all-previous; };
      }
    );
}
