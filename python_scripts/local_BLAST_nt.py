# tools for local blast with nt
from Bio import SeqIO
import os
import subprocess
import time
from datetime import datetime


# define a function that can convert seconds to hours for later use during time reporting
def seconds_to_hms(seconds):
    """Convert seconds to a HH:MM:SS string."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"



# Parameters
# Define the input FASTA file, database, and output XML file, as well as the batch size for our BLAST search
query_file = "/home/moularta/BLAST/input_MultiFasta/clean_sequences_16_24_MultiFasta.fasta"  # the multi-FASTA file with headers
blast_db = "nt"                   # the BLAST database prefix (make sure BLASTDB is set, in this case nt)
evalue_threshold = 0.001          # e-value threshold (probability that a match is found by chance based on database size)
batch_size = 100  # number of sequences per batch (adjust as needed)


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

    # Start time for this batch
    # this is done as a timestamp that is not useful for a human
    batch_start_time = time.time()
    # Convert to a datetime object
    start_dt = datetime.fromtimestamp(batch_start_time)
    # Format it to make it understandable
    # %d = day, %m = month, %H Hour (0-24), %M and %S = minutes and seconds
    formatted_start_time = start_dt.strftime("%d.%m - %H:%M:%S")

    print(f"Running BLAST for batch {batch_index + 1}/{num_batches} ({start + 1}-{end} of {total_sequences}).\nCurrent time: {formatted_start_time}")


    # Call the actual blast search by saving it in cmd (=command) and executing it with the subprocess.run method
    # IMPORTANT: -parse_defline should save the sequence header in the output.xml files instead of a generic Query_1 etc.
    # this is crucial for this setup, as the batching will otherwise split up the indexes into groups of 100, hence the Query_1 will go up to Query_100 and then restart from 1
    cmd = f"blastn -query {temp_batch_file} -db {blast_db} -out {output_xml} -evalue {evalue_threshold} -outfmt 5 -num_threads 12 -parse_deflines"
    subprocess.run(cmd, shell=True)

    # remove the temporary batch file (we're only interested in the xml output files)
    os.remove(temp_batch_file)

    # update user on the finished batch and how long it took before starting the next one
    batch_end = time.time()
    elapsed = batch_end - batch_start_time
    print(f"\nFinished batch {batch_index + 1}/{num_batches} in {seconds_to_hms(elapsed)}\n\n")

# if this statement executes, the loop is completed and all batches have been processed
print("All batches processed.")
