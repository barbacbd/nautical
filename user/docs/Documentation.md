# API Documentation

API documentation is auto-generated from Python docstrings using [Sphinx](https://www.sphinx-doc.org/) and deployed to GitHub Pages on every push to `master`.

**Live docs**: [barbacbd.github.io/nautical](https://barbacbd.github.io/nautical/)

## Building locally

```bash
make docs
```

This runs `sphinx-apidoc` to generate API stubs from the source, then `sphinx-build` to produce HTML. Open `docs/build/html/index.html` to view the result.

## How it works

- The CI workflow (`.github/workflows/docs.yml`) builds Sphinx HTML and deploys it directly to GitHub Pages via `actions/deploy-pages` — no separate branch needed.
- The repo's **Settings > Pages > Source** must be set to **GitHub Actions** for deployment to work.
- `docs/conf.py` configures Sphinx with the `sphinx_rtd_theme` theme, `autodoc` for extracting docstrings, and `napoleon` for Google/NumPy-style docstring support.

## Cleaning up

```bash
make clean
```

This removes `docs/build/` and `docs/source/` along with other build artifacts.
