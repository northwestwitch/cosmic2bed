# cosmic2bed
Convert TSV COSMIC format to bed

Created files correspond to the UCSC COSMIC tracks described [here](https://genome.ucsc.edu/cgi-bin/hgTables?db=hg38&hgta_group=phenDis&hgta_track=cosmicMuts&hgta_table=cosmicMuts&hgta_doSchema=describe+table+schema)

## Howto

### Install this software
1. Create a conda environment with Python 3 -> `conda create -n py3 python=3.11`
1. Activate the environment -> `conda activate py3`
1. Clone this repository -> `git clone https://github.com/northwestwitch/cosmic2bed.git`
1. Enter cloned folder -> `cd cosmic2bed`
1. Install poetry -> `pip install poetry`
1. Install this software -> `poetry install`
1. Make sure the script works -> `poetry run cosmic2bed --help`

<img width="522" alt="image" src="https://github.com/user-attachments/assets/c77aba42-2a72-402d-bc3e-d9a924aae930">


### COSMIC data availability
Cosmic data should be downloaded from [COSMIC](https://cancer.sanger.ac.uk/cosmic/download/cosmic). Note that you need to register as a non-commercial user or have a commercial license in order to download COSMIC data.

### Howto using demo data
Demo data present in this repository consists of 2 files: `Cosmic_MutantCensus_v100_GRCh38.tsv` and `Cosmic_NonCodingVariants_v100_GRCh38.tsv`, both present in the [.tar sample download](https://cog.sanger.ac.uk/cosmic-downloads-production/taster/example_grch38.tar) in build 38 obtained from COSMIC.
These files can be found in the `cosmic2bed/demo/infiles` folder.

#### Convert a demo .tsv to a sorted bed
[Demo outfiles](https://github.com/northwestwitch/cosmic2bed/tree/master/cosmic2bed/demo/outfiles) were created in this way:
```
poetry run cosmic2bed -i cosmic2bed/demo/infiles/Cosmic_MutantCensus_v100_GRCh38.tsv -o cosmic2bed/demo/outfiles/Cosmic_MutantCensus_v100_GRCh38.bed --build 38
```
This command will convert the .tsv file to a 6+3 BED file.

### Convert the sorted BED to bigbed
The sorted BED file created in the step above can be converted to bigbed using the [bedToBigBed utility from UCSC](http://hgdownload.cse.ucsc.edu/admin/exe/). The utility can also be installed using [conda](https://anaconda.org/bioconda/ucsc-bedtobigbed).
In this example I've used the script present in the `cosmic2bed/scripts` folder (don't use it and download the script specific for your architecture from UCSC instead) and runned the following command:
```
./cosmic2bed/scripts/bedToBigBed -type=bed6+3 -as=<path-to-bedplus-definitions> <path-to-sorted-bed-infile> <path-to-chrom-sizes> <path-to-sorted-bigbed-outfile> -tab
```

- `path-to-bedplus-definitions`: use the path to `cosmic2bed/resources/bedPlus_definitions.as`
- `path-to-sorted-bed-infile`: it's the sorted BED file obtained in the step above
- `path-to-chrom-sizes`: A file with chromosome sizes is present in this repository under cosmic2bed/resources. Choose the right genome build.
- `path-to-sorted-bigbed-outfile`: It's the outfile, for instance `Cosmic_MutantCensus_v100_GRCh38.bb`
