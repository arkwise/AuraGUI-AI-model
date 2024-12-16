import json
import os

# taking the steb output and testing it to make sure it is correctly readable to build stepc

def summarize_dataset(dataset_file):
    # Load the dataset
    with open(dataset_file, 'r') as f:
        dataset = json.load(f)
    
    # Access code_elements and other relevant sections
    code_elements = dataset.get("code_elements", {})
    file_mapping = dataset.get("file_mapping", {})
    header_files = dataset.get("header_files", "")

    # Check if the structure is valid
    if not code_elements:
        print("No valid code elements found.")
        return

    # Extract functions, variables, and other elements
    functions = code_elements.get("functions", [])
    variables = code_elements.get("variables", [])
    constants = code_elements.get("constants", [])
    function_calls = code_elements.get("function_calls", [])
    pointers = code_elements.get("pointers", [])
    memory_allocations = code_elements.get("memory_allocations", [])
    conditional_compilation = code_elements.get("conditional_compilation", [])
    header_guards = code_elements.get("header_guards", [])
    includes = code_elements.get("includes", [])
    typedefs = code_elements.get("typedefs", [])
    enums = code_elements.get("enums", [])

    # Print summary
    print(f"Total functions: {len(functions)}")
    print(f"Total variables: {len(variables)}")
    print(f"Total constants: {len(constants)}")
    print(f"Total function calls: {len(function_calls)}")
    print(f"Total pointers: {len(pointers)}")
    print(f"Total memory allocations: {len(memory_allocations)}")
    print(f"Total conditional compilation blocks: {len(conditional_compilation)}")
    print(f"Total header guards: {len(header_guards)}")
    print(f"Total includes: {len(includes)}")
    print(f"Total typedefs: {len(typedefs)}")
    print(f"Total enums: {len(enums)}")
    print(f"File mappings: {len(file_mapping)}")
    print(f"Header files directory: {header_files}")

    # Sample of function names (first 5)
    print("\nSample Function Names (First 5):")
    for i, function in enumerate(functions[:5], start=1):
        print(f"{i}. {function}")

    # Sample variables (first 5)
    print("\nSample Variables (First 5):")
    for i, variable in enumerate(variables[:5], start=1):
        print(f"{i}. {variable}")

    # Sample enums (first 5)
    print("\nSample Enums (First 5):")
    for i, enum in enumerate(enums[:5], start=1):
        print(f"{i}. {enum}")

    # Sample file mappings (first 5)
    print("\nSample File Mappings (First 5):")
    for i, (function, file) in enumerate(list(file_mapping.items())[:5], start=1):
        print(f"{i}. {function} -> {file}")

# Example usage
dataset_file = 'dataset.json'  # Path to your dataset file
summarize_dataset(dataset_file)