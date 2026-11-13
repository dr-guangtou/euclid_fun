#!/usr/bin/env bash
# Archive extra arXiv papers (Euclid cluster team: intra-cluster light and LSB photometry of extended galaxies).
# Polite to arXiv: one request every few seconds.
set -euo pipefail

archive_root="${EUCLID_ARCHIVE:-$HOME/Desktop/euclid}"
out_dir="$archive_root/papers_extra"
mkdir -p "$out_dir"

for arxiv_id in 2610.29682 2610.29683 2610.29684; do
  [ -s "$out_dir/arxiv_${arxiv_id}_abs.html" ] || { curl -sfL --max-time 60 "https://arxiv.org/abs/$arxiv_id" -o "$out_dir/arxiv_${arxiv_id}_abs.html"; sleep 4; }
  [ -s "$out_dir/arxiv_${arxiv_id}.pdf" ] || { curl -sfL --max-time 300 "https://arxiv.org/pdf/$arxiv_id" -o "$out_dir/arxiv_${arxiv_id}.pdf"; sleep 4; }
done
ls -la "$out_dir"
