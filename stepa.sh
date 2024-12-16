#!/bin/bash

#parsing all code to output files to be built with step b

# Prompt the user for directories
read -p "Enter the directory containing the header files: " HEADER_DIR
read -p "Enter the directory containing the source code: " SOURCE_DIR

# Validate the directories
if [ ! -d "$HEADER_DIR" ]; then
    echo "Error: Header directory does not exist!"
    exit 1
fi

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source code directory does not exist!"
    exit 1
fi

# Find files
HEADER_FILES=$(find "$HEADER_DIR" -type f -name "*.h")
SOURCE_FILES=$(find "$SOURCE_DIR" -type f \( -name "*.c" -o -name "*.cpp" -o -name "*.java" \))

# Output file
OUTPUT_FILE="output.txt"
> "$OUTPUT_FILE"

echo "Extracting data from source and header files..."

# Extract functions
echo "Extracting functions..."
grep -Eh '^[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*{' $SOURCE_FILES | sed 's/{//g' | sort -u > functions.txt
echo "Functions:" >> "$OUTPUT_FILE"
cat functions.txt >> "$OUTPUT_FILE"

# Extract variables
echo "Extracting variables..."
grep -Eh '^\s*(extern|static)?\s*[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*;' $HEADER_FILES | sort -u > variables.txt
echo "Variables:" >> "$OUTPUT_FILE"
cat variables.txt >> "$OUTPUT_FILE"

# Extract constants
echo "Extracting constants..."
grep -Eh '^\s*const\s+[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*=.*;' $HEADER_FILES | sort -u > constants.txt
echo "Constants:" >> "$OUTPUT_FILE"
cat constants.txt >> "$OUTPUT_FILE"

# Extract function calls
echo "Extracting function calls..."
grep -Eh '\b[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*;' $SOURCE_FILES | sort -u > function_calls.txt
echo "Function Calls:" >> "$OUTPUT_FILE"
cat function_calls.txt >> "$OUTPUT_FILE"

# Extract pointers
echo "Extracting pointer declarations..."
grep -Eh '^\s*(extern|static)?\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\*+\s*[a-zA-Z_][a-zA-Z0-9_]*' $HEADER_FILES | sort -u > pointers.txt
echo "Pointers:" >> "$OUTPUT_FILE"
cat pointers.txt >> "$OUTPUT_FILE"

# Extract memory allocations
echo "Extracting memory allocations..."
grep -Eh '\b(malloc|calloc|realloc|free)\s*\([^)]*\)' $SOURCE_FILES | sort -u > memory_allocations.txt
echo "Memory Allocations:" >> "$OUTPUT_FILE"
cat memory_allocations.txt >> "$OUTPUT_FILE"

# Extract conditional compilation blocks
echo "Extracting conditional compilation blocks..."
grep -Eh '#\s*(if|ifdef|ifndef|else|elif|endif).*' $HEADER_FILES | sort -u > conditional_compilation.txt
echo "Conditional Compilation Blocks:" >> "$OUTPUT_FILE"
cat conditional_compilation.txt >> "$OUTPUT_FILE"

# Extract header guards
echo "Extracting header guards..."
grep -Eh '#\s*ifndef\s+[a-zA-Z_][a-zA-Z0-9_]*' $HEADER_FILES | sort -u > header_guards.txt
echo "Header Guards:" >> "$OUTPUT_FILE"
cat header_guards.txt >> "$OUTPUT_FILE"

# Extract includes
echo "Extracting includes..."
grep -Eh '#\s*include\s+[<"].*[">]' $SOURCE_FILES | sort -u > includes.txt
echo "Includes:" >> "$OUTPUT_FILE"
cat includes.txt >> "$OUTPUT_FILE"

# Extract typedefs
echo "Extracting typedefs..."
grep -Eh 'typedef\s+.*;' $HEADER_FILES | sort -u > typedefs.txt
echo "Typedefs:" >> "$OUTPUT_FILE"
cat typedefs.txt >> "$OUTPUT_FILE"

# Extract enums
echo "Extracting enums..."
grep -Eh 'enum\s+[a-zA-Z_][a-zA-Z0-9_]*\s*{[^}]*}' $HEADER_FILES | sort -u > enums.txt
echo "Enums:" >> "$OUTPUT_FILE"
cat enums.txt >> "$OUTPUT_FILE"

# Finalize the dataset
echo "Extraction completed. Results saved to $OUTPUT_FILE."