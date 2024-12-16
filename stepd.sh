#!/bin/bash

# this way doesnt work on current models

# Prompt the user for the path to the prepared dataset JSON
echo "Enter the path to your prepared_dataset.json:"
read dataset_path

# Check if the dataset file exists
if [ ! -f "$dataset_path" ]; then
    echo "Error: Dataset file '$dataset_path' not found."
    exit 1
fi

# Run the fine-tuning command using Ollama
echo "Fine-tuning CodeLlama-7B with dataset from '$dataset_path'..."
ollama fine-tune codellama-7b --dataset "$dataset_path"

# Check if the fine-tuning was successful
if [ $? -eq 0 ]; then
    echo "Fine-tuning completed successfully!"
else
    echo "Error during fine-tuning."
fi

#/Users/aundreiastenson/prepared_dataset.json

#ollama create codellama-7b-custom -f /Users/aundreiastenson/prepared_dataset.json