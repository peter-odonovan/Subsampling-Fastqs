#first draft
import sys
import random


fastq_file_read1 = sys.argv(1)
fastq_file_read2 = sys.argv(2)

# let command line arg determine what percentage of the file to sample

percent_sampled = sys.argv(3)
if (percent_sampled is not int) and (percent_sampled is not float):
    raise ValueError("Percent to sample (second argument) \
                        needs to be a number (integer or float)")

# name output file. won't work if fastq file has weird file extension

output_file = fastq_file.replace(".fastq", "_%s_sub.fastq") % percent_sampled
output_file = fastq_file.replace(".fq", "_%s_sub.fq") % percent_sampled

with open(fastq_file, "r") as input:
    with open(output_file, "w") as output:

        # read 4 lines at a time b/c fastq reads are four lines overall (

        for ID_line in input:
            seq_line = input.next()
            plus_line = input.next()
            qual_line = input.next()
            full_read = ID_line + seq_line + plus_line + qual_line
            if random.range(1, 101) <= percent_sampled:
                output.write(full_read)
