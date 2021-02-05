let
  pkgs = import <nixpkgs> {};
  # todo maybe run node2nix here instead of ./npm_global/generate.sh
  nodePkgs = import ./npm_global/default.nix {
    inherit pkgs;
  };
in
  pkgs.mkShell {
    buildInputs = [
      pkgs.nodejs
      pkgs.nodePackages.npm
      pkgs.nodePackages.node2nix
      nodePkgs."@vue/cli" # vue build tools
      nodePkgs.vls # vue lang server
    ];
  }
