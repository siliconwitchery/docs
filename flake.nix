{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in
    {
      devShells.x86_64-linux.default = pkgs.mkShell {
        packages = [
          pkgs.ruby
          pkgs.bundler # RubyGems 3.7 in nixpkgs' Ruby warns with Ruby's default Bundler 2.6
        ];

        shellHook = ''
          export BUNDLE_PATH="$PWD/.bundle"
          export BUNDLE_BIN="$PWD/.bundle/bin"
          export PATH="$BUNDLE_BIN:$PATH"
          bundle check > /dev/null || bundle install
        '';
      };
    };
}
