import csv
from os import system
from os.path import isfile
from typing import Optional

import click
from importlib_resources import files
from loguru import logger

SUPPORTED_FORMATS = ["tsv", "gz"]
OUTFORMAT = ".bed"
COL_ORDER = [
    "CHROMOSOME",
    "GENOME_START",
    "GENOME_STOP",
    "GENOMIC_MUTATION_ID",
    "SCORE",
    "STRAND",
    "GENOMIC_WT_ALLELE",
    "GENOMIC_MUT_ALLELE",
    "LEGACY_MUTATION_ID",
]
SCORE_VALUE = 0
RESOURCES_PATH = "cosmic2bed.resources"
BUILD_CHROM_LENGTHS = {
    "37": str(files(RESOURCES_PATH).joinpath("GRCh37.chrom.sizes.txt")),
    "38": str(files(RESOURCES_PATH).joinpath("GRCh38.chrom.sizes.txt")),
}
SCRIPTS_PATH = "cosmic2bed.scripts"
BED2BIGBED_PATH = str(files(SCRIPTS_PATH).joinpath("bedToBigBed"))


def convert_tsv(infile: str, outfile: str, build: str) -> None:
    """Convert an uncompressed TSV file.."""

    # Export columns in the right order
    with open(infile, "r", newline="") as fin, open(outfile, "w", newline="") as fout:
        reader = csv.DictReader(fin, delimiter="\t")
        writer = csv.DictWriter(
            fout, delimiter="\t", fieldnames=COL_ORDER, extrasaction="ignore"
        )
        for row in reader:
            row["SCORE"] = SCORE_VALUE  # Replace missing value
            if "STRAND" not in row:  # Non-coding variants have no strand
                row["STRAND"] = "."
            for allele in [
                "GENOMIC_WT_ALLELE",
                "GENOMIC_MUT_ALLELE",
            ]:  # field length must not exceed 255 characters
                if len(row[allele]) >= 255:
                    row[allele] = row[allele][:255]

            if "" in [
                row["CHROMOSOME"],
                row["GENOME_START"],
                row["GENOME_STOP"],
            ]:  # Chromosome coordinates should be present
                continue
            elif (
                row["GENOME_START"] > row["GENOME_STOP"]
            ):  # Remove position with weird coordinates
                continue

            writer.writerow(row)

    # Sort by coordinates:
    cmd = (
        f"cat {outfile} | sort -k1,1V -k2,2n > {outfile.replace('.bed', '_sorted.bed')}"
    )
    system(cmd)

    # Convert to bigbed --> Doesn't work yet
    """
    cmd = f". {BED2BIGBED_PATH} -type=bed6+3 {outfile.replace('.bed', '_sorted.bed')} {BUILD_CHROM_LENGTHS[build]} {outfile.replace('.bed', '.bb')} -tab"
    logger.warning(cmd)
    system(cmd)
    """


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
@click.option(
    "--build",
    "-b",
    type=click.Choice(["37", "38"]),
    required=True,
    help="Genomic build",
)
@click.option("--outfile", "-o", required=False, help="Outfile name")
def main(infile: str, build: str, outfile: Optional[str] = None):
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
        convert_tsv(infile=infile, outfile=outfile, build=build)
