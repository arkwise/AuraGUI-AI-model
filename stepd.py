from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset

# Load the base model
model_name = "codellama/CodeLlama-7b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# Prepare model for LoRA fine-tuning
model = prepare_model_for_kbit_training(model)
lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"], lora_dropout=0.1, bias="none")
model = get_peft_model(model, lora_config)

# Load your dataset
dataset = load_dataset("json", data_files="prepared_dataset.json")["train"]

# Tokenize dataset
def tokenize_function(example):
    return tokenizer(example["prompt"], padding="max_length", truncation=True)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Fine-tune the model
model.train()
for epoch in range(3):  # Adjust epochs as needed
    for batch in tokenized_dataset:
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

# Save the fine-tuned model
model.save_pretrained("./lora_fine_tuned_model")
tokenizer.save_pretrained("./lora_fine_tuned_model")