{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem(system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        mkTest = python: pkgs.callPackage ./nix/test-with-python.nix { inherit python; };

        test-with-py311 = mkTest pkgs.python311;
        test-with-py312 = mkTest pkgs.python312;
        test-with-py313 = mkTest pkgs.python313;
        test-with-py314 = mkTest pkgs.python314;

        test-all-previous = pkgs.callPackage ./nix/test-all-previous.nix {
          tests = [ test-with-py311 test-with-py312 test-with-py313 ];
        };

        xo = pkgs.python314Packages.callPackage ./nix/xo.nix {};
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

        packages = {
          default = xo;
          inherit test-all-previous test-with-py311 test-with-py312 test-with-py313 test-with-py314 xo;
        };

        checks = {
          inherit xo;
        };
      }
    );
}
