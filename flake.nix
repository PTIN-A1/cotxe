{
    description = "Software pel cotxe, tant físic com virtual";

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

                dev_tools = with pkgs.python312Packages; [
                    pip

                    bandit
                    flake8

                    python-lsp-server
                    python-lsp-ruff
                    autopep8
                ];
                
                native_package_build = pkgs.python312Packages.buildPythonPackage {
                    pname = "cotxe-ptin";
                    version = "0.3.0";

                    src = pkgs.lib.cleanSource ./.;
                    
                    propagatedBuildInputs = with pkgs.python312Packages; [
                        pyserial
                        certifi
                        websockets
                    ];
                };

                docker_image_build = pkgs.dockerTools.buildImage {
                    name = "cotxe-ptin";
                    tag = "0.3.0";

                    contents = [ native_package_build pkgs.coreutils pkgs.busybox ];

                    config = {
                        Cmd = [ "${native_package_build}/bin/cotxe-ptin" ];
                        Env = [ "PYTHONUNBUFFERED=1" 
                                "CAR_TYPE=virtual"
                        ]; # PYTHONBUFFERED=1 -> Sense buffer, per tant els missatges s'imprimiran per la sortida estàndard cada vegada que s'executi un print
                    }; # CAR_TYPE -> pot ser "virtual" o "physical"
                };

            in { 
                packages = {
                    default = native_package_build;
                    docker = docker_image_build;
                };
                
                devShells.default = pkgs.mkShell {
                    buildInputs = build_tools ++ dev_tools;

                    shellHook = ''
                        python -m venv .venv
                        source .venv/bin/activate
                        pip install -r requirements.txt
                    '';
                };
            }
        );
}
