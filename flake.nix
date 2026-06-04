{
  description = "Silicon Witchery docs — Jekyll dev shell";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" "x86_64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            ruby_3_3   # Includes `bundle` and matches github-pages (~> 228)
            gcc        # Tools to build native gems
            gnumake
            pkg-config
            zlib
            libffi

            # Shortcut for starting the server
            (writeShellScriptBin "start" "bundle install && exec bundle exec jekyll serve --livereload")
          ];
          shellHook = ''
            export BUNDLE_PATH="$PWD/.bundle"   # Keep gems here rather than on system path
            export BUNDLE_FORCE_RUBY_PLATFORM=1 # Build gems for Nix rather than pulling them
          '';
        };
      });
    };
}
