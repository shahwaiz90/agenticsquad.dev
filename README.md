# agenticsquad.dev

Source for [agenticsquad.dev](https://agenticsquad.dev), served by GitHub Pages from the `main` branch.

## Arabic page

`ar/index.html` is generated from `index.html`. After changing the English page, run:

```bash
python3 scripts/build_ar.py index.html ar/index.html
```

If an English sentence it translates has changed, the script stops and names it; update that pair in `scripts/build_ar.py`.

## Shared head, header and footer

GitHub Pages builds the site with Jekyll. Every page starts with an empty front matter block (`---` twice) and pulls in:

- `_includes/head.html`: icons, theme script and Google Analytics (`ga_title` sets the page title sent to Analytics)
- `_includes/header.html`: logo, section links, language switch and theme button (`lang`, `home`, `alt`)
- `_includes/footer.html`: licence, LinkedIn, sitemap and llms.txt links (`lang`)
- `_includes/chrome-css.html`: the styles for the header and footer, included inside each page's `<style>`

Change the header or footer once there and every page picks it up. To preview locally, run `bundle exec jekyll serve` with Jekyll 3.10 (the version GitHub Pages uses).
