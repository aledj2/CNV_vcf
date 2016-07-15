'''
Created on 15 Jul 2016
This script reads an aberration report and performs a blat search to get the ref base and creates a VCF file 
@author: aled
'''
import subprocess

class create_vcf():
    def __init__(self):
        self.base_template = "/home/aled/Documents/CNV_vcf/cnv_template.vcf"
        self.aber_report = "/home/aled/Documents/CNV_vcf/aber_report.txt"
        self.output_vcf = "/home/aled/Documents/CNV_vcf/output/output_vcf.vcf"
        
    
    def read_aber_report(self):  
        #open the output file 
        output_file=open(self.output_vcf,'a')
        
        #open base template and copy it to output file
        vcf_header=open(self.base_template,'r')
        for i in vcf_header:
            output_file.write(i)
        
        #close files
        vcf_header.close()
        output_file.close()
        
        #send each line of aber report to get_first_base
        aber_report=open(self.aber_report,'r')
        
        #loop through the aber_report and pass line to get_first_base module
        for line in aber_report:
            create_vcf().get_first_base(line)
        aber_report.close()
        
        
    def get_first_base(self,line):
        #split line to get relevant cols
        linesplit=line.split('\t')
        chr=linesplit[1]
        start=linesplit[3]
        
        #create coordinate for first base of CNV
        pos=chr+":"+str(start)+"-"+str(start)
        
        # run the samtools command via command line
        proc = subprocess.Popen(["samtools faidx /home/aled/Documents/Reference_Genomes/hg19.fa " + pos], stdout=subprocess.PIPE, shell=True)
        # capture stdout and stderror
        (out, err) = proc.communicate()
        
        # capture the reference base from the output
        blat_out = out
        if err is not None:
            print err
        
        #capture the Ref base from the output  
        ref_base = out[-2:-1]
        
        #pass line and ref base to module to write vcf
        create_vcf().write_to_output_file(ref_base,line)
        
    def write_to_output_file(self,ref_base,line):
        #split line
        linesplit=line.split('\t')
        chr=linesplit[1]
        start=linesplit[3]
        end=linesplit[4]
        num_probes=linesplit[5]
        #calculate length of CNV
        length=int(end)-int(start)
        
        #open output file
        output_file=open(self.output_vcf,'a')
        
        #an example vcf line:
        #CHROM    POS    ID    REF    ALT    QUAL    FILTER    INFO    FORMAT    SAMPLE
        #chr1    1583259    .    REF    <CNV>    100.0    .    PRECISE=FALSE;SVTYPE=CNV;END=1655696;LEN=72437;NUMTILES=70;CONFIDENCE=10;PRECISION=10    GT:GQ:CN    ./.:0:3
        
        #write line
        output_file.write("\n"+chr+"\t"+start+"\t.\t"+ref_base+"\t<CNV>\t100.0\t.\tPRECISE=FALSE;SVTYPE=CNV;END="+str(end)+":LEN="+str(length)+":NUMTILES="+str(num_probes)+":CONFIDENCE=0;PRECISION=45\tGT:GQ:CN\t./.:0:1")
        # close file
        output_file.close()


if __name__=="__main__":
    a=create_vcf()
    a.read_aber_report()