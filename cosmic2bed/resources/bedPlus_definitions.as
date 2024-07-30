table bed9Source
"Browser extensible data (9 fields) plus the source of this item."
    (
    string chrom;      "Chromosome (or contig, scaffold, etc.)"
    uint   chromStart; "Start position in chromosome"
    uint   chromEnd;   "End position in chromosome"
    string name;       "Genomic mutation identifier (COSV)"
    uint   score;      "Score from 0-1000"
    char[1] strand;    "+ or -"
    string wt_allele;   "Genomic Wild type allele sequence"
    string mut_allele;     "Genomic mutation allele sequence"
    string legacy_mut_id;     "Legacy mutation identifier (COSM) or (COSN)"
    )