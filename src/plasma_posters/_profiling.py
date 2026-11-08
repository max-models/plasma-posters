"""The scope-profiler tag of plasma_posters's profiling regions.

The regions are opt-in: :mod:`plasma_posters` registers the tag on import, so they
record nothing unless the application enables it, e.g. with
``scope_profiler.setup(enable_tags=["plasma_posters"])``.
"""

#: Tags of every plasma_posters region; the first is the opt-in tag.
PROFILE_TAGS = ("plasma_posters",)
