# Silicon Witchery Docs - Source

This site is built with [Jekyll](https://jekyllrb.com) and [Just the Docs](https://github.com/just-the-docs/just-the-docs). It's all hosted here on GitHub using the GitHub's [Pages](https://pages.github.com) feature.

**If you spot any errors** in our documentation, feel free to make an [issue](https://github.com/siliconwitchery/docs/issues).

If you'd like to make extensive edits, you can also clone this repository locally and view the pages live while editing.

## Running locally

This project uses a [Nix](https://nixos.org) flake to provide its toolchain. The flake supports x86-64 Linux only.

1. Install Nix with flakes enabled, and [direnv](https://direnv.net).

1. Clone this repository:

    ```sh
    git clone git@github.com:siliconwitchery/docs.git
    ```

1. Enable `direnv`, which enters the development shell and installs the gems:

    ```sh
    cd docs
    direnv allow
    ```

1. Start the live server:

    ```sh
    bundle exec jekyll serve --livereload --port 4001
    ```

1. Open <http://localhost:4001>. The site rebuilds and refreshes your browser automatically as you edit.
