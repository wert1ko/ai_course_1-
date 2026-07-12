# Prelegal Project

## Overview

This is a SaaS product to allow users to draft legal agreements based on templates in the templates directory. The user uses an AI chat in order to establish what document they want and how to fill in the fields. The available documents are covered in the catalog.json file in the project root, included here:

@catalog.json

Before we start: the initial implementation is a frontend-only prototype that only supports the Mutual NDA document with no AI chat.

## Development process

When instructed to build a feature:

1. Use your Atlassian tools to read the feature instructions from Jira
2. Develop the feature - do not skip any step from the feature-dev 7 step process
3. Thoroughly test the feature with unit tests and integration tests and fix any issues
4. Submit a PR using your github tools

## AI design

When writing code to make calls to LLMs, use your Cerebras skill to use LiteLLM via OpenRouter to the openrouter/openai/gpt-oss-120b model with Cerebras as the inference provider. You should use Structured Outputs so that you can interpret the results and populate fields in the legal document.

There is an OPENROUTER_API_KEY in the .env file in the project root.

## Technical design

The entire project should be packaged into a Docker container. The backend should be in backend/ and be a uv project, using FastAPI. The frontend should be in frontend/ Consider statically building the frontend and serving it via FastAPI, if that will work. There should be scripts in scripts/ for:

​```
# Mac
scripts/start-mac.sh     # Start
scripts/stop-mac.sh      # Stop

# Linux
scripts/start-linux.sh
scripts/stop-linux.sh

# Windows
scripts/start-windows.ps1
scripts/stop-windows.ps1
​```

Backend available at http://localhost:8000

## Color Scheme

- Accent Amber: `#F5B942` — accent lines, highlights
- Blue Primary: `#3B9EFF` — links, key sections
- Purple Secondary: `#8B5CF6` — submit buttons, important actions
- Dark Navy: `#0B1120` — headings / base background
- Gray Text: `#94A3B8` — supporting text, labels