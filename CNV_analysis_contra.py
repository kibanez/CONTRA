'''
Created on 08/09/2015

@author: kibanez
'''

#!/usr/bin/python

import sys, re, shlex , os, string, urllib, time, math, random, subprocess, shutil

from multiprocessing import Process, Manager

import inspect

from itertools import izip_longest,groupby

from operator import itemgetter

import ConfigParser

import optparse

from os import path as osp

import logging

import copy

import numpy


######################################################################

class OptionParser(optparse.OptionParser):

    def check_required (self, opt):

        option = self.get_option(opt)

        atrib = getattr(self.values, option.dest)
        
        if atrib is None:
#            self.error("%s option not supplied" % option)
            return False
        else:
            return True
            

######################################################################

def read_cfg_file(cfg_filename):
    
    fi = open(cfg_filename,'r')
    
    config = ConfigParser.ConfigParser()
    config.readfp(fi)
    
    hash_cfg = {}
        
    for field in config.options('INPUT'):
        hash_cfg[field] = config.get('INPUT',field)
   
    for field in config.options('OUTPUT'):
        hash_cfg[field] = config.get('OUTPUT',field)
     
    for field in config.options('REFERENCE'):
        hash_cfg[field] = config.get('REFERENCE',field)

    for field in config.options('SOFTWARE'):
        hash_cfg[field] = config.get('SOFTWARE',field)
        
    fi.close()
    
    return hash_cfg


#######################################################################

def run(argv=None):
    
    if argv is None: argv = sys.argv    
   
    parser = OptionParser(add_help_option=True,description="The script performs CNV estimation within the regions of interest following CONTRA strategy")
    
    parser.add_option("--cfg",default=None,help="Config file with the complete information of the target regions and paths of the files needed for the calling",dest="f_cfg")

                    
    # Se leen las opciones aportadas por el usuario
    (options, args) = parser.parse_args(argv[1:])

    if len(argv) == 1:
        sys.exit(0)
    
    if not parser.check_required("--cfg"):
        raise IOError('The cfg file does not exist')
        
               
    try:
        
        if options.f_cfg <> None:
            
            cfg_file = options.f_cfg        
          
            if not os.path.exists(cfg_file):
                raise IOError('The file %s does not exist' % (cfg_file))
            
            hash_cfg = read_cfg_file(cfg_file)

	    # INPUT           
            alignment_path  = hash_cfg.get('alignment_path','')
            l_samples  = hash_cfg.get("sample_names",'').split(',')            
            analysis_bed = hash_cfg.get('analysis_bed','')

	    # OUTPUT
            folder_path = hash_cfg.get('scratch_path','')
            cnv_path = hash_cfg.get('cnv_path','')
		
	    # REFERENCE
            ref_fasta = hash_cfg.get('ref_fasta','')


	    # SOFTWARE (CoNIFER)
            contra_path = hash_cfg.get('contra_path','')
            baseline_path = hash_cfg.get('baseline_path','')

            
            if not os.path.exists(alignment_path):
                raise IOError('The alignment path does not exist. %s' % (alignment_path))
            
            if not os.path.isfile(analysis_bed):
                raise IOError('The file does not exist. %s' % (analysis_bed))

            if not os.path.isfile(contra_path):
                raise IOError('The file does not exist. %s' % (contra_path))

            if not os.path.isfile(baseline_path):
                raise IOError('The file does not exist. %s' % (baseline_path))

            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            if not os.path.exists(cnv_path):
                os.mkdir(cnv_path)
            
                
            #Configure logger
            formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            console.setLevel(logging.INFO)
            logger = logging.getLogger("preprocess")
            logger.setLevel(logging.INFO)
            logger.addHandler(console)
            
            l_bams = []
            for bam_f in l_samples:
                abs_path = os.path.join(alignment_path,bam_f)
                if not os.path.exists(abs_path):
                    raise IOError("The bam file does not exist. Check if the introduced path is correct: %s" %(abs_path))
                else:
                    l_bams.append(abs_path)
                
            logger.info("CNV estimation will be done in the following files: \n %s \n" %(l_bams))
            
    	    # 1- In each pool, for each sample, we will compute a baseline (control coverage estimates) file to compare to:
    	    l_baselines = []
            baselina_folder = os.path.join(folder_path,"baselina")
            if not os.path.exists(baselina_folder):
                os.mkdir(baselina_folder)	
    
     	    for bam_f in l_samples:
                all_bam = copy.deepcopy(l_bams)
                output_folder = bam_f
                l_baselines.append(output_folder)
                baselina_folder2 = os.path.join(baselina_folder,bam_f)
    
                aux = os.path.join(alignment_path,bam_f)
                all_bam.remove(aux)
                all_bam2 = ' '.join(all_bam)
                arg = 'python %s -t %s -f %s -o %s -n %s' %(baseline_path,analysis_bed,all_bam2,baselina_folder2,'baseline')
                print arg
                os.system(arg)	
                    
                # 2 - Compute each sample vs the corresponding baseline_folder
    	    
    	    for index,bam_f in enumerate(l_bams):
                baseline_text = os.path.join(baselina_folder + "/" + l_baselines[index],"baseline.pooled2_TRIM0.2.txt")
                print baseline_text
                output_folder = os.path.join(cnv_path,l_samples[index])
                arg = 'python %s --target %s --test %s --bed --control %s --fasta %s --outFolder %s'%(contra_path,analysis_bed,bam_f,baseline_text,ref_fasta,output_folder)	
                print arg
                os.system(arg)	
    
    
            logger.info("CONTRA CNV estimation done! ")    
            
    except:
        print >> sys.stderr , '\n%s\t%s' % (sys.exc_info()[0],sys.exc_info()[1])
        sys.exit(2)

############################################################################333

if __name__=='__main__':
    
    run()



