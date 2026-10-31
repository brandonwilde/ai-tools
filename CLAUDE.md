# Branches, PRs, and releases

Release Drafter keeps a draft GitHub Release listing each merged PR by title, so
**PR titles are release-note lines**: write them for someone importing the
package.

PR labels set the section and the version bump. They are applied automatically
from the branch prefix:

| Branch prefix | Label | Bump |
| --- | --- | --- |
| `feat/` | `enhancement` | minor |
| `fix/` | `bug` | patch |
| `docs/` | `documentation` | patch |
| `chore/`, `ci/`, `build/`, `refactor/`, `test/` | `chore` | patch |

Add `breaking` by hand for incompatible API changes (major bump), and
`skip-changelog` for PRs that shouldn't appear in the notes.

The package version comes from the latest git tag via setuptools-scm. Don't add
a version string to `setup.py`; publishing the draft release creates the tag.
