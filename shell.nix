{ pkgs ? import <nixpkgs> {} }:

with pkgs;
let
  Rlibs = with rPackages; [
    argparser
    BradleyTerry2
  ];
  Rrpy2 = python38Packages.rpy2.override { extraRPackages = Rlibs; };
  Rruntime = rWrapper.override{ packages = Rlibs; };

  poetryEnv = poetry2nix.mkPoetryEnv {
    projectDir = ./backend;
    editablePackageSources = { webrankit = ./backend/webrankit; };
  };
  nodePkgs = import ./frontend/npm_global/default.nix { inherit pkgs; };
in
mkShell {
  buildInputs = [
    poetry
    poetryEnv
    Rruntime
    Rrpy2

    nodejs
    nodePackages.npm
    nodePackages.node2nix
    nodePkgs."@vue/cli" # Vue 3 build tools
    nodePkgs.vls # Vue language server
  ];
}

