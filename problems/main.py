import os
import json

def rename_pdfs_from_metadata(metadata_path):
    with open(metadata_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        original_pdf = item.get("pdf")
        if not original_pdf or not os.path.exists(original_pdf):
            print(f"Skipping missing file: {original_pdf}")
            continue

        base, ext = os.path.splitext(original_pdf)
        new_problem = f"{base}_problem{ext}"
        new_solution = f"{base}_solution{ext}"

        # Rename original PDF to _problem
        try:
            os.rename(original_pdf, new_problem)
            print(f"Renamed: {original_pdf} → {new_problem}")
        except Exception as e:
            print(f"Error renaming to problem: {e}")

        # Copy or create _solution version
        try:
            if os.path.exists(new_solution):
                print(f"Solution already exists: {new_solution}")
            else:
                # Duplicate the problem file as a placeholder for the solution
                with open(new_problem, 'rb') as src, open(new_solution, 'wb') as dst:
                    dst.write(src.read())
                print(f"Created dummy solution file: {new_solution}")
        except Exception as e:
            print(f"Error creating solution: {e}")

# Example usage:
rename_pdfs_from_metadata("pdf_metadata.json")
