table bed9Source
"Browser extensible data (9 fields) plus the source of this item."
    (
    string chrom;      "Reference sequence chromosome or scaffold"
    uint   chromStart; "Start position in chrom"
    uint   chromEnd;   "End position in chrom"
    string name;       "Genomic Mutation ID"
    uint   score;      "Not used"
    char[1] strand;    "Which DNA strand contains the observed alleles"
    string refAllele;   "Sequence of reference allele"
    string altAllele;     "Sequence of alternate allele"
    string cosmicLegIden;     "Cosmic legacy mutation identifier"
    )