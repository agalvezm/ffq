from unittest import mock, TestCase
from unittest.mock import call

from bs4 import BeautifulSoup

import ffq.ffq as ffq
from tests.mixins import TestMixin


class TestFfq(TestMixin, TestCase):


    def test_validate_accession(self):
        SEARCH_TYPES = ('SRR', 'ERR', 'DRR', 'SRP', 'ERP', 'DRP', 'SRX', 'GSE','GSM', 'DOI')
        self.assertEqual([('SRR', 'SRR244234'),
                            False,
                            ('DOI', '10.1016/j.cell.2018.06.052'),
                            False,
                            ('GSM', 'GSM12345'),
                            ('GSE', 'GSE567890')
        ], ffq.validate_accession(["SRR244234", "SRT44322", '10.1016/j.cell.2018.06.052',
                                   'ASA10.1016/j.cell.2018.06.052', "GSM12345", "GSE567890"],
                                   SEARCH_TYPES))


    def test_parse_run(self):
        with mock.patch('ffq.ffq.cached_get') as cached_get:
            with open(self.fastqs_path, 'r') as f:
                cached_get.return_value = f.read()
            with open(self.run_path, 'r') as f:
                soup = BeautifulSoup(f.read(), 'xml')
            self.assertEqual({
                'accession':
                    'SRR8426358',
                'experiment':
                    'SRX5234128',
                'study':
                    'SRP178136',
                'sample':
                    'SRS4237519',
                'title':
                    'Illumina HiSeq 4000 paired end sequencing; GSM3557675: old_Dropseq_1; Mus musculus; RNA-Seq',
                'files': [{
                    'url':
                        'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR842/008/SRR8426358/SRR8426358_1.fastq.gz',
                    'md5':
                        'be7e88cf6f6fd90f1b1170f1cb367123',
                    'size':
                        '5507959060'
                }, {
                    'url':
                        'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR842/008/SRR8426358/SRR8426358_2.fastq.gz',
                    'md5':
                        '2124da22644d876c4caa92ffd9e2402e',
                    'size':
                        '7194107512'
                }],
                'attributes': {
                    'ENA-SPOT-COUNT': '109256158',
                    'ENA-BASE-COUNT': '21984096610',
                    'ENA-FIRST-PUBLIC': '2019-01-27',
                    'ENA-LAST-UPDATE': '2019-01-27'
                }         
            }, ffq.parse_run(soup))

    def test_parse_run_bam(self):
        with mock.patch('ffq.ffq.cached_get') as cached_get:
            with open(self.fastqs2_path, 'r') as f1, open(self.bam_path,
                                                          'r') as f2:
                cached_get.side_effect = [f1.read(), f2.read()]
            with open(self.run2_path, 'r') as f:
                soup = BeautifulSoup(f.read(), 'xml')

            self.assertEqual({
                'accession':
                    'SRR6835844',
                'experiment':
                    'SRX3791763',
                'study':
                    'SRP131661',
                'sample':
                    'SRS3044236',
                'title':
                    'Illumina NovaSeq 6000 sequencing; GSM3040890: library 10X_P4_0; Mus musculus; RNA-Seq',
                'files': [{
                    'url':
                        'ftp://ftp.sra.ebi.ac.uk/vol1/SRA653/SRA653146/bam/10X_P4_0.bam',
                    'md5':
                        '5355fe6a07155026085ce46631268ab1',
                    'size':
                        '17093057664'
                }, {
                    'url':
                        'ftp://ftp.sra.ebi.ac.uk/vol1/run/SRR683/SRR6835844/10X_P4_0.bam.bai',
                    'md5':
                        'c9396c2596254831470a9138ae86ded7',
                    'size':
                        '7163216'
                }],
                'attributes': {
                    'assembly': 'mm10',
                    'dangling_references': 'treat_as_unmapped',
                    'ENA-SPOT-COUNT': '137766536',
                    'ENA-BASE-COUNT': '12398988240',
                    'ENA-FIRST-PUBLIC': '2018-03-30',
                    'ENA-LAST-UPDATE': '2018-03-30'
                }    
            }, ffq.parse_run(soup))

    def test_parse_sample(self):
        with open(self.sample_path, 'r') as f:
            soup = BeautifulSoup(f.read(), 'xml')

        self.assertEqual({
            'accession': 'SRS4237519',
            'title': 'old_Dropseq_1',
            'organism': 'Mus musculus',
            'attributes': {
                'source_name': 'Whole lung',
                'tissue': 'Whole lung',
                'age': '24 months',
                'number of cells': '799',
                'ENA-SPOT-COUNT': '109256158',
                'ENA-BASE-COUNT': '21984096610',
                'ENA-FIRST-PUBLIC': '2019-01-11',
                'ENA-LAST-UPDATE': '2019-01-11'
            },
            'experiment': 'SRX5234128'
        }, ffq.parse_sample(soup))

    def test_parse_experiment_with_run(self):
        with open(self.experiment_path, 'r') as f:
            soup = BeautifulSoup(f.read(), 'xml')

        self.assertEqual({'accession': 'SRX5234128',
 'instrument': 'Illumina HiSeq 4000',
 'platform': 'ILLUMINA',
 'runs': {'SRR8426358': {'accession': 'SRR8426358',
   'attributes': {'ENA-BASE-COUNT': '21984096610',
    'ENA-FIRST-PUBLIC': '2019-01-27',
    'ENA-LAST-UPDATE': '2019-01-27',
    'ENA-SPOT-COUNT': '109256158'},
   'experiment': 'SRX5234128',
   'files': [{'md5': 'be7e88cf6f6fd90f1b1170f1cb367123',
     'size': '5507959060',
     'url': 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR842/008/SRR8426358/SRR8426358_1.fastq.gz'},
    {'md5': '2124da22644d876c4caa92ffd9e2402e',
     'size': '7194107512',
     'url': 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR842/008/SRR8426358/SRR8426358_2.fastq.gz'}],
   'sample': 'SRS4237519',
   'study': 'SRP178136',
   'title': 'Illumina HiSeq 4000 paired end sequencing; GSM3557675: old_Dropseq_1; Mus musculus; RNA-Seq'}},
 'title': 'Illumina HiSeq 4000 paired end sequencing; GSM3557675: old_Dropseq_1; Mus musculus; RNA-Seq'}, ffq.parse_experiment_with_run(soup))

    def test_parse_study(self):
        with open(self.study_path, 'r') as f:
            soup = BeautifulSoup(f.read(), 'xml')

        self.assertEqual({'accession': 'SRP178136',
                          'title': 'Multi-modal analysis of the aging mouse lung at cellular resolution',
                          'abstract': 'A) Whole lung tissue from 24 months (n=7) '
                          'and 3 months old (n=8) mice was dissociated and single-cell '
                          'mRNAseq libraries generated with Drop-Seq. B) Bulk RNA-seq '
                          'data was generated from whole mouse lung tissue of old (n=3) '
                          'and young (n=3) samples. C) Bulk RNA-seq data was generated '
                          'from flow-sorted macrophages from old (n=7) and young (n=5) '
                          'mice and flow-sorted epithelial cells from old (n=4) and '
                          'young (n=4) mice. Overall design: Integration of bulk RNA-seq '
                          'from whole mouse lung tissue and bulk RNA-seq from flow-sorted '
                          'lung macrophages and epithelial cells was used to validate results '
                          'obtained from single cell RNA-seq of whole lung tissue.',
                          'accession': 'SRP178136'
                          }, ffq.parse_study(soup))

    def test_parse_study_with_run(self):
        with open(self.study_with_run_path, 'r') as f:
            soup = BeautifulSoup(f.read(), 'xml')
            self.assertEqual({
                'accession':
                    'SRP096361',
                'title':
                    'A Molecular Census of Arcuate Hypothalamus and Median Eminence Cell Types',
                'abstract': (
                    'Drop-seq and single cell sequencing of mouse arcuate nucleus and '
                    'median eminence. Please see below link for searchable cluster-based '
                    'gene expression. Overall design: Drop-Seq was performed on six separate '
                    'days using mice in C57BL6/J background at various ages/sex noted. '
                    'On day 1, Chow_1 replicate was obtained. On day 2, Chow_2 replicate '
                    'was  obtained. On day 3, Chow_3 replicate was obtained.  On day 4, 10% '
                    'Diet_1 and HFD_1 replicates were obtained. On day 5, Fast_1 and Refed_1 '
                    'replicates were obtained. On day 6,  Fast_2, Fast_3, Chow_4, and Chow_5 '
                    'replicates were obtained'
                ),
                'runlist': [
                    'SRR5164436', 'SRR5164437', 'SRR5164438', 'SRR5164439',
                    'SRR5164440', 'SRR5164441', 'SRR5164442', 'SRR5164443',
                    'SRR5164444', 'SRR5164445', 'SRR5164446'
                ]
            }, ffq.parse_study_with_run(soup))

    def test_gse_search_json(self):
        with open(self.gse_search_path, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            self.assertEqual({
                'accession': 'GSE93374',
                'geo_id': '200093374'
            }, ffq.parse_gse_search(soup))

    def test_gse_summary_json(self):
        with open(self.gse_summary_path, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            self.assertEqual({'accession': 'SRP096361'},
                             ffq.parse_gse_summary(soup))

    def test_ffq_gse(self):
        # Need to figure out how to add for loop test for adding individual runs
        with mock.patch('ffq.ffq.get_gse_search_json') as get_gse_search_json, \
            mock.patch('ffq.ffq.parse_gse_search') as parse_gse_search, \
            mock.patch('ffq.ffq.gse_to_gsms') as gse_to_gsms, \
            mock.patch('ffq.ffq.ffq_gsm') as ffq_gsm, \
            mock.patch('ffq.ffq.geo_to_suppl') as geo_to_suppl:

            parse_gse_search.return_value = {
                'accession': 'GSE1',
                'geo_id': 'GEOID1'
            }

            gse_to_gsms.return_value = ['GSM_1', 'GSM_2']
            geo_to_suppl.return_value = {'filename': 'file', 'size': 'size', 'url': 'url'}
            ffq_gsm.side_effect = [{'accession': 'GSM1'}, {'accession': 'GSM2'}, 'test', 'test']

            self.assertEqual({
                'accession': 'GSE1',
                'supplementary_files': {
                    'filename': 'file',
                    'size': 'size',
                    'url': 'url'
                },    
                'samples': {
                    'GSM1': {
                        'accession': 'GSM1'
                    }, 
                    'GSM2': {
                        'accession' : 'GSM2'
                        }
                    }
                 }, ffq.ffq_gse('GSE1'))

            get_gse_search_json.assert_called_once_with('GSE1')
            gse_to_gsms.assert_called_once_with('GSE1')
            ffq_gsm.assert_has_calls([call('GSM_1'), call('GSM_2')])


    def test_ffq_gsm(self):
        # Need to figure out how to add for loop test for adding individual runs     
        with mock.patch('ffq.ffq.get_gsm_search_json') as get_gsm_search_json, \
            mock.patch('ffq.ffq.geo_to_suppl') as geo_to_suppl, \
            mock.patch('ffq.ffq.gsm_to_platform') as gsm_to_platform, \
            mock.patch('ffq.ffq.gsm_id_to_srs') as gsm_id_to_srs, \
            mock.patch('ffq.ffq.ffq_sample') as ffq_sample:

            get_gsm_search_json.return_value = {
                'accession': 'GSM1',
                'geo_id': 'GSMID1'
            }
            geo_to_suppl.return_value = {'supplementary_files' : 'supp'}
            gsm_to_platform.return_value = {'platform' : 'platform'}
            gsm_id_to_srs.return_value = 'SRS1'
            ffq_sample.return_value = {'accession': 'SRS1'}

            self.assertEqual({
                'accession': 'GSM1',
                'supplementary_files' : {'supplementary_files' : 'supp'},
                'platform' : 'platform',
                'sample': {
                    'SRS1': {
                        'accession': 'SRS1'
                    }
                }
            }, ffq.ffq_gsm('GSM1'))
            get_gsm_search_json.assert_called_once_with('GSM1')
            geo_to_suppl.assert_called_once_with('GSM1', 'GSM')
            gsm_to_platform.assert_called_once_with('GSM1')
            gsm_id_to_srs.assert_called_once_with('GSMID1')
            ffq_sample.assert_called_once_with('SRS1')

    def test_ffq_run(self):
        with mock.patch('ffq.ffq.get_xml') as get_xml,\
            mock.patch('ffq.ffq.parse_run') as parse_run:
            run = mock.MagicMock()
            parse_run.return_value = run
            self.assertEqual(run, ffq.ffq_run('SRR8426358'))
            get_xml.assert_called_once_with('SRR8426358')

    def test_ffq_study(self):
        with mock.patch('ffq.ffq.get_xml') as get_xml,\
            mock.patch('ffq.ffq.parse_study') as parse_study,\
            mock.patch('ffq.ffq.ffq_sample') as ffq_sample,\
            mock.patch('ffq.ffq.get_samples_from_study') as get_samples_from_study:
            parse_study.return_value = {'study': 'study_id'}
            get_samples_from_study.return_value = ["sample_id1", "sample_id2"]    
            ffq_sample.side_effect = [{'accession': 'id1'}, {'accession': 'id2'}]
            self.assertEqual({'study': 'study_id',
                'samples': {'id1': {'accession': 'id1'},
                 'id2': {'accession': 'id2'}
                     },
            }, ffq.ffq_study('SRP226764'))
            get_xml.assert_called_once_with('SRP226764')
            self.assertEqual(2, ffq_sample.call_count)
            ffq_sample.assert_has_calls([call('sample_id1'), call('sample_id2')])

    def test_ffq_experiment(self):
        with mock.patch('ffq.ffq.get_xml') as get_xml,\
            mock.patch('ffq.ffq.parse_experiment_with_run') as parse_experiment_with_run:
            parse_experiment_with_run.return_value = {'experiment': 'experiment', 'runs' : {'run': 'run'}}

            self.assertEqual({'experiment': 'experiment', 'runs' : {'run': 'run'
            }}, ffq.ffq_experiment('SRX7048194'))
            get_xml.assert_called_once_with('SRX7048194')



## To use for ffq_sample
#    def test_ffq_experiment(self):
#        with mock.patch('ffq.ffq.get_xml') as get_xml,\
#            mock.patch('ffq.ffq.parse_experiment') as parse_experiment,\
#            mock.patch('ffq.ffq.ffq_sample') as ffq_sample:
#            parse_experiment.return_value = {'experiment': 'experiment', 'sample': 'sample'}
 #           ffq_sample.return_value = {'accession': 'sample'}
#
 #           self.assertEqual({'experiment': 'experiment', 'sample': 'sample',
  #              'samples': {'sample': {'accession':'sample'
   #         }}}, ffq.ffq_experiment('SRX7048194'))
     #       get_xml.assert_called_once_with('SRX7048194')
    #        ffq_sample.assert_called_once_with('sample')
## To use for ffq_sample



    def test_ffq_doi(self):
        with mock.patch('ffq.ffq.get_doi') as get_doi,\
            mock.patch('ffq.ffq.search_ena_title') as search_ena_title,\
            mock.patch('ffq.ffq.ffq_study') as ffq_study:

            get_doi.return_value = {'title': ['title']}
            search_ena_title.return_value = ['SRP1']
            self.assertEqual([ffq_study.return_value], ffq.ffq_doi('doi'))
            get_doi.assert_called_once_with('doi')
            search_ena_title.assert_called_once_with('title')
            ffq_study.assert_called_once_with('SRP1')

    def test_ffq_doi_no_title(self):
        with mock.patch('ffq.ffq.get_doi') as get_doi,\
            mock.patch('ffq.ffq.search_ena_title') as search_ena_title,\
            mock.patch('ffq.ffq.ncbi_search') as ncbi_search,\
            mock.patch('ffq.ffq.ncbi_link') as ncbi_link,\
            mock.patch('ffq.ffq.geo_ids_to_gses') as geo_ids_to_gses,\
            mock.patch('ffq.ffq.ffq_gse') as ffq_gse:

            get_doi.return_value = {'title': ['title']}
            search_ena_title.return_value = []
            ncbi_search.return_value = ['PMID1']
            ncbi_link.return_value = ['GEOID1']
            geo_ids_to_gses.return_value = ['GSE1']
            self.assertEqual([ffq_gse.return_value], ffq.ffq_doi('doi'))
            get_doi.assert_called_once_with('doi')
            search_ena_title.assert_called_once_with('title')
            ncbi_search.assert_called_once_with('pubmed', 'doi')
            ncbi_link.assert_called_once_with('pubmed', 'gds', 'PMID1')
            geo_ids_to_gses.assert_called_once_with(['GEOID1'])
            ffq_gse.assert_called_once_with('GSE1')

    def test_ffq_doi_no_geo(self):
        with mock.patch('ffq.ffq.get_doi') as get_doi,\
            mock.patch('ffq.ffq.search_ena_title') as search_ena_title,\
            mock.patch('ffq.ffq.ncbi_search') as ncbi_search,\
            mock.patch('ffq.ffq.ncbi_link') as ncbi_link,\
            mock.patch('ffq.ffq.sra_ids_to_srrs') as sra_ids_to_srrs,\
            mock.patch('ffq.ffq.ffq_run') as ffq_run:

            get_doi.return_value = {'title': ['title']}
            search_ena_title.return_value = []
            ncbi_search.return_value = ['PMID1']
            ncbi_link.side_effect = [[], ['SRA1']]
            sra_ids_to_srrs.return_value = ['SRR1']
            ffq_run.return_value = {
                'accession': 'SRR1',
                'study': {
                    'accession': 'SRP1'
                }
            }
            self.assertEqual([{
                'accession': 'SRP1',
                'runs': {
                    'SRR1': {
                        'accession': 'SRR1',
                        'study': {
                            'accession': 'SRP1'
                        }
                    }
                }
            }], ffq.ffq_doi('doi'))
            get_doi.assert_called_once_with('doi')
            search_ena_title.assert_called_once_with('title')
            ncbi_search.assert_called_once_with('pubmed', 'doi')
            self.assertEqual(2, ncbi_link.call_count)
            ncbi_link.assert_has_calls([
                call('pubmed', 'gds', 'PMID1'),
                call('pubmed', 'sra', 'PMID1'),
            ])
            sra_ids_to_srrs.assert_called_once_with(['SRA1'])
            ffq_run.assert_called_once_with('SRR1')
