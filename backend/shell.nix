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
    python3
    poetry
    poetryEnv

    python3.pkgs.pynvim
    #python3.pkgs.jedi

    python3.pkgs.black
    python3.pkgs.epc
    python3.pkgs.importmagic
    python3.pkgs.isort
    python3.pkgs.mypy
    python3.pkgs.pyls-black
    python3.pkgs.pyls-isort
    python3.pkgs.pyls-mypy
    python3.pkgs.python-language-server
  ];
}

