{
    description = "Software pel cotxe físic";

    inputs = {
        nixpkgs.url     = "github:NixOS/nixpkgs/nixos-24.11";
        flake-utils.url = "github:numtide/flake-utils";
    };

    outputs = { self, nixpkgs, flake-utils, ... }:
        flake-utils.lib.eachDefaultSystem (system:
            let
                pkgs = import nixpkgs { inherit system; };
                
                build_tools = with pkgs; [ 
                    python3
                ];

                dependencies = with pkgs.python312Packages; [
                    pyserial
                    websockets
                ];

                dev_tools = with pkgs.python312Packages; [
                    bandit
                    flake8

                    python-lsp-server
                    python-lsp-ruff
                    autopep8
                ];

            in { 
                devShells.default = pkgs.mkShell {
                    buildInputs = build_tools ++ dependencies ++ dev_tools;
                };
            }
        );
}
