---
name: llm-inference
description: "Local and production LLM inference: llama.cpp (GGUF), vLLM (high-throughput serving), and model discovery."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llm, inference, llama.cpp, vllm, gguf, serving, quantization, local, production]
    related_skills: [huggingface-hub, evaluating-llms-harness]
---

# LLM Inference

Deploy and run large language models locally or in production. Covers local GGUF inference with llama.cpp and high-throughput serving with vLLM.

## When to Use

- Run models on CPU, Apple Silicon, CUDA, ROCm, or Intel GPUs
- Deploy production LLM APIs with OpenAI-compatible endpoints
- Choose between quantization methods for memory constraints
- Discover and download models from the Hugging Face Hub
- Optimize inference latency and throughput

## Decision Map

| Scenario | Tool | Section |
|----------|------|---------|
| Local/edge inference, CPU, single-user | llama.cpp | § Local Inference |
| Production API, high throughput, multi-user | vLLM | § Production Serving |
| Find GGUF models on Hugging Face | Hub search | § Model Discovery |

---

## Local Inference (llama.cpp)

Run GGUF-quantized models locally with minimal dependencies.

### Installation

```bash
# macOS / Linux
brew install llama.cpp

# Windows
winget install llama.cpp

# From source
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp && cmake -B build && cmake --build build --config Release
```

### Run from Hugging Face Hub

```bash
# Shorthand quant selection
llama-cli -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0

# OpenAI-compatible server
llama-server -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0
```

### Exact file from Hub

```bash
llama-server \
    --hf-repo microsoft/Phi-3-mini-4k-instruct-gguf \
    --hf-file Phi-3-mini-4k-instruct-q4.gguf \
    -c 4096
```

### Python bindings (llama-cpp-python)

```bash
pip install llama-cpp-python
# CUDA: CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
# Metal: CMAKE_ARGS="-DGGML_METAL=on" ...
```

```python
from llama_cpp import Llama

llm = Llama(
    model_path="./model-q4_k_m.gguf",
    n_ctx=4096,
    n_gpu_layers=35,  # 0 for CPU, 99 for full offload
    n_threads=8,
)

# Generation
out = llm("What is machine learning?", max_tokens=256, temperature=0.7)
print(out["choices"][0]["text"])

# Chat + streaming
llm = Llama(model_path="./model.gguf", n_ctx=4096, n_gpu_layers=35, chat_format="llama-3")
resp = llm.create_chat_completion(
    messages=[{"role": "user", "content": "What is Python?"}],
    max_tokens=256,
)
for chunk in llm("Explain:", max_tokens=256, stream=True):
    print(chunk["choices"][0]["text"], end="", flush=True)

# Embeddings
llm = Llama(model_path="./model.gguf", embedding=True, n_gpu_layers=35)
vec = llm.embed("This is a test.")
```

### Quant Selection

- General chat: start with `Q4_K_M`
- Code/technical work: prefer `Q5_K_M` or `Q6_K` if memory allows
- Tight RAM budgets: `Q3_K_M`, `IQ` variants, or `Q2` (fit over quality)
- Do not normalize repo-native labels — if the page says `UD-Q4_K_M`, report that

### Model Discovery on Hugging Face

1. Search: `https://huggingface.co/models?apps=llama.cpp&sort=trending`
2. Open repo with local-app view: `https://huggingface.co/<repo>?local-app=llama.cpp`
3. Check hardware compatibility section for recommended quant
4. Query tree API: `https://huggingface.co/api/models/<repo>/tree/main?recursive=true`
5. Extract `.gguf` files, sizes, and quant labels

---

## Production Serving (vLLM)

High-throughput LLM serving with PagedAttention and continuous batching.

### Installation

```bash
pip install vllm
```

### Basic Usage

```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3-8B-Instruct")
sampling = SamplingParams(temperature=0.7, max_tokens=256)
outputs = llm.generate(["Explain quantum computing"], sampling)
print(outputs[0].outputs[0].text)
```

### OpenAI-Compatible Server

```bash
vllm serve meta-llama/Llama-3-8B-Instruct

# Query
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello!"}]}'
```

### Production Deployment

```bash
# Single GPU (7B-13B)
vllm serve meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 --max-model-len 8192 --port 8000

# Multi-GPU (30B-70B) with tensor parallelism
vllm serve meta-llama/Llama-2-70b-hf \
  --tensor-parallel-size 4 --quantization awq --port 8000

# With caching and metrics
vllm serve meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 --enable-prefix-caching \
  --enable-metrics --metrics-port 9090 --host 0.0.0.0
```

### Quantized Serving

```bash
# AWQ (best for 70B models, minimal accuracy loss)
vllm serve TheBloke/Llama-2-70B-AWQ --quantization awq

# GPTQ (wide model support)
vllm serve TheBloke/Llama-2-7B-GPTQ --quantization gptq

# FP8 (fastest on H100)
vllm serve meta-llama/Llama-3-8B-Instruct --quantization fp8
```

### Offline Batch Inference

```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3-8B-Instruct", tensor_parallel_size=2)
sampling = SamplingParams(temperature=0.7, top_p=0.95, max_tokens=512)

# Process all prompts in one call (vLLM batches internally)
outputs = llm.generate(prompts, sampling)
results = [o.outputs[0].text for o in outputs]
```

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `--gpu-memory-utilization` | Fraction of GPU memory to use (0.9 default) |
| `--tensor-parallel-size` | Number of GPUs for tensor parallelism |
| `--max-model-len` | Maximum sequence length |
| `--quantization` | `awq`, `gptq`, `fp8` |
| `--enable-prefix-caching` | Cache repeated prompt prefixes |
| `--enable-chunked-prefill` | Reduce TTFT for long prompts |
| `--max-num-seqs` | Maximum concurrent sequences |

---

## Comparison

| Feature | llama.cpp | vLLM |
|---------|-----------|------|
| Best for | Local/edge, CPU, single-user | Production, multi-user, GPU |
| Format | GGUF | HuggingFace transformers |
| Quantization | Q2-Q8, IQ, built-in | AWQ, GPTQ, FP8 |
| Throughput | Moderate | 24x higher than standard HF |
| API | OpenAI-compatible server | OpenAI-compatible server |
| Hardware | CPU, GPU, Apple Silicon | NVIDIA (primary), AMD, Intel |
| Memory | Very efficient | Requires GPU VRAM |

---

## Pitfalls

- **llama.cpp:** Using `127.0.0.1` in Docker → debugger can't attach. Use `0.0.0.0`.
- **vLLM:** OOM during model loading → reduce `--gpu-memory-utilization` or use quantization.
- **vLLM:** Slow TTFT → enable prefix caching or chunked prefill.
- **vLLM:** Low throughput → check GPU utilization with `nvidia-smi`, should be >80%.
- **Both:** Choosing wrong quant for the use case → test quality before deploying.
