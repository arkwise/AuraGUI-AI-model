import os
import json

# creating the first stage of the dataset for use with stepc


# Helper function to read data from files
def read_file(filepath):
    with open(filepath, "r") as file:
        return [line.strip() for line in file if line.strip()]

# Process extracted files
def process_extracted_files(extracted_dir):
    data = {}

    # Read each file
    data["functions"] = read_file(os.path.join(extracted_dir, "functions.txt"))
    data["variables"] = read_file(os.path.join(extracted_dir, "variables.txt"))
    data["constants"] = read_file(os.path.join(extracted_dir, "constants.txt"))
    data["function_calls"] = read_file(os.path.join(extracted_dir, "function_calls.txt"))
    data["pointers"] = read_file(os.path.join(extracted_dir, "pointers.txt"))
    data["memory_allocations"] = read_file(os.path.join(extracted_dir, "memory_allocations.txt"))
    data["conditional_compilation"] = read_file(os.path.join(extracted_dir, "conditional_compilation.txt"))
    data["header_guards"] = read_file(os.path.join(extracted_dir, "header_guards.txt"))
    data["includes"] = read_file(os.path.join(extracted_dir, "includes.txt"))
    data["typedefs"] = read_file(os.path.join(extracted_dir, "typedefs.txt"))
    data["enums"] = read_file(os.path.join(extracted_dir, "enums.txt"))

    return data

# Map elements to source files
def map_to_source(data, source_dir):
    mapping = {}

    # Iterate through functions and locate them in source files
    for function in data["functions"]:
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith((".c", ".cpp")):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as src:
                            if function in src.read():
                                mapping[function] = filepath
                                break
                    except Exception as e:
                        print(f"Error reading file {filepath}: {e}")
    
    return mapping

# Build final dataset
def build_dataset():
    # Ask the user for directories
    extracted_dir = input("Enter the directory containing the extracted files: ").strip()
    source_dir = input("Enter the directory containing the source code files: ").strip()
    header_dir = input("Enter the directory containing the header files: ").strip()

    # Validate directories
    if not os.path.isdir(extracted_dir):
        print("Error: Extracted files directory does not exist!")
        return

    if not os.path.isdir(source_dir):
        print("Error: Source code directory does not exist!")
        return

    if not os.path.isdir(header_dir):
        print("Error: Header files directory does not exist!")
        return

    # Process files and build the dataset
    data = process_extracted_files(extracted_dir)
    mapping = map_to_source(data, source_dir)

    # Combine extracted data with mapping
    dataset = {
        "code_elements": data,
        "file_mapping": mapping,
        "header_files": header_dir  # Include the header files directory as part of the dataset
    }

    # Save to a JSON file for further analysis
    output_file = "dataset.json"
    with open(output_file, "w") as json_file:
        json.dump(dataset, json_file, indent=4)

    print(f"Dataset built and saved as {output_file}")

# Run the script
if __name__ == "__main__":
    build_dataset()