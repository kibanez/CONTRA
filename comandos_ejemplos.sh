# ACHTUNG!! HEMOS CAMBIADO EN contra.py ==> en analysisperBin function ==> cn_analysis.v3.R por cn_analysis.v4.R !!


# crear fichero baselina (controles), con todos los de la carrera
python /home/kibanez/Escritorio/CNV/CONTRA/CONTRA_aplicaçao_august2015/CONTRA.v2.0.6/baseline.py -t Epilepsy_s20_reheadered.bed -f align/1-NGS00925-MiSeq-Epilepsy-v4-0RochePool4-Run-DR18_S1_align.realign.recal.bam align/2-NGS00926-MiSeq-Epilepsy-v4-0RochePool4-Run-DR102_S2_align.realign.recal.bam align/3-NGS00927-MiSeq-Epilepsy-v4-0RochePool4-Run-DR418_S3_align.realign.recal.bam align/4-NGS00928-MiSeq-Epilepsy-v4-0RochePool4-Run-DR420_S4_align.realign.recal.bam align/5-NGS00929-MiSeq-Epilepsy-v4-0RochePool4-Run-DR478_S5_align.realign.recal.bam align/6-NGS00930-MiSeq-Epilepsy-v4-0RochePool4-Run-DR623_S6_align.realign.recal.bam align/7-NGS00931-MiSeq-Epilepsy-v4-0RochePool4-Run-DR692_S7_align.realign.recal.bam align/8-NGS00932-MiSeq-Epilepsy-v4-0RochePool4-Run-DR703_S8_align.realign.recal.bam align/9-NGS00933-MiSeq-Epilepsy-v4-0RochePool4-Run-DR707_S9_align.realign.recal.bam align/10-NGS00934-MiSeq-Epilepsy-v4-0RochePool4-Run-DR714_S10_align.realign.recal.bam align/11-NGS00935-MiSeq-Epilepsy-v4-0RochePool4-Run-DR752_S11_align.realign.recal.bam align/12-NGS00936-MiSeq-Epilepsy-v4-0RochePool4-Run-DR758_S12_align.realign.recal.bam align/13-NGS00937-MiSeq-Epilepsy-v4-0RochePool4-Run-DR762_S13_align.realign.recal.bam align/14-NGS00938-MiSeq-Epilepsy-v4-0RochePool4-Run-DR769_S14_align.realign.recal.bam align/16-NGS00940-MiSeq-Epilepsy-v4-0RochePool5-Run-DR784_S16_align.realign.recal.bam -o baselina -n baseline

# control = baselina
python /home/kibanez/Escritorio/CNV/CONTRA/CONTRA_aplicaçao_august2015/CONTRA.v2.0.6/contra.py --target Epilepsy_s20_reheadered.bed --test align/15-NGS00939-MiSeq-Epilepsy-v4-0RochePool4-Run-DR776_S15_align.realign.recal.bam --bed --control baselina/baseline.pooled2_TRIM0.2.txt --fasta /ingemm/ref/Ref/hg19/fasta/ucsc.hg19.fasta --outFolder asqueroso_baselina

# control = uno cualquiera
python /home/kibanez/Escritorio/CNV/CONTRA/CONTRA_aplicaçao_august2015/CONTRA.v2.0.6/contra.py --target Epilepsy_s20_reheadered.bed --test align/15-NGS00939-MiSeq-Epilepsy-v4-0RochePool4-Run-DR776_S15_align.realign.recal.bam --control align/16-NGS00940-MiSeq-Epilepsy-v4-0RochePool5-Run-DR784_S16_align.realign.recal.bam --fasta /ingemm/ref/Ref/hg19/fasta/ucsc.hg19.fasta --outFolder asqueroso2



