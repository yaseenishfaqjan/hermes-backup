---
name: mlops-workflows
description: "ML operations workflows: experiment tracking, benchmarking, and model evaluation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mlops, experiment-tracking, benchmarking, evaluation, wandb, lm-eval, weights-and-biases]
    related_skills: [llm-inference, huggingface-hub]
---

# MLOps Workflows

Experiment tracking, model benchmarking, and evaluation pipelines for machine learning projects.

## When to Use

- Track ML experiments with metrics, hyperparameters, and artifacts
- Benchmark LLMs across standard academic tasks (MMLU, GSM8K, HumanEval)
- Compare model versions and training checkpoints
- Optimize hyperparameters with automated sweeps
- Manage model registries with versioning and lineage

## Decision Map

| Task | Tool | Section |
|------|------|---------|
| Track experiments, metrics, artifacts | Weights & Biases | § Experiment Tracking |
| Benchmark LLMs on standard tasks | lm-evaluation-harness | § Model Benchmarking |
| Compare training checkpoints | Both | § Training Progress |

---

## Experiment Tracking (Weights & Biases)

Track experiments, visualize training, compare runs, and manage model registries.

### Quick Start

```bash
pip install wandb
wandb login  # or export WANDB_API_KEY=...
```

```python
import wandb

run = wandb.init(
    project="my-project",
    config={"learning_rate": 0.001, "epochs": 10, "batch_size": 32}
)

for epoch in range(run.config.epochs):
    train_loss = train_epoch()
    val_loss = validate()
    wandb.log({"epoch": epoch, "train/loss": train_loss, "val/loss": val_loss})

wandb.finish()
```

### PyTorch Integration

```python
import wandb
wandb.init(project="pytorch-demo", config={"lr": 0.001, "epochs": 10})
config = wandb.config

for epoch in range(config.epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        output = model(data)
        loss = criterion(output, target)
        optimizer.zero_grad(); loss.backward(); optimizer.step()
        if batch_idx % 100 == 0:
            wandb.log({"loss": loss.item(), "epoch": epoch})

wandb.save("model.pth")
wandb.finish()
```

### Hyperparameter Sweeps

```python
sweep_config = {
    'method': 'bayes',
    'metric': {'name': 'val/accuracy', 'goal': 'maximize'},
    'parameters': {
        'learning_rate': {'distribution': 'log_uniform', 'min': 1e-5, 'max': 1e-1},
        'batch_size': {'values': [16, 32, 64, 128]},
        'optimizer': {'values': ['adam', 'sgd', 'rmsprop']},
        'dropout': {'distribution': 'uniform', 'min': 0.1, 'max': 0.5}
    }
}

sweep_id = wandb.sweep(sweep_config, project="my-project")

def train():
    run = wandb.init()
    lr = wandb.config.learning_rate
    # ... build model with sweep config, train, log metrics

wandb.agent(sweep_id, function=train, count=50)
```

### Model Registry

```python
# Log model as artifact
artifact = wandb.Artifact('final-model', type='model')
artifact.add_file('model.pth')
wandb.log_artifact(artifact, aliases=['best', 'production'])

# Link to registry
run.link_artifact(artifact, 'model-registry/production-models')
```

### Best Practices

- Use descriptive run names: `bert-base-lr0.001-bs32-epoch10`
- Log everything relevant: git commit, data splits, system metrics
- Organize with tags and groups: `tags=["baseline", "resnet"], group="resnet-experiments"`
- Use offline mode for unstable connections: `WANDB_MODE=offline`

---

## Model Benchmarking (lm-evaluation-harness)

Evaluate LLMs across 60+ academic benchmarks using standardized prompts and metrics.

### Installation

```bash
pip install lm-eval
```

### Standard Evaluation

```bash
# Core benchmarks
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge \
  --device cuda:0 --batch_size 8 --num_fewshot 5 \
  --output_path results/llama2-7b.json
```

### Available Benchmarks

| Benchmark | Measures | Time (7B, A100) |
|-----------|----------|-----------------|
| MMLU | 57-subject knowledge | ~2 hours |
| GSM8K | Grade school math | ~5 minutes |
| HumanEval | Python code generation | ~20 minutes |
| HellaSwag | Common sense reasoning | ~10 minutes |
| TruthfulQA | Truthfulness | ~10 minutes |
| ARC | Science questions | ~5 minutes |

### Fast Evaluation (vLLM Backend)

```bash
# 5-10x faster than standard HF
lm_eval --model vllm \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=2 \
  --tasks mmlu --batch_size auto
```

### Track Training Progress

```bash
#!/bin/bash
# eval_checkpoint.sh
CHECKPOINT_DIR=$1; STEP=$2
lm_eval --model hf \
  --model_args pretrained=$CHECKPOINT_DIR/checkpoint-$STEP \
  --tasks gsm8k,hellaswag \
  --num_fewshot 0 --batch_size 16 \
  --output_path results/step-$STEP.json
```

### Compare Multiple Models

```bash
# models.txt: list of model IDs
while read model; do
  model_name=$(echo $model | sed 's/\//-/g')
  lm_eval --model hf --model_args pretrained=$model,dtype=bfloat16 \
    --tasks mmlu,gsm8k,hellaswag --num_fewshot 5 \
    --batch_size auto --output_path results/$model_name.json
done < models.txt
```

### Result Analysis

```python
import json

with open("results/llama2-7b.json") as f:
    data = json.load(f)

for task, metrics in data["results"].items():
    acc = metrics.get("acc", metrics.get("exact_match", "N/A"))
    print(f"{task}: {acc}")
```

---

## Training Progress Tracking

Combine W&B and lm-eval for comprehensive training monitoring:

```python
import wandb
import os

# Initialize W&B
wandb.init(project="training", config={"model": "Llama-3-8B", "lr": 1e-4})

# Training loop
for step in range(total_steps):
    loss = train_step()
    wandb.log({"train/loss": loss, "step": step})

    # Periodic evaluation
    if step % eval_interval == 0:
        checkpoint_path = f"checkpoints/step-{step}"
        model.save_pretrained(checkpoint_path)

        # Run lm-eval
        os.system(f"lm_eval --model hf --model_args pretrained={checkpoint_path} "
                  f"--tasks gsm8k,hellaswag --num_fewshot 0 "
                  f"--output_path results/step-{step}.json")

        # Parse and log results
        with open(f"results/step-{step}.json") as f:
            eval_data = json.load(f)
        wandb.log({
            "eval/gsm8k": eval_data["results"]["gsm8k"]["exact_match"],
            "eval/hellaswag": eval_data["results"]["hellaswag"]["acc_norm"],
            "step": step
        })

wandb.finish()
```

---

## Pitfalls

- **W&B:** Generic run names (`run1`) make comparison impossible. Use descriptive names.
- **W&B:** Forgetting to `wandb.finish()` leaves runs hanging in the UI.
- **lm-eval:** Wrong fewshot count → results don't match published numbers. Use `--num_fewshot 5` for standard comparison.
- **lm-eval:** Different task variants (`mmlu` vs `mmlu_direct`) → check exact task name.
- **Both:** Not logging git commit → can't reproduce results later.
- **lm-eval:** HumanEval requires `--allow_code_execution` flag.
