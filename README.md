# wikitexthtml

[![GitHub License](https://img.shields.io/github/license/TrueBrain/wikitexthtml)](https://github.com/TrueBrain/wikitexthtml/blob/master/LICENSE)
[![GitHub Tag](https://img.shields.io/github/v/tag/TrueBrain/wikitexthtml?include_prereleases&label=stable)](https://github.com/TrueBrain/wikitexthtml/releases)
[![GitHub commits since latest release](https://img.shields.io/github/commits-since/TrueBrain/wikitexthtml/latest/master)](https://github.com/TrueBrain/wikitexthtml/commits/master)

[![GitHub Workflow Status (Testing)](https://img.shields.io/github/workflow/status/TrueBrain/wikitexthtml/Testing/master?label=master)](https://github.com/TrueBrain/wikitexthtml/actions?query=workflow%3ATesting)
[![GitHub Workflow Status (Release)](https://img.shields.io/github/workflow/status/TrueBrain/wikitexthtml/Release?label=release)](https://github.com/TrueBrain/wikitexthtml/actions?query=workflow%3A%22Release%22)

wikitexthtml is a library that renders HTML from WikiText.

## Dependencies

- Python3.8 or higher.
- `python-slugify` (via `setup.py`), for slugs in anchors
- `ply` (via `setup.py`), to implement `{{#ifexpr}}` and `{{#expr}}`
- `wikitextparser` (via `setup.py`), to make sense of wikitext

## Installation

```bash
pip install wikitexthtml
```

Or for development work:

```bash
python3 -m venv .env
.env/bin/pip install -e .
```

## Usage

Extend [Page](https://github.com/TrueBrain/wikitexthtml/blob/master/wikitexthtml/page.py) by implementing the missing functions as seen in [prototype.py](https://github.com/TrueBrain/wikitexthtml/blob/master/wikitexthtml/prototype.py).
This way you can customize where files are read from (from disk, from a database, etc) and how to sanitize titles and URLs.
In the [tests](https://github.com/TrueBrain/wikitexthtml/tree/master/tests/) folder examples of this can be found.

Now you can instantiate this new class and call `render()` on it.
The result will be available in `html`. For example:

```python
class WikiPage(Page):
    ...

print(WikiPage("Main Page").render().html)
```
