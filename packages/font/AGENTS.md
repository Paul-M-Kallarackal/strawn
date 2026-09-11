# Strawn Typeface Package Guidance

`packages/font` is Moriatz Labs' canonical Strawn variable typeface package.

## Source and artifacts

- `scripts/build.py` is the source of truth for glyph construction, interpolation masters, metadata, packaged CSS, and specimen artwork.
- Keep the family original. Do not import, trace, rename, or derive outlines from third-party fonts.
- Preserve the tapered toothpick construction across all masters while keeping the Regular master dark enough for interface text.
- Commit the generated `dist/` files because Git and GitHub installs consume the package directly.
- Commit the generated Moriatz Labs PNG and SVG files under `proofs/`.

## Quality

- Use the package scripts, which run pinned dependencies in a uv-managed Python 3.12 environment.
- Run `bun run build` followed by `bun run test` from `packages/font`.
- Confirm the variable `wght` axis remains 100–700 with a default of 500 Dense.
- Visually inspect the Moriatz Labs proof after every glyph or interpolation change.

## Release

- Font software and sources remain under OFL-1.1.
- Tag releases with semantic versions.
- Attach the variable TTF, variable WOFF2, Fine, Signature, Dense, and Structural TTFs, manifests, and Moriatz Labs proof to each GitHub release.
