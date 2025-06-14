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
        pythonEnv = pkgs.python312.withPackages (ps: with ps; [
          certifi
          websockets
          joblib
          pyserial
          scikit-learn
          gpiozero
          # lgpio
          # RPi.GPIO
          # pigpio
          # PCA9685-smbus2
        ]);

        # Empaquetar projecte com script executable
        appPackage = pkgs.stdenv.mkDerivation {
          name = "cotxe-ptin";
          src = ./.;

          # Fer que al contenidor existi la ruta:
          # /nix/store/...-cotxe-ptin/app/src/main.py
          installPhase = ''
            mkdir -p $out/app
            cp -r src $out/app/src
            cp requirements.txt $out/app/
          '';
        };

        docker_image_build = pkgs.dockerTools.streamLayeredImage {
          name = "cotxe-ptin";
          tag = "0.5.0";

          contents = [
            pythonEnv
            pkgs.coreutils
            pkgs.busybox
            appPackage
          ];

          config = {
            WorkingDir = "/app";
            Cmd = [ "python" "src/main.py" ];
            Env = [
              "PYTHONUNBUFFERED=1"
              "CAR_ID=0x346B9B94"
              "CAR_CONTROLLER=ws://192.168.10.11:8765"
              "CAR_LOG_LEVEL=INFO"
            ];
          };
        };
      in {
        # Per poder construir la imatge amb "nix build"
        packages.default = docker_image_build;

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            python3.pkgs.pip
            python3.pkgs.certifi
            python3.pkgs.websockets
          ];

          shellHook = ''
            python -m venv .venv
            source .venv/bin/activate
            pip install -r requirements.txt
          '';
        };
      }
    );
}

