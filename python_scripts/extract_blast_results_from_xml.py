from Bio.Blast import NCBIXML  # Import Biopython’s BLAST XML parser
import pandas as pd
import glob  # Import glob from the Python standard library
import os # required to find xml file names and number batches
import re # required for searching strings more efficiently


def extract_blast_info_from_xml_file(blast_xml_file):
    """
    Extracts BLAST results from a single local XML output file.

    Parameters:
      blast_xml_file (str): Path to the BLAST XML output file.

    Returns:
      List of dictionaries containing the extracted BLAST fields.
    """
    results = []  # List to hold results for each query

    # Open and parse the BLAST XML output file
    with open(blast_xml_file) as result_handle:
        # Parse and convert the result to a list (for multiple iterations)
        blast_records = list(NCBIXML.parse(result_handle))

    # Loop over each BLAST record (i.e. each query)
    for record in blast_records:
        # Retrieve query-level information and make the query_id unique by including the file name
        # This is super important because if the file name is not added to the query ID, each batch will have the same IDs
        # This is because BLASTn doesn't save the query sequence by default, so instead xml output files just number their outputs
        # But because of the batches, the numbering resets for every 100 sequences and you can't tell them apart without adding the batch file name
        """query_id = os.path.basename(blast_xml_file) + "_" + (
            record.query_id if hasattr(record, "query_id") else record.query)"""
        # IMPORTANT:
        # the difference between the string above and the line below is what lets us retrieve the header instead of the problematic Query_<number> format!
        # if the sequence header should be recorded: run the line below, not the code in the string above!
        query_id = record.query
        query_length = record.query_letters

        # If there are no hits, you may either skip or add a record with placeholders
        if not record.alignments:
            # Optionally store a row with no hit data
            results.append({
                "query_id": query_id,
                "query_length": query_length,
                "hit_accession": None,
                "hit_def": None,
                "e_value": None,
                "bit_score": None,
                "alignment_length": None,
                "identities": None,
                "percent_identity": None,
                "query_coverage": None,
                "organism": "Not Available",
                "taxonomy": "Not Available",
                "genbank_sequence_length": "Not Available",
                "submission_date": "Not Available",
                "references": "Not Available"
            })
            continue

        # Extract the top hit (first alignment) and its first HSP
        top_alignment = record.alignments[0]
        top_hsp = top_alignment.hsps[0]

        hit_accession = top_alignment.accession
        hit_def = top_alignment.hit_def
        e_value = top_hsp.expect
        bit_score = top_hsp.bits
        alignment_length = top_hsp.align_length
        identities = top_hsp.identities

        # Calculate percent identity and query coverage
        percent_identity = (identities / alignment_length * 100) if alignment_length > 0 else 0.0
        query_coverage = (alignment_length / query_length * 100) if query_length > 0 else 0.0

        # Set additional fields as "Not Available"
        organism = "Not Available"
        taxonomy = "Not Available"
        genbank_sequence_length = "Not Available"
        submission_date = "Not Available"
        references = "Not Available"

        # Append the extracted data into our results list
        results.append({
            "query_id": query_id,
            "query_length": query_length,
            "hit_accession": hit_accession,
            "hit_def": hit_def,
            "e_value": e_value,
            "bit_score": bit_score,
            "alignment_length": alignment_length,
            "identities": identities,
            "percent_identity": percent_identity,
            "query_coverage": query_coverage,
            "organism": organism,
            "taxonomy": taxonomy,
            "genbank_sequence_length": genbank_sequence_length,
            "submission_date": submission_date,
            "references": references
        })
    return results


def extract_and_save_all_results(xml_dir, output_excel_file, result_extraction_cutoff=None):
    """
    Aggregates BLAST results from all XML files in a directory and writes them to an Excel file.

    Parameters:
      xml_dir (str): Directory containing BLAST XML files.
      output_excel_file (str): The name of the Excel file to save the results.
      result_extraction_cutoff (int): An optional parameter that lets us define a cutoff point (by batch number) which, once reached, will end the extraction there.
    """
    all_results = []

    # Use glob to find all XML files in the given directory
    xml_files = glob.glob(f"{xml_dir}/*.xml")

    def batch_key(path):
        # this extracts just the file name from the full path
        name = os.path.basename(path)
        # regex (regular expression) used to look for “batch_<number>.xml”
        # re.search scans the file name for a group of digits
        # note: \ has to be used since regex understands . to mean "any character", whereas here it needs to be part of the ".xml" string
        batch_number = re.search(r'batch_(\d+)\.xml', name)
        # a numerical version of the batch number is returned, so that we can sort batches
        # the otherwise assigned float("inf") assigns a special floating-point values that represents infinity (thus always placed at the end)
        # so here, anything that doesn't match the expected pattern will be placed at the end of our files.
        return int(batch_number.group(1)) if batch_number else float('inf')

    # updates xml_files order using batch_key function
    xml_files = sorted(xml_files, key=batch_key)

    # due to an interrupted blast search I need an option to only retrieve the data up to a certain point
    # enumerate acts as a counter and numbers our xml files, corresponding to batch number
    # the cutoff point is defined during the function call and needs to be decided at the bottom (or left out for a full extraction)
    for batch_counter, xml_file in enumerate(xml_files, start=1):
        file_results = extract_blast_info_from_xml_file(xml_file)
        all_results.extend(file_results)
        print(f"Processed {xml_file}")

        # here, we check that the extraction point has not been reached yet (if a cutoff point was specified)
        if result_extraction_cutoff is not None and batch_counter >= result_extraction_cutoff:
            print(f"\nReached cutoff at batch {batch_counter}; stopping.")
            break

    # Convert the aggregated results into a DataFrame and write to Excel
    blast_results = pd.DataFrame(all_results)
    blast_results.to_excel(output_excel_file, index=False)
    print(f"\nResults successfully saved to {output_excel_file}")


# Specify the directory containing the XML files and the output Excel file name
xml_directory = "/home/moularta/BLAST/output_xml"
output_excel = "/home/moularta/BLAST/results_excel_files/blast_results.xlsx"

# Process all XML files in the directory and save the aggregated results to Excel
# IMPORTANT NOTE: Delete the optional result_extraction_cutoff parameter if you want to extract ALL .xml files in the directory
extract_and_save_all_results(xml_directory, output_excel)
