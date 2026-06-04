# Silicon Witchery Docs - Source

This site is built with [Jekyll](https://jekyllrb.com) and [Just the Docs](https://github.com/just-the-docs/just-the-docs). It's all hosted here on GitHub using the GitHub's [Pages](https://pages.github.com) feature.

**If you spot any errors** in our documentation, feel free to make an [issue](https://github.com/siliconwitchery/docs/issues).

If you'd like to make extensive edits, you can also clone this repository locally and view the pages live while editing.

## Running locally

This site uses [Nix](https://nixos.org) to provide a reproducible toolchain. It works on NixOS, Linux and MacOS.

1. Clone this repository:

    ```bash
    git clone https://github.com/siliconwitchery/docs.git
    ```

1. Install Nix (on NixOS, Nix is already set up):

    ```bash
    # Linux (not needed on NixOS)
    sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install) --daemon

    # MacOS
    sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install)
    ```

1. Install `direnv`. It automatically loads the environment whenever entering the directory:
    - On NixOS, simply add `programs.direnv.enable = true;` to your `configuration.nix`.
    - On Linux/MacOS, install with:
        ```sh
        nix profile install nixpkgs#direnv --extra-experimental-features nix-command --extra-experimental-features flakes
        echo 'eval "$(direnv hook zsh)"' >> $ZDOTDIR/.zshrc
        exec zsh
        ```

1. Enable `direnv`:

    ```sh
    cd docs
    direnv allow
    ```

1. Start the live server:

    ```sh
    start
    ```

1. Open <http://localhost:4000>. The site rebuilds and refreshes your browser automatically as you edit.
