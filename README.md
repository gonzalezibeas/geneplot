# mock
## Geneplot library

A Python library for plotting single nucleotide polymorhpysm (SNP) data and 
protein domain information on the exon-intron structure of a gene. For more 
details about features and implementation see the associated document:



## Code availability



## installation

pip install geneplot

## documentation



## Get started
Plot geneID (from the GFF3 file) and proteinID domains (from IPR file)
and SNPs listed on sample_ID from the VCF files directory.

```Python
import geneplot as gp

#input data
filegff = '/path-to-data/file.gff'
fileipr = '/path-to-data/file.ipr'
filevcf = '/path-to-data/vcfs/'

# class instantiation (gene object)
gene1 = gp.gene('geneID', 'proteinID', filegff, fileipr, filevcf)

# plot
gene1.plot('sample_ID', 'Pfam')
´´´


