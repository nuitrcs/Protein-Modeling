#!/usr/bin/env python3
"""Convert FASTA file(s) into AlphaFold3 input JSON.

Usage:  python fasta_to_af3_json.py input.fasta [more.fasta ...]
Output: input.json (same name and folder as each input, .json extension)

- Chain IDs come from RCSB headers ("Chains A, C" / "Chain B"); otherwise they
  are assigned A, B, C, ... in FASTA order.
- Molecule type (protein / DNA / RNA) is detected from the sequence.
- Job name = input file name without extension. Seed = 1.
"""
import json
import re
import string
import sys
from pathlib import Path


def read_fasta(path):
    header, seq = None, []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(seq)
                header, seq = line[1:], []
            else:
                seq.append(line)
    if header is not None:
        yield header, "".join(seq)


def parse_chains(header):
    """Chain IDs from an RCSB header, or None."""
    m = re.search(r"\bChains?\s+([^|]+)", header)
    if not m:
        return None
    chains = []
    for tok in m.group(1).split(","):
        tok = tok.strip()
        auth = re.match(r"^(\S+)\[auth\s+(\S+)\]$", tok)  # "A[auth H]" -> H
        chains.append(auth.group(2) if auth else tok)
    return [c for c in chains if c] or None


def mol_type(seq):
    chars = set(seq)
    if chars <= set("ACGUN") and "U" in chars and "T" not in chars:
        return "rna"
    if chars <= set("ACGTN"):
        return "dna"
    return "protein"


def convert(path):
    records = []
    for header, raw in read_fasta(path):
        seq = re.sub(r"[\s\-\.\*]", "", raw).upper()
        if seq:
            records.append((parse_chains(header), seq))

    used = {c for chains, _ in records if chains for c in chains}
    free = (c for c in string.ascii_uppercase if c not in used)

    sequences = []
    for chains, seq in records:
        chains = chains or [next(free)]
        sequences.append({mol_type(seq): {"id": chains, "sequence": seq}})
    sequences.sort(key=lambda s: next(iter(s.values()))["id"][0])

    return {
        "name": re.sub(r"[^\w.\-]+", "_", Path(path).stem),
        "sequences": sequences,
        "modelSeeds": [1],
        "dialect": "alphafold3",
        "version": 1,
    }


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for path in sys.argv[1:]:
        out = Path(path).with_suffix(".json")
        out.write_text(json.dumps(convert(path), indent=2) + "\n")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
