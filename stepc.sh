#!/bin/bash

#this script is for finding the models and information for them on mac M1

# Set directories
MODEL_BLOBS_DIR="$HOME/.ollama/models/blobs"
MODEL_MANIFESTS_DIR="$HOME/.ollama/models/manifests"

# Output report file
REPORT_FILE="ollama_model_analysis_report.txt"

# Create or clear the report file
echo "Ollama Model Analysis Report" > "$REPORT_FILE"
echo "Generated on: $(date)" >> "$REPORT_FILE"
echo "=========================================" >> "$REPORT_FILE"

# Function to analyze a single blob file
analyze_blob() {
    local blob_path=$1
    echo "Analyzing blob: $(basename "$blob_path")" >> "$REPORT_FILE"
    echo "Size: $(du -h "$blob_path" | cut -f1)" >> "$REPORT_FILE"
    echo "File type: $(file "$blob_path" | cut -d':' -f2 | xargs)" >> "$REPORT_FILE"
    echo "Extracted strings (if any):" >> "$REPORT_FILE"
    strings "$blob_path" | head -n 10 >> "$REPORT_FILE" 2>/dev/null
    echo "-----------------------------------------" >> "$REPORT_FILE"
}

# Analyze all blobs in the blobs directory
echo "Scanning blobs in: $MODEL_BLOBS_DIR" >> "$REPORT_FILE"
for blob in "$MODEL_BLOBS_DIR"/*; do
    if [ -f "$blob" ]; then
        analyze_blob "$blob"
    else
        echo "Skipping non-file item: $blob" >> "$REPORT_FILE"
    fi
done

# Analyze manifests for additional metadata
echo "Analyzing manifests in: $MODEL_MANIFESTS_DIR" >> "$REPORT_FILE"
echo "-----------------------------------------" >> "$REPORT_FILE"
find "$MODEL_MANIFESTS_DIR" -type f -name "*.json" -exec sh -c 'echo "Manifest: {}" >> "$REPORT_FILE"; cat {} | jq "." >> "$REPORT_FILE"; echo "-----------------------------------------" >> "$REPORT_FILE"' \;

# Final message
echo "Analysis completed. Report saved to: $REPORT_FILE"