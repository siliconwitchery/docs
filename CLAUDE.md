# Silicon Witchery docs

This repository holds the technical documentation for the S1 Module, S2 Module
and Superstack. It is served at `docs.siliconwitchery.com` with the Just the
Docs theme. Most readers are engineers integrating a module. The docs also feed
sales on `siliconwitchery.com`: a reader who would rather not build the product
themselves should find a route to consulting.

## Follow the website

`~/projects/website/CLAUDE.md` defines the Silicon Witchery brand. Read these
sections of it and follow them:

- Art direction
- Truth in copy
- Search and answer engines
- Accessibility

The docs restyle the Just the Docs theme to match the website. Don't redesign
the theme.

## Funnel

The homepage and the S1 and S2 datasheets end with a "Let us build it for you"
section. It links to a Cal.com call and to the services page. Keep its copy the
same as `services.html` on the website.

## Search

`jekyll-seo-tag` appends " | Silicon Witchery Documentation Center" (40
characters) to every `title`. Keep each `title` to 20 characters, so the full
title fits in the roughly 60 characters that search results show.

## Images

The five product mastheads are PNG files in `assets/images`, named
`*-annotated-masthead.png`. Pages also use them as share images in the `image`
front matter, which must be a PNG or JPEG. They have no source file.

Datasheet diagrams are SVG files in `_includes/diagrams/`. A page includes the
SVG inline, so the diagram uses the site's fonts and the styles in the
"Diagrams" section of `_sass/custom/custom.scss`. Draw every new or changed
diagram this way. The other PNG diagrams in `assets/images` are old Figma
exports. Replace one with an SVG when you change it.

`_includes/diagrams/s2-module-power-inputs.svg` is the reference diagram. Copy
its structure.

## Draw a diagram

All sizes below are SVG units. The canvas is always 880 units wide, so text is
the same size in every diagram.

### 1. Export the render

Diagrams use the CAD renders in `~/company/branding/hardware`, named
`<date>-sw-render-<product>-<view>.png`. Use the newest render of the view you
need. Never use a `cutout` or `photo` file in a diagram. If no render shows the
view you need, ask the user.

The exported file is `assets/images/<product>-<view>.webp`, such as
`assets/images/s2-module-front.webp`. If it already exists, reuse it. Otherwise
export it with this command. It trims the transparent margin, scales the
longest side to 560 pixels and drops the metadata:

```sh
nix-shell -p 'python3.withPackages(p: [p.pillow])' --run "python3 - ~/company/branding/hardware/20261026-sw-render-s2-module-front.png assets/images/s2-module-front.webp" <<'EOF'
import sys
from PIL import Image

render = Image.open(sys.argv[1])
render = render.crop(render.getchannel("A").getbbox())
scale = 560 / max(render.size)
render = render.resize((round(render.width * scale), round(render.height * scale)), Image.LANCZOS)
render.save(sys.argv[2], quality=90)
print(sys.argv[2], render.size)
EOF
```

The command prints the file's pixel size, such as `(554, 560)`.

### 2. Place the render

Draw the render at half its pixel size, centred across the canvas, 20 units
from the top:

- `width = file width / 2`
- `height = file height / 2`
- `x = (880 - width) / 2`
- `y = 20`

For the 554 × 560 S2 render: `width="277" height="280" x="301.5" y="20"`.

When a diagram shows two renders, place them symmetrically about the canvas
centre, `x = 440`.

### 3. Measure points on the render

A point is a spot a callout or wire attaches to, such as a part or a connector
pin. Measure each point in the exported file's pixels, then convert it to
canvas units with the `x` and `y` from step 2:

- `canvas x = x + pixel x / 2`
- `canvas y = y + pixel y / 2`

For the S2 render, the thermistor at pixel (349.5, 490) is at canvas
(476.25, 265).

