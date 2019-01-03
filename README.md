# Subsampling-Fastqs
Python scripts for subsampling Paired end Fastq files


Just a little thing I made for subsampling a percentage of fastq files from paired end read data. 
Needs to be called from the command line as follows:

'''
python Subsample_fastqs.py {Fastq_R1} {Fastq_R2} {Percentage of the file you want subsampled}
 
'''

The script will output 2 files, with equivalent reads subsampled from each of the two Fastq files you have input (so for example, if the 1st, 10, and 15th read are taken from the R1 file, the 1st, 10th and 15th read will also be taken from the R2 file). The names of the output files are generated automatically and indicate which input file the reads in that output file originated from, as well as what percentage of the input files was subsampled.

I have only tested that this works in Python 3. If there are issues using it with Python 2, please contact me and I will correct them if possible.
