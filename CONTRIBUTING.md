# Contributing to Audify

Thanks for your interest in contributing to Audify.

Audify is an open-source AI application that turns documents into editable, two-speaker podcast-style scripts and downloadable audio using a FastAPI microservices backend and a React frontend. We welcome improvements across the codebase, documentation, bug reports, UX refinements, observability, and feature enhancements.

Before you start, read the relevant section below. It helps keep contributions focused, reviewable, and aligned with the current project setup.

---

## Quick Setup Checklist

Before you dive in, make sure you have these installed:

```bash
# Check Python (3.11+ recommended)
python --version

# Check Node.js (18+ recommended)
node --version

# Check npm
npm --version

# Check Docker
docker --version
docker compose version

# Check Git
git --version
```

New to contributing?

1. Open an issue or pick an existing one to work on.
2. Sync your branch from `dev/Audify`.
3. Follow the local setup guide below.
4. Run the app locally and verify your change before opening a PR.

## Table of Contents

- [How do I...?](#how-do-i)
  - [Get help or ask a question?](#get-help-or-ask-a-question)
  - [Report a bug?](#report-a-bug)
  - [Suggest a new feature?](#suggest-a-new-feature)
  - [Set up Audify locally?](#set-up-audify-locally)
  - [Start contributing code?](#start-contributing-code)
  - [Improve the documentation?](#improve-the-documentation)
  - [Submit a pull request?](#submit-a-pull-request)
- [Code guidelines](#code-guidelines)
- [Pull request checklist](#pull-request-checklist)
- [Branching model](#branching-model)
- [Thank you](#thank-you)

---

## How do I...

### Get help or ask a question?

- Start with the main project docs in [`README.md`](./README.md), [`docs/PROJECT_ARCHITECTURE.md`](./docs/PROJECT_ARCHITECTURE.md), and the service-level READMEs under [`api/`](./api).
- Review relevant config files such as [`simple_backend.py`](./simple_backend.py), [`api/llm-service/app/config.py`](./api/llm-service/app/config.py), and [`api/tts-service/app/config.py`](./api/tts-service/app/config.py).
- If something is still unclear, open a GitHub issue with your question and the context you already checked.

### Report a bug?

1. Search existing issues first.
2. If the bug is new, open a GitHub issue.
3. Include your environment, what happened, what you expected, and exact steps to reproduce.
4. Add screenshots, logs, request payloads, or response details if relevant.

### Suggest a new feature?

1. Open a GitHub issue describing the feature.
2. Explain the problem, who it helps, and how it fits Audify.
3. If the change is large, get alignment in the issue before writing code.

### Set up Audify locally?

#### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Git
- Docker with Docker Compose v2
- One inference path for script generation:
  - Ollama or another OpenAI-compatible local inference endpoint, or
  - An OpenAI-compatible API endpoint for fallback or hosted inference
- OpenAI API key for TTS generation

#### Option 1: Local Development

##### Step 1: Clone the repository

```bash
git clone https://github.com/cld2labs/Audify.git
cd Audify
```

##### Step 2: Configure environment variables

Create the root `.env` file:

```bash
cp .env.example .env
```

If `.env.example` is not present in your branch, create `.env` manually using the values documented in [`README.md`](./README.md).

Create `api/llm-service/.env` with your inference settings. Example:

```env
SERVICE_PORT=8002
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=
INFERENCE_API_ENDPOINT=
INFERENCE_API_TOKEN=
INFERENCE_MODEL_NAME=gpt-4o-mini
VLLM_BASE_URL=http://localhost:11434/v1
VLLM_MODEL=Qwen/Qwen3-1.7B
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_TONE=conversational
DEFAULT_MAX_LENGTH=2000
TEMPERATURE=0.7
MAX_TOKENS=2048
MAX_RETRIES=3
```

Create `api/tts-service/.env` with your TTS settings. Example:

```env
SERVICE_PORT=8003
OPENAI_API_KEY=sk-...
TTS_MODEL=tts-1-hd
DEFAULT_HOST_VOICE=alloy
DEFAULT_GUEST_VOICE=nova
OUTPUT_DIR=static/audio
AUDIO_FORMAT=mp3
AUDIO_BITRATE=192k
SILENCE_DURATION_MS=500
MAX_CONCURRENT_REQUESTS=5
MAX_SCRIPT_LENGTH=100
```

##### Step 3: Install backend dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r api/pdf-service/requirements.txt
pip install -r api/llm-service/requirements.txt
pip install -r api/tts-service/requirements.txt
```

##### Step 4: Install frontend dependencies

```bash
cd ui
npm install
cd ..
```

##### Step 5: Start the backend services

Open separate terminals and start:

```bash
# Terminal 1: gateway
source .venv/bin/activate
python simple_backend.py
```

```bash
# Terminal 2: PDF service
source .venv/bin/activate
cd api/pdf-service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

```bash
# Terminal 3: LLM service
source .venv/bin/activate
cd api/llm-service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

```bash
# Terminal 4: TTS service
source .venv/bin/activate
cd api/tts-service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8003
```

##### Step 6: Start the frontend

Open another terminal:

```bash
cd ui
npm run dev
```

##### Step 7: Access the application

- Frontend: `http://localhost:5173` in local Vite development, or `http://localhost:3000` when using Docker
- Backend gateway health check: `http://localhost:8000/health`
- PDF service docs: `http://localhost:8001/docs`
- LLM service docs: `http://localhost:8002/docs`
- TTS service docs: `http://localhost:8003/docs`

#### Option 2: Docker

From the repository root:

```bash
# Create and configure the required env files first
docker compose up --build
```

This starts:

- Frontend on `http://localhost:3000`
- Backend gateway on `http://localhost:8000`
- PDF service on `http://localhost:8001`
- LLM service on `http://localhost:8002`
- TTS service on `http://localhost:8003`

#### Common Troubleshooting

- If ports `3000`, `8000`, `8001`, `8002`, or `8003` are already in use, stop the conflicting process before starting Audify.
- If script generation fails, confirm the LLM service `.env` points to a reachable model endpoint.
- If you use Ollama with Docker, make sure Ollama is running on the host and reachable from the container.
- If audio generation fails, verify `OPENAI_API_KEY` is set in `api/tts-service/.env`.
- If Docker fails to build, rebuild with `docker compose up --build`.
- If Python packages fail to install, confirm you are using a supported Python version.

### Start contributing code?

1. Open or choose an issue.
2. Create a feature branch from `dev/Audify`.
3. Keep the change focused on a single problem.
4. Run the app locally and verify the affected workflow.
5. Update docs when behavior, setup, configuration, or architecture changes.
6. Open a pull request from your feature branch into `dev/Audify`.

### Improve the documentation?

Documentation updates are welcome. Relevant files currently live in:

- [`README.md`](./README.md)
- [`docs/`](./docs/)
- [`api/pdf-service/README.md`](./api/pdf-service/README.md)
- [`api/llm-service/README.md`](./api/llm-service/README.md)
- [`api/tts-service/README.md`](./api/tts-service/README.md)
- [`benchmarks/README.md`](./benchmarks/README.md)

### Submit a pull request?

Follow the checklist below before opening your PR. Your pull request should:

- Stay focused on one issue or topic.
- Explain what changed and why.
- Include manual verification steps.
- Include screenshots or short recordings for UI changes.
- Reference the related GitHub issue when applicable.

Note: pull requests should target the `dev/Audify` branch unless maintainers ask otherwise.

---

## Code guidelines

- Follow the existing project structure and patterns before introducing new abstractions.
- Keep frontend changes consistent with the React + Vite + Tailwind setup already in use under [`ui/`](./ui/).
- Keep backend changes consistent with the FastAPI microservice structure under [`api/`](./api/) and the gateway in [`simple_backend.py`](./simple_backend.py).
- Avoid unrelated refactors in the same pull request.
- Do not commit secrets, API keys, local `.env` files, generated audio, or benchmark artifacts that do not belong in version control.
- Prefer clear, small commits and descriptive pull request summaries.
- Update documentation when contributor setup, behavior, environment variables, or service logic changes.
- If you change API contracts, verify both the service endpoint and the frontend consumer still match.

---

## Pull request checklist

Before submitting your pull request, confirm the following:

- You tested the affected flow locally.
- The application still starts successfully in the environment you changed.
- You removed debug code, stray logs, and commented-out experiments.
- You documented any new setup steps, environment variables, or behavior changes.
- You kept the pull request scoped to one issue or topic.
- You added screenshots for UI changes when relevant.
- You did not commit secrets, API keys, sample private documents, or generated media outputs by mistake.
- You are opening the pull request against `dev/Audify`.

If one or more of these are missing, the pull request may be sent back for changes before review.

---

## Branching model

- Base new work from `dev/Audify`.
- Open pull requests against `dev/Audify`.
- Use descriptive branch names such as `fix/script-generation-timeout` or `docs/update-contributing-guide`.
- Rebase or merge the latest `dev/Audify` before opening your PR if your branch has drifted.

---

## Thank you

Thanks for contributing to Audify. Whether you are fixing a bug, improving the docs, refining the UI, strengthening the service architecture, or making the generation workflow more reliable, your work helps make the project more useful and easier to maintain.
