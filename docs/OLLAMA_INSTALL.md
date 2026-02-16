# Ollama Installation Guide (macOS, Windows, Linux)

## Overview

This guide shows how to install and run Ollama for Audify local script generation.

Recommended starter model:
- `qwen3:1.7b`

---

## Prerequisites

- At least 8 GB RAM (16 GB recommended for smoother local inference).
- ~4 GB free disk space for runtime and model files.
- Docker Desktop installed if you run Audify via Docker Compose.

---

## macOS Installation

### 1. Install Ollama

Option A (Installer):
1. Download from [https://ollama.com/download](https://ollama.com/download)
2. Open installer and complete setup.

Option B (Homebrew):

```bash
brew install ollama
```

### 2. Start Ollama service

```bash
ollama serve
```

Keep this terminal running, or run Ollama as a background app from the installer.

### 3. Pull a model

```bash
ollama pull qwen3:1.7b
```

### 4. Verify

```bash
ollama list
curl http://localhost:11434/api/tags
```

---

## Windows Installation

### 1. Install Ollama

1. Download the Windows installer from [https://ollama.com/download](https://ollama.com/download)
2. Run installer and complete setup.

### 2. Start Ollama

Ollama usually starts as a background service after installation.  
If needed, start from Start Menu: `Ollama`.

### 3. Pull a model (PowerShell)

```powershell
ollama pull qwen3:1.7b
```

### 4. Verify (PowerShell)

```powershell
ollama list
curl http://localhost:11434/api/tags
```

If `curl` aliases to `Invoke-WebRequest`, this also works:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

---

## Linux Installation

### 1. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Start service

```bash
ollama serve
```

For `systemd` environments, you can run as a service if configured by your setup:

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

### 3. Pull a model

```bash
ollama pull qwen3:1.7b
```

### 4. Verify

```bash
ollama list
curl http://localhost:11434/api/tags
```

---

## Configure Audify to Use Ollama

Update `api/llm-service/.env`:

```bash
OLLAMA_BASE_URL=http://host.docker.internal:11434/v1
OLLAMA_MODEL=qwen3:1.7b
```

Notes:
- `host.docker.internal` works for Docker Desktop on macOS/Windows.
- On Linux, you may need to expose host networking differently or set `OLLAMA_BASE_URL` to your host IP.

---

## Quick Functional Test

Run a local generation test:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3:1.7b",
  "prompt": "Write one sentence about document to podcast conversion.",
  "stream": false
}'
```

If you receive a JSON response with generated text, Ollama is ready.

---

## Troubleshooting

### Ollama command not found
- Reopen terminal after install.
- Confirm binary path is in `PATH`.

### Port 11434 not reachable
- Check service is running: `ollama serve`.
- Check firewall settings.

### Model pulls are slow
- First pull downloads full model weights.
- Verify network connectivity and disk space.

### Audify cannot connect from Docker
- Confirm `OLLAMA_BASE_URL` is correct for your OS.
- Restart stack: `docker compose down && docker compose up --build -d`.

---

## Recommended Models for Audify

- `qwen3:1.7b` for fast local testing.
- `llama3` for broader language quality.
- `mistral` as another lightweight option.

Choose based on latency, quality, and available hardware.
