#!/usr/bin/env bash
# Archive the Euclid DR1 documentation into ~/Desktop/euclid (idempotent; skips files already present).
# Afterwards run: uv run python -I scripts/extract_text.py
set -euo pipefail

archive_root="${EUCLID_ARCHIVE:-$HOME/Desktop/euclid}"
mkdir -p "$archive_root"/{papers,papers_q1,web,docs,expsup_mirror,dpdd_mirror,listing}

download() {  # url output_path
  [ -s "$2" ] || { curl -sfL --max-time 300 "$1" -o "$2" && sleep 1; } || echo "FAILED: $1"
}

# 1. A&A Special Issue for DR1-Foundation (November 2026): PDFs listed on the ECEB public page.
curl -sL --max-time 60 https://eceb.astro.uni-bonn.de/public/ -o "$archive_root/listing/eceb_public.html"
python3 -I - "$archive_root/listing/eceb_public.html" > "$archive_root/listing/dr1_paper_links.txt" <<'EOF'
import re, sys
text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
start = text.find("DR1-Foundation")
segment = text[start:]
stop = segment.find("Special Issue", 50)
segment = segment[: stop if stop > 0 else len(segment)]
for link in dict.fromkeys(re.findall(r"href='(dr1/[^']+\.pdf)'", segment)):
    print(link)
EOF
while read -r link; do
  download "https://eceb.astro.uni-bonn.de/public/$link" "$archive_root/papers/$(basename "$link")"
done < "$archive_root/listing/dr1_paper_links.txt"

# 1b. Q1 coordinated-release papers that the DR1 Explanatory Supplement cites as the detailed
#     description of the VIS, NIR and MER processing used for DR1.
for name in romelli_etal mccracken_etal polenta_etal; do
  download "https://eceb.astro.uni-bonn.de/public/coordinated_release/$name.pdf" "$archive_root/papers_q1/$name.pdf"
done

# 2. ESA web pages about DR1, the astroquery module documentation (docs.astropy.org sits behind a
#    Cloudflare browser check, so the reStructuredText source is fetched from GitHub instead).
fetch_page() {  # url output_name
  [ -s "$archive_root/web/$2" ] || curl -sL --max-time 60 "$1" -o "$archive_root/web/$2"
}
fetch_page https://www.cosmos.esa.int/web/euclid/euclid-dr1 cosmos_euclid_dr1.html
fetch_page https://www.cosmos.esa.int/web/euclid/dr1-data cosmos_dr1_data.html
fetch_page https://www.cosmos.esa.int/web/euclid/dr1-documentation cosmos_dr1_documentation.html
fetch_page https://www.cosmos.esa.int/web/euclid/dr1-papers cosmos_dr1_papers.html
fetch_page https://www.cosmos.esa.int/web/euclid/est-publications cosmos_est_publications.html
fetch_page https://euclid.dataspace.esa.int/community/help-pages/Euclid_Science_Archive_User_Guide.html eds_science_archive_user_guide.html
fetch_page https://euclid.dataspace.esa.int/community/help-pages/EDS_Portal_Help.html eds_portal_help.html
fetch_page https://euclid.caltech.edu/ ensc_ipac_home.html
fetch_page https://raw.githubusercontent.com/astropy/astroquery/main/docs/esa/euclid/euclid.rst astroquery_esa_euclid.rst

# 3. Memos: DR1 product memo and the Science Archive list of supported data products.
download "https://www.cosmos.esa.int/documents/10647/12245842/DR1-memo_260922.pdf" "$archive_root/docs/DR1-memo_260922.pdf"
download "https://www.cosmos.esa.int/documents/10647/19912696/EUCL-ESAC-RP-8-017+-+List+of+supported+data+products-v42-20260730_080821.pdf" \
  "$archive_root/docs/EUCL-ESAC-RP-8-017_list_of_supported_data_products_v42.pdf"

# 4. Explanatory Supplement (LaTeXML HTML site) and the DR1 Data Product Definition Document (Sphinx).
wget --mirror --no-parent --page-requisites --adjust-extension --convert-links \
  --wait=0.3 --random-wait --quiet --no-host-directories --cut-dirs=3 \
  -P "$archive_root/expsup_mirror" https://euclid.esac.esa.int/dr/dr1/expsup/ || true
wget --mirror --no-parent --page-requisites --adjust-extension --convert-links \
  --wait=0.2 --random-wait --quiet --no-host-directories --cut-dirs=3 -R '*.fits,*.gz,*.tar,*.zip' \
  -P "$archive_root/dpdd_mirror" https://euclid.esac.esa.int/dr/dr1/dpdd/ || true

echo "papers: $(ls "$archive_root/papers" | wc -l)  q1: $(ls "$archive_root/papers_q1" | wc -l)  web: $(ls "$archive_root/web" | wc -l)  docs: $(ls "$archive_root/docs" | wc -l)"
