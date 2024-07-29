import csv
from os.path import isfile
from typing import Optional

import click
from loguru import logger

SUPPORTED_FORMATS = ["tsv", "gz"]
OUTFORMAT = ".bed"
COL_ORDER = [
    "CHROMOSOME",
    "GENOME_START",
    "GENOME_STOP",
    "GENE_SYMBOL",
    "NAME",
    "COSMIC_GENE_ID",
    "SOMATIC",
    "GERMLINE",
    "TUMOUR_TYPES_SOMATIC",
    "TUMOUR_TYPES_GERMLINE",
    "CANCER_SYNDROME",
    "TISSUE_TYPE",
    "MOLECULAR_GENETICS",
    "ROLE_IN_CANCER",
    "MUTATION_TYPES",
    "TRANSLOCATION_PARTNER",
    "OTHER_GERMLINE_MUT",
    "OTHER_SYNDROME",
    "TIER",
    "SYNONYMS",
]


def convert_tsv(infile: str, outfile: str) -> None:
    """Convert an uncompressed TSV file.."""
    with open(infile, "r", newline="") as fin, open(outfile, "w", newline="") as fout:
        reader = csv.DictReader(fin, delimiter="\t")
        writer = csv.DictWriter(fout, delimiter='\t', fieldnames=COL_ORDER, extrasaction='ignore')
        writer.writeheader()
        for row in reader:
            writer.writerow(row)


def set_outfile(infile: str, outfile: Optional[str], in_format: str) -> str:
    """Set name/path to the outfile."""
    if outfile and outfile.endswith(OUTFORMAT):
        return outfile
    elif outfile:
        return f"{outfile}{OUTFORMAT}"
    else:
        return OUTFORMAT.join(infile.rsplit(in_format, 1))


@click.command()
@click.option(
    "--infile", "-i", required=True, help="Path to the COSMIC-formatted infile"
)
@click.option("--outfile", "-o", required=False, help="Outfile name")
def main(infile: str, outfile: Optional[str] = None):
    if isfile(infile) is False:
        logger.error("Path to COSMIC file is not valid.")
        return

    in_format: str = infile.rsplit(".")[-1]
    if not in_format in SUPPORTED_FORMATS:
        logger.error(
            "File format not valid. Infile format should be '.tsv' or '.tsv.gz'."
        )
    outfile: str = set_outfile(
        infile=infile, outfile=outfile, in_format=f".{in_format}"
    )
    logger.info(f"Converting '{infile}' to '{outfile}'.")

    if in_format == "tsv":
        convert_tsv(infile=infile, outfile=outfile)