To find a part, draw a grid over a region of the file and view the result with
the Read tool. Pass the region as `left,top,right,bottom` in file pixels. The
grid has a line every 10 pixels, with a label every 50:

```sh
nix-shell -p 'python3.withPackages(p: [p.pillow])' --run "python3 - assets/images/s2-module-front.webp /tmp/grid.png 300,420,460,520" <<'EOF'
import sys
from PIL import Image, ImageDraw

render = Image.open(sys.argv[1]).convert("RGBA")
left, top, right, bottom = (int(v) for v in sys.argv[3].split(","))
zoom = 4

view = Image.alpha_composite(Image.new("RGBA", render.size, "#100c14"), render)
view = view.crop((left, top, right, bottom)).resize(((right - left) * zoom, (bottom - top) * zoom), Image.NEAREST)
draw = ImageDraw.Draw(view)

for x in range(left - left % 10, right, 10):
    draw.line([((x - left) * zoom, 0), ((x - left) * zoom, view.height)], fill="cyan" if x % 50 == 0 else "teal")
    if x % 50 == 0:
        draw.text(((x - left) * zoom + 2, 2), str(x), fill="cyan")

for y in range(top - top % 10, bottom, 10):
    draw.line([(0, (y - top) * zoom), (view.width, (y - top) * zoom)], fill="magenta" if y % 50 == 0 else "purple")
    if y % 50 == 0:
        draw.text((2, (y - top) * zoom + 2), str(y), fill="magenta")

view.save(sys.argv[2])
print(sys.argv[2])
EOF
```

Measure the centre of a part, not its edge.

Connector housings, pins and white parts are lighter than the board. To find
their exact edges, print the runs of light pixels along one row or one column
of the file:

```sh
nix-shell -p 'python3.withPackages(p: [p.pillow])' --run "python3 - assets/images/s2-module-front.webp row 556" <<'EOF'
import sys
from PIL import Image

render = Image.open(sys.argv[1]).convert("RGBA")
axis, at = sys.argv[2], int(sys.argv[3])
length = render.width if axis == "row" else render.height
runs, start = [], None

for i in range(length + 1):
    pixel = render.getpixel((i, at) if axis == "row" else (at, i)) if i < length else (0, 0, 0, 0)
    light = pixel[3] > 200 and sum(pixel[:3]) > 450
    if light and start is None:
        start = i
    if not light and start is not None:
        runs.append((start, i - 1))
        start = None

print(axis, at, runs)
EOF
```

It prints pairs of first and last pixels. On the S2 render, `row 556` prints
`[(83, 178), (387, 458)]`: the bottom faces of the external power port and the
battery port.

### 4. Measure a connector for wires

Wires leave the connector housing, so centre them on the housing, not on the
pins. The render has perspective: a tall housing appears further from the
image centre than its pins on the board. On the S2 bottom connectors, the
housing sits about 10 pixels further out than the pins.

1. **Face.** Find the face of the housing that the wires leave. For a
   connector on the bottom edge, run the edge command on a row 3 pixels above
   the housing's lowest pixel. The housing's centre is the midpoint of its run.
2. **Pitch.** Run the edge command on a row across the pins. The pitch is
   `(last pin centre - first pin centre) / (pins - 1)`.
3. **Positions.** Space the wires at the pitch, centred on the housing's
   centre. For 3 pins, they sit at `centre - pitch`, `centre` and
   `centre + pitch`. For 2 pins, they sit at `centre ± pitch / 2`.
4. **Start.** Each wire starts at the housing's outer edge. For a connector
   on the bottom edge, that is one pixel below the housing's lowest pixel.

For the S2 external power port, `row 556` gives the face 83 to 178, so the
centre is 130.5. `row 450` gives pins centred on 118.5, 140.5 and 162, so the
pitch is 21.75. The wires sit at pixels 108.75, 130.5 and 152.25, which are
canvas 355.875, 366.75 and 377.625. The housing's lowest pixel is 559, so
the wires start at pixel 560, which is canvas y 300.

