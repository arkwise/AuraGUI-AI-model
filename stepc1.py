from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import Trainer, TrainingArguments
import torch
import os
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.4"  # Set the memory limit to 40% of total RAM

# Set your Hugging Face token as an environment variable
os.environ["HUGGINGFACE_HUB_TOKEN"] = "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"

# Load the base model and tokenizer from Hugging Face's model hub
model_name = "codellama/CodeLlama-7b-hf"  # Replace with your desired model or use local path if needed
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float32  # Force the model to use float32 to avoid issues with meta tensor
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Define LoRA configuration
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # Target specific layers
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA to the model
model = get_peft_model(model, lora_config)

# Load and preprocess dataset from local JSON
dataset = load_dataset("json", data_files="/Users/chelsonaitcheson/auram6/prepared_dataset.json")

def preprocess_function(examples):
    return tokenizer(
        examples["prompt"],
        text_target=examples["completion"],
        truncation=True
    )

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Split the dataset into training and validation sets (e.g., 80% train, 20% validation)
train_size = 0.8
train_test_split = tokenized_dataset["train"].train_test_split(test_size=1-train_size)

train_dataset = train_test_split["train"]
validation_dataset = train_test_split["test"]

# Training arguments for Hugging Face Trainer
training_args = TrainingArguments(
    output_dir="/Users/chelsonaitcheson/.ollama/models/manifests/registry.ollama.ai/library/Auracore",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    num_train_epochs=3,
    logging_dir="/Users/chelsonaitcheson/auram6",  # Logs in the same directory as the dataset
    save_strategy="steps",
    save_steps=500,
    learning_rate=2e-4,
    logging_steps=100,
    evaluation_strategy="steps",  # Evaluation at steps, as we're passing eval_dataset
    eval_steps=500,
    save_total_limit=2,
    warmup_steps=100,
    weight_decay=0.1,
    fp16=False  # Disable fp16 mixed precision
)

# Dummy forward pass to initialize the model's parameters
input_ids = torch.ones((1, 1), dtype=torch.long)  # Dummy input (adjust as needed)
model(input_ids)

# Move model to MPS (Metal Performance Shaders)
if torch.backends.mps.is_available():
    model = model.to("mps")
else:
    model = model.to("cpu")  # Use CPU as fallback

# Trainer for fine-tuning
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=validation_dataset,  # Use validation dataset here
    tokenizer=tokenizer
)

# Train the model
trainer.train()

# Save the LoRA-adapted model to Hugging Face Model Hub (if needed)
model.push_to_hub("Auracore")

# Save the LoRA-adapted model locally
model.save_pretrained("/Users/chelsonaitcheson/.ollama/models/manifests/registry.ollama.ai/library/Auracore")