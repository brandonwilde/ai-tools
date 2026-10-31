# Commits and PRs

Every commit uses [Conventional Commits](https://www.conventionalcommits.org):
`<type>(<optional scope>): <summary>`, with `!` after the type/scope for
breaking changes. CI rejects PRs containing commits that don't match, and
release-please derives version bumps and the changelog from them.

- `feat` — new capability for library users (minor bump)
- `fix` — bug fix (patch bump)
- `feat!` / `fix!` — breaking change to the public API (minor bump while on 0.x)
- `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `style`, `revert`
  — everything else

Commit subjects become changelog lines, so write them for someone importing
the package.

Feature branches PR into `main`. Don't edit the version in `setup.py`,
`CHANGELOG.md`, or `.release-please-manifest.json` by hand; merging the
release-please Release PR does that.