### 5. Place the callouts

A callout is a chip of text joined to its point by a leader line.

1. **Side.** Put the callout on the side of the render nearest its point. A
   point left of `x = 440` gets a left callout, and a point right of it gets a
   right callout. A point exactly on 440 goes on the side with fewer callouts.
2. **Column.** Callouts on one side line up in a column, 48 units from the
   render:
   - Left chips end at `render x - 48`, so the column is right-justified.
   - Right chips start at `render x + render width + 48`, so the column is
     left-justified.
3. **Order.** Keep the chips on one side in the same top-to-bottom order as
   their points, so leaders never cross.
4. **Height.** Start with each chip centred on its point's height, which makes
   the leader horizontal. Then check what the leader passes over. A leader is
   a thin line, so the reader must be able to follow it to its point. If it
   runs along an edge of a part, a connector or the board, or within 6 units
   of one, move the chip up or down so the leader crosses that edge at an
   angle. Aim for 20 to 45 degrees from horizontal. Cross a housing through
   its middle, not at a corner.
5. **Spacing.** Chip centres on one side must be at least 40 units apart. With
   three or more chips on one side, space them evenly, then recheck each
   leader against rule 4.
6. **Leader.** Draw one straight line from the point to the middle of the
   chip's near edge, at any angle. Never bend a leader. A leader never crosses
   another leader, a chip, a wire or a label.
7. **Point.** Draw a `point` circle with `r="4"` on the point. The leader and
   point are moon, and the point has a night outline. Don't use candle gold
   there, because it disappears against the gold pads on the board.

On the S2 power inputs diagram, a horizontal leader from the thermistor runs
along the top edge of the battery port. The chip therefore sits 81 units
higher, at y 184, and the leader crosses the battery port's pins and the
lowest right-hand connector at 28 degrees.

Size each chip from its text. JetBrains Mono at 14 units is 8.4 units per
character, so for a chip centred at height `c`:

- `width = 8.4 × characters + 20`, counting spaces
- `height = 26` and `y = c - 13`
- text at `x = chip x + 10` and `y = c`

A chip must stay at least 8 units inside the canvas. If it doesn't fit, split
the text over two lines. A two-line chip has `height = 44` and `y = c - 22`,
with lines at `y = c - 9` and `y = c + 9`. Its width comes from the longer line.

### 6. Draw the wires

Draw wires on a connector when the diagram is about what that connector
carries.

1. **One wire per pin.** Draw a wire for every pin, including a pin the
   diagram doesn't describe. Readers must see that the pin exists, so they
   don't connect to it by mistake. On the external power port, pin 1 is the
   V<sub>SYS</sub> output, so it gets a wire with no label.
2. **Position.** Place the wires as step 4 measured them.
3. **Straight.** Run each wire straight away from the board, at right angles
   to the board edge. Never bend a wire. Never draw a wire over the housing,
   because a cream wire on the cream housing disappears.
4. **Flat colour.** Give each wire a class, and nothing else. `power` is
   ember, for a supply or battery rail. `ground` is dim, for GND. `unused` is
   cream, for a pin the diagram doesn't describe. The CSS sets a 5-unit width
   with square ends. Don't add tips, gradients, shadows or outlines.
5. **Label side.** Labels go on the side of the connector away from the
   canvas centre: the left side for a connector left of `x = 440`, and the
   right side otherwise.
6. **Length.** Make the wires a staircase, so each label has clear space
   beside its wire's end. The wire nearest the label side is 40 units long.
   Each next wire is 32 units longer than the one before.
7. **Wire label.** Give every wire except an `unused` one a `wire-label`
   beside its end, at `y = wire end`:
   - Label side left: class `wire-label end` at `x = wire x - 8.5`.
   - Label side right: class `wire-label` at `x = wire x + 8.5`.
