#!/usr/bin/env python

import unittest
import geneplot as gp
import shutil


class geneplottest(unittest.TestCase):

    filegff = '/home/user01/data/genomes/droso/FBpp0086739.gff3'
    fileipr = '/home/user01/data/genomes/droso/FBpp0086739.ipr'
    pathvcfs = '/home/user01/data/genomes/droso/vcfs'
    sp = 'w79_w11182w79_UPD'

    def test_list(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

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
        
        gene1 = gp.gene('transcript:FBtr0087613', self.filegff, 'FBpp0086739', self.fileipr, self.pathvcfs)
        self.assertIsInstance(gene1, gp.gene, 'class instantiation failed')
        gene1._proteindoms(self.fileipr, 'FBpp0086739')
        self.assertEqual(len(gene1.doms), 8, 'protein domain report failed')
        gene1._transcriptpos_to_genomepos()
        self.assertEqual(len(gene1.coor), 2955, 'protein coordinates failed')
        gene1._getsnppos(self.sp, self.pathvcfs)
        self.assertEqual(len(gene1.varssall), 13, 'SNP positions failed')

        gene1.plot('Pfam', self.sp)
        shutil.move('geneplot.transcript:FBtr0087613.png', 'geneplot.full.png')

    def test_only_domains_plotting(self):
        gene1 = gp.gene('transcript:FBtr0087613', self.filegff, 'FBpp0086739', self.fileipr)
        gene1._proteindoms(self.fileipr, 'FBpp0086739')
        self.assertEqual(len(gene1.doms), 8, 'protein domain report failed')
        self.assertEqual(gene1.vcffiles, None, 'vcffiles attribute should not be defined')
        try:
            gene1.varssall
        except(AttributeError):
            print('varsall does not exist, as expected')

        gene1._getsnppos(self.sp, self.pathvcfs)
        self.assertEqual(len(gene1.varssall), 13, 'SNP positions failed')

        gene1.plot('Pfam', self.sp)
        shutil.move('geneplot.transcript:FBtr0087613.png', 'geneplot.onlydomains.png')

    def test_only_SNPs_plotting(self):
        gene1 = gp.gene('transcript:FBtr0087613', self.filegff, vcffiles=self.pathvcfs)
        gene1._getsnppos(self.sp, self.pathvcfs)
        self.assertEqual(len(gene1.varssall), 13, 'SNP positions failed')
        self.assertEqual(gene1.proteinid, None, 'proteinid attribute should not be defined')
        self.assertEqual(gene1.iprfile, None, 'iprfile attribute should not be defined')
        try:
            gene1.doms
        except(AttributeError):
            print('doms does not exist, as expected')

        gene1._proteindoms(self.fileipr, 'FBpp0086739')
        self.assertEqual(len(gene1.doms), 8, 'protein domain report failed')

        gene1.plot('Pfam', self.sp)
        shutil.move('geneplot.transcript:FBtr0087613.png', 'geneplot.onlySNPs.png')


if __name__ == '__main__':
    unittest.main()


## to run the tests, -b to avoid printing messages
## python -m unittest -v -b tests_geneplot.py


