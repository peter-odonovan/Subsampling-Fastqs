import sys
import random
import gzip


fastq_file_read1 = sys.argv[1]
fastq_file_read2 = sys.argv[2]


# let command line arg determine what percentage of the file to sample
try:
    percent_sampled = float(sys.argv[3])
except ValueError:
    raise ("Percent to sample (third argument) "
           "needs to be a number so it can be turned into a float")


# name output file. won't work if fastq file has weird file extension
def name_output_file(file, number):
    # else if statement so that it works with both zipped and unzipped files
    if file.endswith("q"):
        output_file = file.replace(".fastq", "_%s_sub.fastq" % (number))
        output_file = output_file.replace(".fq", "_%s_sub.fq" % (number))

    else:
        output_file = file.replace(".fastq.gz", "_%s_sub.fastq.gz" % (number))
        output_file = output_file.replace(".fq.gz", "_%s_sub.fq.gz" % (number))

    return output_file


output_file1 = name_output_file(fastq_file_read1, percent_sampled)
output_file2 = name_output_file(fastq_file_read2, percent_sampled)


def read_random_lines(files_list, reader_function):
    counter = 0
    Read_1 = reader_function(files_list[0], "r")
    Read_2 = reader_function(files_list[1], "r")
    First_output = reader_function(files_list[2], "w")
    Second_output = reader_function(files_list[3], "w")

    # List to hold already announced percents
    # So that the progress report doesn't keep printing the same percentage
    Announced_percentages = list()
    # trial code to have a percent finished var
    with Read_1 as input:

        # increment by 0.25 each line b/c reads are four lines long overall
        num_reads = sum([0.25 for line in input])
# re-open read 1
    Read_1 = reader_function(files_list[0], "r")

    with Read_1 as main_input, \
         Read_2 as read2_input, \
         First_output as output1, \
         Second_output as output2:

            # read 4 lines at a time b/c fastq reads are four lines overall
            # (ID line,seq line, "+" line, qual line)
            # Iterates over Fq read1 file to get all the reads
            # get reads from the Read 1 fastq file
            for ID_line1 in main_input:
                seq_line1 = main_input.readline()
                plus_line1 = main_input.readline()
                qual_line1 = main_input.readline()

                full_read1 = ID_line1 + seq_line1 + \
                        plus_line1 + qual_line1

                # get reads from Read 2 file
                ID_line2 = read2_input.readline()
                seq_line2 = read2_input.readline()
                plus_line2 = read2_input.readline()
                qual_line2 = read2_input.readline()

                full_read2 = ID_line2 + seq_line2 + \
                           plus_line2 + qual_line2

                counter += 1

                # use the randrange function to set
                # a random number btw 1 and 100
                # if this number is below the percent we want,
                # write reads to output file.
                # This leads to roughly the percent of reads we want
                # being written to the output file
                # NOTE: This is inexact but for large file (like fq files!)
                # it should average out to very close to the
                # percentage of reads we want
                if random.randrange(1, 101) <= percent_sampled:
                    output1.write(full_read1)
                    output2.write(full_read2)

                percent_done = round((counter/num_reads)*100)


                if (percent_done % 5 == 0) and \
                        str(percent_done) not in Announced_percentages:
                    print("%s percent of reads have been sampled" % percent_done)
                    # If the below bit is not there it repeatedly prints the
                    # same percent
                    Announced_percentages.append(str(percent_done))


# make list of file names so it will work with the function
file_names = [fastq_file_read1, fastq_file_read2, output_file1, output_file2]

# if statement so it uses the gzip function if it's a zip file,
# regular open function otherwise
if fastq_file_read1.endswith("gz"):
    read_random_lines(file_names, reader_function=gzip.open)
else:
    read_random_lines(file_names, reader_function=open)
