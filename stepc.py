import json
import os

#preparing the dataset into prepared_dataset.json


# Function to read the source code from the given file path
def read_source_code(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IsADirectoryError:
        # Skip directories and return a warning
        return f"Error: {file_path} is a directory, not a file."
    except Exception as e:
        # Handle any other errors (e.g., file not found)
        return f"Error reading {file_path}: {str(e)}"

# Function to prompt the user for directory paths
def get_user_paths():
    header_path = input("Enter the path to the header files: ")
    source_path = input("Enter the path to the source code files: ")
    return header_path, source_path

# Function to check if directories exist
def validate_directories(header_path, source_path):
    if not os.path.isdir(header_path):
        print(f"Error: Header directory '{header_path}' does not exist.")
        return False
    if not os.path.isdir(source_path):
        print(f"Error: Source directory '{source_path}' does not exist.")
        return False
    return True

# Function to prepare input-output pairs
def prepare_pairs(dataset, header_path, source_path):
    pairs = []
    for function_signature, file_path in dataset['file_mapping'].items():  # Iterate over file_mapping
        # Check if file_path is a dictionary or a string
        print(f"Processing: {function_signature}, File Path: {file_path}")

        # Handle dictionary-based paths (you can adjust this based on your dataset structure)
        if isinstance(file_path, dict):
            print(f"File path is a dictionary, resolving keys...")
            for key, value in file_path.items():
                print(f"Key: {key}, Value: {value}")
                # If the key corresponds to file path information, update file_path
                if 'file' in key.lower():
                    file_path = value
                    break

        # If file_path is still not a string, we skip processing for this entry
        if not isinstance(file_path, str):
            print(f"Invalid file path: {file_path}")
            source_code = "// Invalid file path format"
        else:
            print(f"Final file path: {file_path}")

            # Check if the file path is already absolute (e.g., starts with 'src/')
            if "include" in file_path:
                file_path = os.path.join(header_path, file_path)
            elif any(ext in file_path for ext in [".c", ".cpp", ".java"]):
                # Avoid duplicating the 'src/' directory if it's already in the file path
                if file_path.startswith("src/"):
                    file_path = os.path.join(source_path, file_path[4:])  # Remove the 'src/' part
                else:
                    file_path = os.path.join(source_path, file_path)

            # Check if the file exists and read the source code
            if os.path.isfile(file_path):
                print(f"File exists: {file_path}")
                source_code = read_source_code(file_path)
            else:
                print(f"File not found: {file_path}")
                source_code = "// Source code not found or invalid file path"

        # Construct the prompt (input)
        prompt = f"What does the function `{function_signature}` do?"
        
        # Construct the completion (output)
        pair = {
            "prompt": prompt,
            "completion": source_code
        }
        pairs.append(pair)
    
    return pairs

# Save the prepared pairs to a new JSON file
def save_prepared_data(pairs, filename):
    with open(filename, 'w') as f:
        json.dump(pairs, f, indent=4)

# Example usage
def run():
    # Load the dataset (function signatures and file paths)
    with open('dataset.json', 'r') as f:
        dataset = json.load(f)

    # Prompt the user for file paths
    header_path, source_path = get_user_paths()

    # Check if the directories are valid
    if not validate_directories(header_path, source_path):
        print("One or both of the directories are invalid. Exiting.")
        return
    
    # Prepare the input-output pairs
    pairs = prepare_pairs(dataset, header_path, source_path)
    
    # Save the processed dataset
    save_prepared_data(pairs, 'prepared_dataset.json')
    print("Prepared dataset saved to 'prepared_dataset.json'.")

run()