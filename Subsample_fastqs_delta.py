import sys
import random


fastq_file_read1 = sys.argv[1]
fastq_file_read2 = sys.argv[2]

# let command line arg determine what percentage of the file to sample
try:
    percent_sampled = float(sys.argv[3])
except ValueError:
    raise ("Percent to sample (second argument) "
           "needs to be a number so it can be turned into a float")


# name output file. won't work if fastq file has weird file extension
def name_output_file(file, number):
    # else if statement so that it works with both zipped and unzipped files
    if file.endswith("q"):
        output_file = file.replace(".fastq", "_%s_sub.fastq" % str(number))
        output_file = output_file.replace(".fq", "_%s_sub.fq" % str(number))

    else:
        output_file = file.replace(".fastq.gz", "_%s_sub.fastq.gz" % str(number))
        output_file = output_file.replace(".fq.gz", "_%s_sub.fq.gz" % str(number))

    return output_file


output_file1 = name_output_file(fastq_file_read1, percent_sampled)
output_file2 = name_output_file(fastq_file_read2, percent_sampled)


with open(fastq_file_read1, "r") as main_input:
    with open(fastq_file_read2, "r") as read2_input:
        with open(output_file1, "w") as output1:
            with open(output_file2, "w") as output2:
                for ID_line1 in main_input:

                    # read 4 lines at a time b/c fastq reads
                    # are four lines overall
                    # (ID line,seq line, "+" line, qual line)

                    # get reads from the Read 1 fastq file
                    seq_line1 = main_input.readline()
                    plus_line1 = main_input.readline()
                    qual_line1 = main_input.readline()
                    full_read1 = ID_line1 + seq_line1 + plus_line1 + qual_line1

                # get reads from Read 2 file
                    ID_line2 = read2_input.readline()
                    seq_line2 = read2_input.readline()
                    plus_line2 = read2_input.readline()
                    qual_line2 = read2_input.readline()
                    full_read2 = ID_line2 + seq_line2 + plus_line2 + qual_line2

# use the randrange function to set a random number btw 1 and 100
# if this number is below the percent we want, write reads to ouput file
# This leads to roughly the percent of reads we want being written to the output file
#NOTE: This is inexact but for large file (like fq files!) it should average out to
#Very close to the percentage of reads we want
                    if random.randrange(1, 101) <= percent_sampled:
                        output1.write(full_read1)
                        output2.write(full_read2)
