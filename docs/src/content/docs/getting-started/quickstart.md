---
title: Quickstart
description: Build a first poster with plasma-posters.
---

First, ensure that `plasma-posters` and a TeX distribution are
[installed](/plasma-posters/getting-started/installation/).

## A first poster

```python
from plasma_posters import Poster

poster = Poster(
    "Speeds in a thermal plasma",
    authors="Max Lindqvist",
    institute="Max Planck Institute for Plasma Physics",
    columns=2,
)
poster.block("The distribution", r"$f(v) \propto v^2 \exp(-m v^2 / 2 k_B T)$")
poster.figure(
    "Three temperatures", "maxwellian.pdf", caption="Normalised to its peak.", column=1
)
poster.build("poster.pdf")
```

`build` writes `poster.tex` next to the PDF and compiles it with lualatex. Figure paths are
relative to the `.tex` file. Blocks are stacked in their column in the order they are added;
`size` (`"a0"`, `"a1"`, `"a2"`) and `orientation` (`"portrait"`, `"landscape"`) set the paper.

## Check the layout

`preview` renders the first page of the PDF as a PNG, small enough to look at on screen:

```python
from plasma_posters import preview

preview("poster.pdf")  # writes poster.png next to it
```

It needs `pdftoppm` from [poppler](https://poppler.freedesktop.org/) (`poppler-utils` on Debian
and Ubuntu, `brew install poppler` on macOS). The [example scripts](/plasma-posters/example-scripts/)
show their posters this way.

## Edit the LaTeX by hand

`poster.save("poster.tex")` writes the LaTeX without compiling it. After editing it, compile it with

```bash
plasma-posters build poster.tex
```

See the [examples](/plasma-posters/examples/) and the
[API reference](/plasma-posters/api/plasma_posters/).

## Profiling

Compiling is a [scope-profiler](https://github.com/max-models/scope-profiler) region,
`plasma_posters.compile`, with the opt-in tag `plasma_posters`: off by default, and turned on with

```python
import scope_profiler as sp

sp.setup(enable_tags=["plasma_posters"])
```

or with `SCOPE_PROFILER_ENABLE_TAGS=plasma_posters`.
