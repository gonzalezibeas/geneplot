#!/usr/bin/env python

import unittest
import geneplot as gp
import shutil


class geneplottest(unittest.TestCase):

    filegff = './fruit_fly.gff3'
    iprfile = './fruit_fly.ipr'
    vcffiles = './'
    sp = 'w79_w11182w79_UPD'

    genome_1 = gp.genome(filegff, iprfile=iprfile, vcffiles=vcffiles)

    def test_Python_dependencies(self):
        import gffutils
        import os
        import subprocess
        import reportlab
        import Bio
        import matplotlib
        import logging

    def test_external_dependencies(self):
        self.assertIsNot(shutil.which('vcftools'), None, "vcftools is not installed")

    def test_functions_independently(self):
        
        genome_1 = self.genome_1
        gene1 = genome_1.gene(mRNAid='transcript:FBtr0087613', proteinid='FBpp0086739')
        self.assertIsInstance(gene1, genome_1.gene, 'class instantiation failed')
        gene1._proteindoms(self.iprfile, 'FBpp0086739')
        self.assertEqual(len(gene1.doms), 8, 'protein domain report failed')
        gene1._transcriptpos_to_genomepos()
        self.assertEqual(len(gene1.dcoors), 2955, 'protein coordinates failed')
        gene1._getsnppos(self.sp, self.vcffiles, onlycoding=False)
        self.assertEqual(len(gene1.varssall), 13, 'SNP positions failed')

        gene1.plot('Pfam', self.sp)
        shutil.move('geneplot.transcript_FBtr0087613.png', 'geneplot.full.png')

    def test_only_domains_plotting(self):

        genome_1 = self.genome_1
        gene1 = genome_1.gene(mRNAid='transcript:FBtr0087613', proteinid='FBpp0086739')
        gene1._proteindoms(self.iprfile, 'FBpp0086739')
        self.assertEqual(len(gene1.doms), 8, 'protein domain report failed')
        try:
            gene1.varssall
        except(AttributeError):
            print('varsall does not exist, as expected')

        gene1._getsnppos(self.sp, self.vcffiles, onlycoding=False)
        self.assertEqual(len(gene1.varssall), 13, 'SNP positions failed')

        gene1.plot('Pfam', sp=self.sp, onlycoding=False)
        shutil.move('geneplot.transcript_FBtr0087613.png', 'geneplot.onlydomains.png')

    def test_only_SNPs_plotting(self):

        genome_1 = self.genome_1
        gene1 = genome_1.gene(mRNAid='transcript:FBtr0087613')
        gene1._getsnppos(self.sp, self.vcffiles, onlycoding=False)
        self.assertEqual(len(gene1.varssall), 13, 'SNP positions failed')
        self.assertEqual(gene1.proteinid, None, 'proteinid attribute should not be defined')
        try:
            gene1.doms
        except(AttributeError):
            print('doms does not exist, as expected')

        gene1._proteindoms(self.iprfile, 'FBpp0086739')
        self.assertEqual(len(gene1.doms), 8, 'protein domain report failed')

        gene1.plot('Pfam', self.sp)
        shutil.move('geneplot.transcript_FBtr0087613.png', 'geneplot.onlySNPs.png')


if __name__ == '__main__':
    unittest.main()


## to run the tests, -b to avoid printing messages
## python -m unittest -v -b tests_geneplot.py


