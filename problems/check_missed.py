import os
import shutil

def get_pdfs_in_dir(dir_name):
	pdf_files = [f for f in os.listdir(dir_name) if f.endswith(".pdf")]
	return pdf_files

def years_for_stage(pdfs_list):
	already_passed = []

	for problem in pdfs_list:
		problem = problem.replace("3_etap_", "")
		problem = problem.replace(".pdf", "")

		if "experimental" in problem or "expiremental" in problem or "shemes" in problem:
			continue
		
		problem_year = problem[0:4]

		if problem_year not in already_passed:
			already_passed.append(problem_year)

	already_passed.sort()

	return already_passed
	
def find_theory_by_year(pdfs_list, year):
	ans=[]
	for problem in pdfs_list:
		if "experimental" in problem or "expiremental" in problem or "shemes" in problem:
			continue

		if year in problem:
			ans.append(problem)
	return ans


already_parsed = get_pdfs_in_dir("pdfs")

third = get_pdfs_in_dir("third")
final = get_pdfs_in_dir("final")

possible_states = ["_1_problem.pdf", "_2_problem.pdf", "_3_problem.pdf", 
"_1_solution.pdf", "_2_solution.pdf", "_3_solution.pdf"]

list_to_copy = []


print("THIRD\n\n")

for year in years_for_stage(third):
	temp_list = []
	for grade in range(9,12,1):
		for state in possible_states:
			estimated_name = f"{year}_3rd_{grade}{state}"
			if estimated_name not in already_parsed:
				temp_list.append(estimated_name.replace(f"{year}_", ""))

	if temp_list != []:
		f=False
		for i in find_theory_by_year(third, year):
			list_to_copy.append(f"third/{i}")
			
			if not f:
				for j in range(len(temp_list)):
					temp_list[j] = year+"_"+temp_list[j]
				print(f"{i}\t{temp_list}\n")
				f = True


print("\n\nFINAL\n\n")
for year in years_for_stage(final):
	temp_list = []
	for grade in range(9,12,1):
		for state in possible_states:
			estimated_name = f"{year}_Final_{grade}{state}"
			if estimated_name not in already_parsed:
				temp_list.append(estimated_name.replace(f"{year}_", ""))

	if temp_list != []:
		f=False
		for i in find_theory_by_year(final, year):
			list_to_copy.append(f"final/{i}")
			
			if not f:
				for j in range(len(temp_list)):
					temp_list[j] = year+"_"+temp_list[j]
				print(f"{i}\t{temp_list}\n")
				f = True


output_folder = "filtered_pdfs"
output_dirs = [output_folder, f"{output_folder}/third", f"{output_folder}/final"]

for output_dir in output_dirs:
	os.makedirs(output_dir, exist_ok=True)

	for filename in os.listdir(output_dir):
	    file_path = os.path.join(output_dir, filename)
	    if os.path.isfile(file_path):
	        os.remove(file_path)
        
# Copy remaining files
for i in list_to_copy:
    src = os.path.join(i)
    if "third/" in i:
    	dst = os.path.join(output_folder, "third", i.replace("third/", ""))
    elif "final/" in i:
    	dst = os.path.join(output_folder, "final", i.replace("final/", ""))
    	
    # dst = os.path.join(output_dir, i.replace("third/", "").replace("final/", ""))
    shutil.copy2(src, dst)
    # print(f"Copied: {i}")