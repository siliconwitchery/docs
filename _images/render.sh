#!/bin/sh
# Render mastheads into assets/images, for example:
#   _images/render.sh s2-module s1-module
set -eu

dir=$(cd "$(dirname "$0")" && pwd)
profile=$(mktemp -d)
trap 'rm -rf "$profile"' EXIT

for name in "$@"; do
    chromium --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
        --user-data-dir="$profile" --window-size=1640,540 --virtual-time-budget=15000 \
        --screenshot="$dir/../assets/images/$name-annotated-masthead.png" \
        "file://$dir/masthead.html?p=$name" 2>/dev/null
done
