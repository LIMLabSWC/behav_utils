"""Stimulus binning for the stats that bin on the stimulus axis.

One grid for the whole library: ``behav_utils.readouts._base`` owns it; this
module only re-exports it and adds the hard/easy threshold.
"""

from __future__ import annotations

from behav_utils.readouts._base import STIMULUS_RANGE, bin_centres, bin_edges, bin_index

DEFAULT_N_BINS = 8
HARD_THRESHOLD = 0.3          # |stimulus| below this is a "hard" trial (normalised axis)

bin_midpoints = bin_centres

__all__ = ['STIMULUS_RANGE', 'DEFAULT_N_BINS', 'HARD_THRESHOLD', 'bin_edges', 'bin_index',
           'bin_centres', 'bin_midpoints']
