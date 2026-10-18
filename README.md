# agenticsquad.dev

Source for [agenticsquad.dev](https://agenticsquad.dev), served by GitHub Pages from the `main` branch.

## Arabic page

`ar/index.html` is generated from `index.html`. After changing the English page, run:

```bash
python3 scripts/build_ar.py index.html ar/index.html
```

If an English sentence it translates has changed, the script stops and names it; update that pair in `scripts/build_ar.py`.