8. **Connector name.** Name the connector in a chip on the label side. Leave
   16 units between the chip and the label or wire that reaches furthest out.
   Centre the chip on the middle of the longest wire. This chip has no leader.

A wire label is 8.4 units wide per character, and 6.6 per subscript
character. Write a subscript as a `tspan` with class `sub` and `dy="4"`, such
as `V<tspan class="sub" dy="4">IN</tspan>`.

For the external power port, the label side is left. V<sub>SYS</sub> is 40
units long, V<sub>IN</sub> 72 and GND 104. The V<sub>IN</sub> label is 21.6
units wide and ends at 358.25, so it starts at 336.65. The name chip ends 16
units further left, at 320.65.

No diagram has a connector on the top, left or right edge yet. For one,
rotate the bottom-edge layout so the wires run away from that edge, and check
the screenshot closely.

### 7. Size the canvas

Set the viewBox to `0 0 880 <height>`. The height is the bottom of the lowest
element plus 20, rounded up to a multiple of 10. A chip's bottom is
`y + height`. A wire label is centred on its `y`, so its bottom is `y + 8`.

### 8. Write the file

Write `_includes/diagrams/<page>-<subject>.svg` in this order:

```svg
<figure class="diagram">
<svg viewBox="0 0 880 440" role="img" aria-labelledby="<name>-title">
    <title id="<name>-title">Sentences that state every fact the diagram shows.</title>

    <image class="hardware" href="/assets/images/s2-module-front.webp" x="301.5" y="20" width="277" height="280" />

    <!-- wires, then wire labels, then connector name chips -->
    <!-- leaders, then points, then callout chips and their text -->
</svg>
</figure>
```

- Keep the `<title>` id unique across the site by starting it with the file
  name.
- State in the `<title>` what an unlabelled wire is, such as "Its pin 1 is
  the VSYS output, not an input."
- Use the classes `hardware`, `wire`, `wire-label`, `sub`, `chip`,
  `chip-text`, `leader` and `point`. Never write a colour, font or stroke into
  the SVG. Every style lives in the "Diagrams" section of
  `_sass/custom/custom.scss`.
- Take every label from the page text or the datasheet tables. Don't name a
  part or a pin the page doesn't describe.

On the page, replace the image line with the include on its own line, with a
blank line above and below:

```liquid
{% include diagrams/s2-module-power-inputs.svg %}
```

### 9. Check the result

1. Check whether the user's docs server is running on port 4001:

   ```sh
   curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:4001/
   ```

   Port 4000 belongs to the website. Never stop a server you didn't start.

2. If the check didn't print `200`, start a server in the background, and stop
   only that server when you finish:

   ```sh
   nix develop -c bundle exec jekyll serve --port 4001
   ```

3. Screenshot the diagram at the docs column width, 736 pixels:

   ```sh
   name=s2-module-power-inputs
   {
       echo '<!doctype html><meta charset="utf-8"><base href="http://127.0.0.1:4001/">'
       echo '<link rel="stylesheet" href="/assets/css/just-the-docs-default.css">'
       cat _includes/head_custom.html
       echo '<div class="main-content" style="width: 736px; padding: 16px">'
       cat "_includes/diagrams/$name.svg"
       echo '</div>'
   } > "/tmp/$name.html"
   chromium --headless=new --hide-scrollbars --force-device-scale-factor=2 --window-size=776,600 --timeout=8000 --screenshot="/tmp/$name.png" "file:///tmp/$name.html"
   ```

   If the diagram is cut off, raise the window height.

4. View `/tmp/<name>.png` with the Read tool, and check that:
   - every point sits on the part it names;
   - every leader can be followed to its point, and crosses edges at an angle;
   - every pin of a wired connector has a wire, centred on the housing;
   - no label touches a wire, leader or another label;
   - no chip leaves the canvas.

   Fix anything that fails, then take the screenshot again.

On a screen narrower than 700 pixels, the diagram keeps its size and scrolls
sideways, so its text stays readable.
