# Silicon Witchery Docs - Source

This site is built with [Jekyll](https://jekyllrb.com) and [Just the Docs](https://github.com/just-the-docs/just-the-docs). It's all hosted here on GitHub using the GitHub's [Pages](https://pages.github.com) feature.

**If you spot any errors** in our documentation, feel free to make an [issue](https://github.com/siliconwitchery/docs/issues).

If you'd like to do some extensive editing, you can also fork/clone this repository and view the pages live editing.

## Running locally

This site uses [Nix](https://nixos.org) to provide a reproducible toolchain — Ruby, Bundler, and the native build dependencies its gems need. The steps below are identical on macOS, Linux, and NixOS.

1. Install Nix, if you don't have it already. The [Determinate Systems installer](https://determinate.systems/nix-installer) works on macOS and Linux and enables flakes out of the box (on NixOS, Nix is already set up):

    ```bash
    curl -fsSL https://install.determinate.systems/nix | sh -s -- install
    ```

1. Clone this repository and enter it:

    ```bash
    git clone https://github.com/siliconwitchery/docs.git
    cd docs
    ```

1. Enter the development shell. The first run downloads the pinned toolchain:

    ```bash
    nix develop
    ```

1. Start the live server:

    ```bash
    start
    ```

1. Open <http://localhost:4000>. The site rebuilds and refreshes your browser automatically as you edit.

> **Tip:** install [direnv](https://direnv.net) and run `direnv allow` once in the repo, and the shell loads automatically whenever you `cd` in — then you can skip `nix develop` and just run `start`.