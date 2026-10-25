# Silicon Witchery docs

This repository is the technical documentation for the S1 Module, S2 Module
and Superstack, served at `docs.siliconwitchery.com` with the Just the Docs
theme. Most readers are engineers integrating a module. The docs also feed the
sales funnel on `siliconwitchery.com`: a reader who would rather not build the
product themselves should find a route to consulting.

## Follow the website

`~/projects/website/CLAUDE.md` is the reference for the Silicon Witchery
brand. Read it and follow these sections:

- Art direction
- Truth in copy
- Search and answer engines
- Accessibility

The docs restyle the theme to match the website. They don't redesign it.

## Funnel

The homepage and the S1 and S2 datasheets end with a "Let us build it for you"
section. It links to a Cal.com call and to the services page. Keep its copy in
step with `services.html` on the website.

## Search

`jekyll-seo-tag` appends " | Silicon Witchery Documentation Center" (40
characters) to every `title`. Keep `title` to 20 characters, so the full title
fits the roughly 60 characters search results show.

## Technical images

Annotated hardware images, such as mastheads, pinouts and diagrams, use a
technical layout:

- Centre the hardware. Place several boards symmetrically.
- Stack labels in aligned columns with even spacing.
- Draw leader lines in moon, ending in candle dots.

This applies to diagrams only. Artistic images on the website may break the
symmetry.

`_images/` holds the template that draws the product mastheads. Use it for new
or changed annotated images, so they match the existing set.
