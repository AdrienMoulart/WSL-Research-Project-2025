# tools for local blast with nt
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline
import os

# Parameters
# Define the input FASTA file, database, and output XML file, as well as the batch size for our BLAST search
query_file = "/home/moularta/BLAST/input_MultiFasta/clean_sequences_16_24_MultiFasta.fasta"  # the multi-FASTA file with headers
blast_db = "nt"                   # the BLAST database prefix (make sure BLASTDB is set, in this case nt)
evalue_threshold = 0.001          # e-value threshold (probability that a match is found by chance based on database size)
batch_size = 1  # number of sequences per batch (adjust as needed)


# Read all sequences from the multi-FASTA file
sequences = list(SeqIO.parse(query_file, "fasta"))
total_sequences = len(sequences)
# find out the number of total batches (adding the batchsize -1 to make sure the last fraction is included as well)
num_batches = (total_sequences + batch_size - 1) // batch_size  # ceiling division

# report calculated parameters before starting the BLAST search
print(f"Total sequences: {total_sequences}, Batch size: {batch_size}, Number of batches: {num_batches}")

# this starting point can be manually set in the event that our BLAST protocol is interrupted and needs to be run from a certain point onward
# when blasting all sequences, set it to 0
starting_batch_index = 0

# Process sequences in batches
for batch_index in range(starting_batch_index, num_batches):
    # determine starting point based on batch size and which batch the code is currently on.
    start = batch_index * batch_size
    # end point is set using min() to use total_sequences instead of batch_index * batch_size in case the latter exceeds the former during the last batch
    end = min((batch_index + 1) * batch_size, total_sequences)
    # index the list of sequences with the calculated indexes
    batch_sequences = sequences[start:end]

    # Create a temporary file for the current batch
    temp_batch_file = f"batch_{batch_index + 1}.fasta"
    with open(temp_batch_file, "w") as out_handle:
        SeqIO.write(batch_sequences, out_handle, "fasta")

    # Define the output XML file for this batch
    output_xml = f"blast_results_batch_{batch_index + 1}.xml"

    # Construct the blastn command
    # cline = command line
    blastn_cline = NcbiblastnCommandline(query=temp_batch_file,
                                         db=blast_db,
                                         task="blastn", # specifies nucleotide BLAST
                                         evalue=evalue_threshold,
                                         outfmt=5,  # specifies XML output
                                         out=output_xml)

    print(f"Running BLAST for batch {batch_index + 1}/{num_batches} ({start + 1}-{end} of {total_sequences})")

    # Run BLAST
    # This will run the local blastn and write the results into an XML file.
    # standard output and standard error are retrieved
    stdout, stderr = blastn_cline()

    # save stdout and stderr to log files so that we can view the process while the code runs
    with open(f"/home/moularta/script_logs/local_blast/batch_{batch_index + 1}_stdout.log", "w") as out_log:
        out_log.write(stdout)
    with open(f"/home/moularta/script_logs/local_blast/batch_{batch_index + 1}_stderr.log", "w") as err_log:
        err_log.write(stderr)

    # remove the temporary batch file (we're only interested in the xml output files)
    os.remove(temp_batch_file)

    # update user on the finished batch before starting the next one
    print(f"Finished batch {batch_index + 1}/{num_batches}")

# if this statement executes, the loop is completed and all batches have been processed
print("All batches processed.")
