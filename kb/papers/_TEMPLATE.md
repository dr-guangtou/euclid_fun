---
title: "<full paper title>"
short_name: <pdf stem, e.g. kuemmel>
first_author: <surname>
series: A&A Special Issue DR1-Foundation (Nov 2026)   # or "arXiv (Euclid Q1 cluster/ICL)" for the extra papers
local_pdf: ~/Desktop/euclid/papers/<stem>.pdf
local_text: ~/Desktop/euclid/text/papers/<stem>.txt
topics: [comma, separated, keywords]
relevance_extended_galaxies: high | medium | low   # for photometry / 2-D modelling / LSB of low-to-intermediate-z galaxies
---

# <Short descriptive title> (<First author> et al. 2026)

## TL;DR
3-6 sentences: what the paper delivers and why a galaxy-imaging user should care.

## Key facts and numbers
Bullets with concrete values (depths, pixel scales, PSF FWHM, areas, counts, accuracies, versions,
dates, tile sizes, zero points, ...). Cite pages as (p. N).

## Data products and data model
Every product/table/file/HDU/column/flag the paper defines or relies on: name, content, units,
format, where to get it (archive table, product type). Write "none" if not applicable.

## Processing and methods
The pipeline steps or analysis methods, in order, with the important algorithmic choices
(e.g. background estimation scale, masking, PSF modelling, detection thresholds, deblending).

## Validation and performance
How quality was assessed and the resulting metrics.

## Known issues, caveats, limitations
Everything a user could trip over (artefacts, biases, bugs, missing data, regions to avoid,
flags to apply), with page references.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
Concrete consequences and recommendations for our use case (low-to-intermediate-z galaxies,
surface-brightness profiles, Sersic/bulge-disc modelling, tidal features, stellar haloes, ICL).
Say explicitly when the paper is irrelevant to this.

## Practical recommendations for users
Actionable do/don't list (columns to use, flags to cut on, products to prefer).

## Objects, fields and figures worth revisiting
- Named galaxies/objects/fields shown or studied, with coordinates (RA, Dec in deg) and type
  (spiral, early-type, dwarf, LSB, edge-on, interacting, lens, cluster, ...) when given.
- Key figures/tables to look at, with page numbers.

## Cross-references
Other DR1 papers or Explanatory Supplement chapters this paper depends on.
