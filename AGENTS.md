# Strawn Repository Guidance

Strawn is Moriatz's original variable typeface, publishable font package, and public specimen website.

## Scope

- Keep this repository focused on the Strawn font and its specimen.
- Keep the canonical font source and npm package under `packages/font`.
- Make the website consume `@moriatz-labs/strawn` through the workspace; do not duplicate generated font files under `website`.
- Do not add component, icon, token, theme, or design-system packages.
- Preserve the canonical font family name, weight axis, metrics, download link, and accessibility of the specimen tools.
- Preserve committed font artifacts and proofs according to `packages/font/AGENTS.md`.

## Delivery

Use reviewed pull requests. Production deployment happens only through GitHub Actions after all required checks pass.
