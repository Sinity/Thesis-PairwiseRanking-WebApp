{ pkgs ? import <nixpkgs> {} }:

let
  poetryEnv = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./backend;
    editablePackageSources = {
      webrankit = ./backend/webrankit;
    };
  };
  nodePkgs = import ./frontend/npm_global/default.nix {
    inherit pkgs;
  };
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    poetry
    poetryEnv

    pkgs.nodejs
    pkgs.nodePackages.npm
    pkgs.nodePackages.node2nix
    nodePkgs."@vue/cli" # Vue 3 build tools
    nodePkgs.vls # Vue language server
  ];
}

