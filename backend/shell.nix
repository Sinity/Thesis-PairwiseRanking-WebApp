{ pkgs ? import <nixpkgs> {} }:

let poetryEnv = pkgs.poetry2nix.mkPoetryEnv {
  projectDir = ./.;
  editablePackageSources = {
    webrankit = ./webrankit;
  };
};
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    poetry
    poetryEnv
  ];
}

