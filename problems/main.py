import os
import json
import shutil

# Define paths
pdf_dir = "pdfs"
metadata_file = "pdf_metadata.json"

# Load the metadata JSON
with open(metadata_file, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

pdf_dir = "pdfs"
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]


for i in metadata:
    # print(i)
    s1 = f"{i["year"]}_{i["stage"]}_{i["grade"]}_{i["number"]}_problem.pdf"
    s2 = f"{i["year"]}_{i["stage"]}_{i["grade"]}_{i["number"]}_solution.pdf"

    if s1 in pdf_files:
        pdf_files.remove(s1)

    if s2 in pdf_files:
        pdf_files.remove(s2)
        
    # if s1 not in pdf_files and s2 not in pdf_files:
    #     print(s1, s2)
    #     pass

output_dir = "filtered_pdfs"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(output_dir):
    file_path = os.path.join(output_dir, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        
# Copy remaining files
for i in pdf_files:
    src = os.path.join(pdf_dir, i)
    dst = os.path.join(output_dir, i)
    shutil.copy2(src, dst)
    print(f"Copied: {i}")