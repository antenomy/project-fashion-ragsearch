{
  description = "work-hm-project dev environment with playwright";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    playwright-web-flake.url = "github:pietdevries94/playwright-web-flake";
  };

  outputs = { self, nixpkgs, playwright-web-flake }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
      playwrightPkgs = import playwright-web-flake { inherit pkgs; };
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = [
          pkgs.python311
          playwrightPkgs.playwright-test
        ];

        shellHook = ''
          export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc
          ]}:$LD_LIBRARY_PATH
          export PYTHONNOUSERSITE="true"
          echo "Activated work-hm-project dev environment with playwright."
        '';
      };
    };
}