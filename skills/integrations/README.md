# integrations

Skills for third-party service integrations, ML tooling, AI model APIs, and platform connectors. This is the largest category - 88 skills covering everything from calendar and email to fine-tuning frameworks, ML inference, and niche SaaS tools.

Prerequisite tools: varies widely per skill. Most web-API skills require `curl`. ML skills typically require Python 3.10+ and specific pip packages. See each skill's SKILL.md for full prerequisites.

## Skills

| Skill | Description | Required env | Compat |
|-------|-------------|-------------|--------|
| [1password](1password/) | 1Password CLI integration for secret retrieval and vault management | OP_SERVICE_ACCOUNT_TOKEN | Both |
| [appie-content-intelligence](appie-content-intelligence/) | Content performance analysis and distribution intelligence layer | - | Both |
| [arxiv](arxiv/) | Search and fetch arxiv papers by ID, title, or keyword | - | Both |
| [axolotl](axolotl/) | Axolotl fine-tuning framework: configure, run, and monitor LoRA/QLoRA jobs | GPU, Python | Both |
| [blogwatcher](blogwatcher/) | Monitor RSS feeds and blogs for new content, trigger on updates | - | Both |
| [canvas](canvas/) | HTML5 Canvas API for programmatic drawing and diagram generation | - | Both |
| [clip](clip/) | OpenAI CLIP model for image-text similarity and zero-shot classification | Python | Both |
| [code-review](code-review/) | Structured code review checklist and automated review workflow | - | Both |
| [creative-ideation](creative-ideation/) | Brainstorm and expand creative concepts with structured ideation techniques | - | Both |
| [dispatch-multiple-agents](dispatch-multiple-agents/) | Spawn and coordinate multiple parallel sub-agents for concurrent tasks | - | Hermes |
| [doing-tasks](doing-tasks/) | Task execution framework for structured multi-step agent work | - | Both |
| [fal-ai](fal-ai/) | fal.ai image and video generation: Nano Banana, Kling, Hunyuan3D. Primary image gen | FAL_KEY | Both |
| [findmy](findmy/) | Apple Find My integration for location tracking (macOS only) | - | OpenClaw |
| [gguf](gguf/) | Run GGUF quantized models locally via llama.cpp | - | Both |
| [gh-issues](gh-issues/) | GitHub Issues: create, label, comment, close via gh CLI | GH_TOKEN | Both |
| [gif-search](gif-search/) | Search and retrieve GIFs via Tenor or Giphy API | GIPHY_API_KEY | Both |
| [gifgrep](gifgrep/) | Find GIFs matching a description using local embedding search | - | Both |
| [godmode](godmode/) | Extended agent permissions for trusted autonomous task execution | - | Hermes |
| [gog](gog/) | Google OAuth token management and refresh for GWS API access | GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET | Both |
| [gog-calendar-events](gog-calendar-events/) | Google Calendar event management via OAuth token refresh flow | GOOGLE_OAUTH | Both |
| [goplaces](goplaces/) | Google Places API: search locations, get details, reviews | GOOGLE_PLACES_API_KEY | Both |
| [grpo-rl-training](grpo-rl-training/) | GRPO reinforcement learning training for LLM fine-tuning | GPU, Python | Both |
| [gws-calendar](gws-calendar/) | Google Calendar: read events, check availability, manage calendars | GOOGLE_OAUTH | Both |
| [gws-calendar-agenda](gws-calendar-agenda/) | Fetch and format daily/weekly agenda from Google Calendar | GOOGLE_OAUTH | Both |
| [gws-calendar-insert](gws-calendar-insert/) | Create and update Google Calendar events with attendees and conferencing | GOOGLE_OAUTH | Both |
| [gws-classroom](gws-classroom/) | Google Classroom: manage courses, assignments, and student submissions | GOOGLE_OAUTH | Both |
| [gws-events](gws-events/) | Google Workspace Events: subscribe to resource changes and push notifications | GOOGLE_OAUTH | Both |
| [gws-events-subscribe](gws-events-subscribe/) | Subscribe to Google Workspace Events for real-time resource change notifications | GOOGLE_OAUTH | Both |
| [gws-gmail](gws-gmail/) | Gmail full access: read, search, label, archive, delete messages | GOOGLE_OAUTH | Both |
| [gws-gmail-send](gws-gmail-send/) | Send Gmail messages with attachment support and threading | GOOGLE_OAUTH | Both |
| [gws-keep](gws-keep/) | Google Keep: create notes, manage lists, add reminders | GOOGLE_OAUTH | Both |
| [gws-meet](gws-meet/) | Google Meet: create meeting links, manage spaces, invite participants | GOOGLE_OAUTH | Both |
| [gws-modelarmor](gws-modelarmor/) | Google Cloud Model Armor: prompt and response sanitization | GOOGLE_CLOUD_PROJECT | Both |
| [gws-people](gws-people/) | Google People API: read contacts, manage directory entries | GOOGLE_OAUTH | Both |
| [gws-shared](gws-shared/) | Shared Google Workspace utility functions used across GWS skills | GOOGLE_OAUTH | Both |
| [gws-workflow](gws-workflow/) | Multi-step Google Workspace automation workflows | GOOGLE_OAUTH | Both |
| [higgsfield-image](higgsfield-image/) | Higgsfield.ai image generation for cinematic-quality visuals | HIGGSFIELD_API_KEY | Both |
| [huggingface-hub](huggingface-hub/) | HuggingFace Hub: download models, datasets, upload artifacts | HF_TOKEN | Both |
| [jupyter-live-kernel](jupyter-live-kernel/) | Connect to a running Jupyter kernel for live code execution and inspection | - | Both |
| [llama-cpp](llama-cpp/) | Run llama.cpp models locally. Server mode, quantization, prompt formatting | - | Both |
| [llm-wiki](llm-wiki/) | Search and query a local LLM-indexed knowledge wiki | - | Both |
| [lm-evaluation-harness](lm-evaluation-harness/) | EleutherAI LM Evaluation Harness for benchmarking language models | Python, GPU | Both |
| [mcporter](mcporter/) | MCP server port manager for running multiple MCP servers concurrently | - | Both |
| [n8n](n8n/) | Interact with n8n workflows: list, trigger, monitor, manage automations | N8N_API_KEY | Both |
| [n8n-pro](n8n-pro/) | Advanced n8n fleet management: backup, health monitoring, hardening | N8N_API_KEY | Both |
| [nano-pdf](nano-pdf/) | Parse and extract content from PDF files | - | Both |
| [notion](notion/) | Notion workspace: read pages, create entries, update databases | NOTION_API_KEY | Both |
| [notion-masterclass](notion-masterclass/) | Notion operations: source-of-truth protocol, clarity framework, chaos-to-execution pipeline | NOTION_API_KEY | Both |
| [obliteratus](obliteratus/) | Bulk delete and cleanup tool for files, records, and data artifacts | - | Both |
| [openai-whisper](openai-whisper/) | Transcribe audio files using OpenAI Whisper locally via CLI | Python | Both |
| [openai-whisper-api](openai-whisper-api/) | Transcribe audio using OpenAI Whisper API endpoint | OPENAI_API_KEY | Both |
| [oracle](oracle/) | Oracle Database connectivity and SQL query execution | ORACLE_DSN | Both |
| [p5js](p5js/) | Generate p5.js creative coding sketches for visual art and animation | - | Both |
| [peft](peft/) | HuggingFace PEFT library for parameter-efficient fine-tuning (LoRA, QLoRA, etc.) | Python, GPU | Both |
| [persona-content-creator](persona-content-creator/) | Create, organize, and distribute content across Google Workspace | GOOGLE_OAUTH | Both |
| [pokemon-player](pokemon-player/) | Play Pokemon via emulator automation (for fun / demo) | - | Both |
| [polymarket](polymarket/) | Query Polymarket prediction markets for odds and event data | - | Both |
| [popular-web-designs](popular-web-designs/) | Reference library of high-converting web design patterns | - | Both |
| [pretext](pretext/) | PreTeXt document authoring for structured academic and technical content | Python | Both |
| [python-debugpy](python-debugpy/) | Python debugpy remote debugger integration for live session inspection | Python | Both |
| [pytorch-fsdp](pytorch-fsdp/) | PyTorch FSDP (Fully Sharded Data Parallel) training configuration | GPU, Python | Both |
| [ralph-wiggum](ralph-wiggum/) | Absurdist humor and random non-sequitur generation (for entertainment) | - | Both |
| [recipe-watch-drive-changes](recipe-watch-drive-changes/) | Watch Google Drive for file changes and trigger downstream actions | GOOGLE_OAUTH | Both |
| [requesting-code-review](requesting-code-review/) | Structured workflow for requesting and incorporating code review feedback | - | Both |
| [sag](sag/) | Structured agent graph for multi-step reasoning pipelines | - | Both |
| [segment-anything](segment-anything/) | Meta Segment Anything Model for image segmentation | Python, GPU | Both |
| [seo-checklist](seo-checklist/) | Pre-publish on-page SEO checklist: title, meta, H1, keywords, images, breadcrumbs | - | Both |
| [sketch](sketch/) | Sketch vector design file reading and export automation | macOS | OpenClaw |
| [skill-creator](skill-creator/) | Scaffold new Hermes/OpenClaw skills from templates | - | Both |
| [spark-comfy](spark-comfy/) | Generate images via Spark Atlas's ComfyUI inference API. Tailnet-only access with X-API-Key auth. | SPARK_API_KEY | Both |
| [spike](spike/) | Spike.sh incident management and on-call alerting | SPIKE_API_KEY | Both |
| [spotify](spotify/) | Spotify Web API: search, playback control, playlist management | SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET | Both |
| [subagent-driven-development](subagent-driven-development/) | Dispatch multiple sub-agents to implement features in parallel with review gates | - | Hermes |
| [systematic-debugging](systematic-debugging/) | Structured debugging protocol: reproduce, isolate, hypothesize, verify, fix | - | Both |
| [test-driven-development](test-driven-development/) | TDD workflow: red-green-refactor cycle with coverage enforcement | - | Both |
| [touchdesigner-mcp](touchdesigner-mcp/) | TouchDesigner MCP server for generative visual and audio programming | TouchDesigner | Both |
| [trello](trello/) | Trello board management: cards, lists, checklists via Trello API | TRELLO_API_KEY, TRELLO_TOKEN | Both |
| [trl-fine-tuning](trl-fine-tuning/) | HuggingFace TRL library for RLHF and reward model training | Python, GPU | Both |
| [unsloth](unsloth/) | Unsloth optimized fine-tuning for 2x faster LoRA training | Python, GPU | Both |
| [venice](venice/) | Venice.ai API for privacy-focused LLM inference | VENICE_API_KEY | Both |
| [vllm](vllm/) | vLLM inference server configuration and management for local GPU serving | GPU, Python | Both |
| [webflow](webflow/) | Webflow CMS and site management via Webflow API | WEBFLOW_API_KEY | Both |
| [whisper](whisper/) | Whisper transcription skill (faster-whisper backend, large-v3 default) | Python | Both |
| [write-plan](write-plan/) | Write structured implementation plans before coding | - | Both |
| [writing-plans](writing-plans/) | Extended planning skill with multi-phase breakdown and risk analysis | - | Both |
| [xitter](xitter/) | X (Twitter) posting, thread management, and engagement via API | X_API_KEY, X_API_SECRET | Both |
| [xurl](xurl/) | URL expansion, redirect tracing, and link preview extraction | - | Both |
| [youtube-content](youtube-content/) | YouTube channel management: upload, update metadata, manage playlists | YOUTUBE_API_KEY | Both |

## Install

```bash
cp -r skills/integrations/<skill> ~/.hermes/skills/
# or for OpenClaw:
cp -r skills/integrations/<skill> ~/.openclaw/skills/
```
