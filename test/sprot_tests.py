#!/usr/bin/env python

import unittest
import io
from src.annotation import Annotation
from src.sprot import read_sprot, get_gff_info

class TestSprot(unittest.TestCase):

    def setUp(self):
        self.blast_file = io.StringIO(\
        'm.4830	sp|Q5AZY1|MRH4_EMENI	32.65	49	33	0	114	162	500	548	0.56	34.3')

        self.gff_file = io.StringIO(\
                'comp9975_c0_seq1	.	mRNA	25	603	.	+	.	ID=m.4830;Parent=g.4830')

        self.fasta_file = io.StringIO(\
                '>sp|Q5AZY1|MRH4_EMENI ATP-dependent RNA helicase mrh4, mitochondrial OS=Emericella nidulans (strain FGSC A4 / ATCC 38163 / CBS 112.46 / NRRL 194 / M139) GN=mrh4 PE=3 SV=1\n\
MNRLGGLSLPLRPVCLFCRAQTSLALSPLQGGQAVRSIATGRLRRRARMTLSKDVAKSSL\n\
KPKRTDRGKLGPFPNMNQTRARVREDPRSRSPAALKRSGETEEKPAMNTESPLYKALKMQ\n\
TALAPISYGKRTAIKAKIAEITSFDAFTLLPIVRNSIFSQALPGIADAVPTPIQRVAIPR\n\
LLEDAPAKKQAKKVDDDEPQYEQYLLAAETGSGKTLAYLIPVIDAIKRQEIQEKEMEKKE\n\
EERKVREREENKKNQAFDLEPEIPPPSNAGRPRAIILVPTAELVAQVGAKLKAFAHTVKF\n\
RSGIISSNLTPRRIKSTLFNPAGIDILVSTPHLLASIAKTDPYVLSRVSHLVLDEADSLM\n\
DRSFLPISTEVISKAAPSLQKLIFCSATIPRSLDSQLRKLYPDIWRLTTPNLHAIPRRVQ\n\
LGVVDIQKDPYRGNRNLACADVIWSIGKSGAGSDEAGSPWSEPKTKKILVFVNEREEADE\n\
VAQFLKSKGIDAHSFNRDSGTRKQEEILAEFTEPAAVPTAEEILLARKQQQRENINIPFV\n\
LPERTNRDTERRLDGVKVLVTTDIASRGIDTLALKTVILYHVPHTTIDFIHRLGRLGRMG\n\
KRGRAVVLVGKKDRKDVVKEVREVWFGLDS')
        
        
    def test_read_sprot(self):
        sprot_list = read_sprot(self.blast_file, self.gff_file, self.fasta_file)
        expected = [Annotation("g.4830", "name", "mrh4"), Annotation("m.4830", "product", "ATP-dependent RNA helicase mrh4, mitochondrial")]
        self.assertEquals(sprot_list, expected)

    def test_read_sprot_missing_gene_name(self):
        self.fasta_file = io.StringIO(\
                '>sp|Q5AZY1|MRH4_EMENI ATP-dependent RNA helicase mrh4, mitochondrial OS=Emericella nidulans (strain FGSC A4 / ATCC 38163 / CBS 112.46 / NRRL 194 / M139) PE=3 SV=1\n\
MNRLGGLSLPLRPVCLFCRAQTSLALSPLQGGQAVRSIATGRLRRRARMTLSKDVAKSSL\n\
KPKRTDRGKLGPFPNMNQTRARVREDPRSRSPAALKRSGETEEKPAMNTESPLYKALKMQ\n\
TALAPISYGKRTAIKAKIAEITSFDAFTLLPIVRNSIFSQALPGIADAVPTPIQRVAIPR\n\
LLEDAPAKKQAKKVDDDEPQYEQYLLAAETGSGKTLAYLIPVIDAIKRQEIQEKEMEKKE\n\
EERKVREREENKKNQAFDLEPEIPPPSNAGRPRAIILVPTAELVAQVGAKLKAFAHTVKF\n\
RSGIISSNLTPRRIKSTLFNPAGIDILVSTPHLLASIAKTDPYVLSRVSHLVLDEADSLM\n\
DRSFLPISTEVISKAAPSLQKLIFCSATIPRSLDSQLRKLYPDIWRLTTPNLHAIPRRVQ\n\
LGVVDIQKDPYRGNRNLACADVIWSIGKSGAGSDEAGSPWSEPKTKKILVFVNEREEADE\n\
VAQFLKSKGIDAHSFNRDSGTRKQEEILAEFTEPAAVPTAEEILLARKQQQRENINIPFV\n\
LPERTNRDTERRLDGVKVLVTTDIASRGIDTLALKTVILYHVPHTTIDFIHRLGRLGRMG\n\
KRGRAVVLVGKKDRKDVVKEVREVWFGLDS')
        sprot_list = read_sprot(self.blast_file, self.gff_file, self.fasta_file)
        expected = [Annotation("g.4830", "name", "MRH4"), Annotation("m.4830", "product", "ATP-dependent RNA helicase mrh4, mitochondrial")]
        self.assertEquals(sprot_list, expected)

    def test_get_gff_info(self):
        test_gff = io.StringIO('comp9975_c0_seq1	.	mRNA	25	603	.	+	.	foo=dog;Parent=g.4830;bazz=bub;ID=m.4830')
        expected = {"m.4830" : "g.4830"}
        self.assertEquals(get_gff_info(test_gff), expected)


##########################
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSprot))
    return suite

if __name__ == '__main__':
    unittest.main()
