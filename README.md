# pyagent-ai

A toy AI coding agent built from boot.dev's "Build an AI Agent" course. It's an
OpenRouter-backed CLI chatbot that can list files, read files, write files,
and execute Python files, iterating on its own tool calls (up to 20 times)
until it produces a final answer.

## Setup

1. Install [uv](https://docs.astral.sh/uv/) if you don't already have it.
2. Install dependencies:

   ```
   uv sync
   ```
3. Create a `.env` file in the project root with an OpenRouter API key
   ([get a free one here](https://openrouter.ai/keys)):

   ```
   OPENROUTER_API_KEY=sk-or-...
   ```

## Usage

```
uv run main.py "list the files in the working directory"
```

Add `--verbose` to see prompt/response token counts and each tool call's
result:

```
uv run main.py "fix the bug: 3 + 7 * 2 shouldn't be 20" --verbose
```

The agent currently operates on the `calculator/` directory (a small sample
app bundled in this repo). Its working directory is sandboxed via
`functions/common.py::resolve_within`, so it can't read, write, or execute
anything outside that directory.

## Running tests

Each tool function has a small standalone test script:

```
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_run_python_file.py
uv run test_write_file.py
```

The bundled calculator app has real unit tests:

```
uv run calculator/tests.py
```

## Project structure

- `main.py`: CLI entrypoint and the agent loop
- `prompts.py`: system prompt
- `functions/`: the four LLM-callable tools (`get_files_info`,
  `get_file_content`, `run_python_file`, `write_file`), their JSON schemas,
  and `call_function.py`, which dispatches a model's tool call to the right
  function
- `calculator/`: sample app the agent operates on

## Extension roadmap

Ideas for pushing past the course requirements, roughly in priority order.
Each one is a single, shippable slice.

### 1. Diff-based file editing

`write_file` currently overwrites an entire file to make any change, however
small. That's expensive in tokens and risky for large files. Add an
`edit_file` tool that does a targeted find-and-replace instead.

**Requirements:**
- New `functions/edit_file.py` with `edit_file(working_directory, file_path, old_string, new_string)`, sandboxed via `resolve_within` like the other four tools
- Error clearly if `old_string` isn't found or matches more than once, instead of silently guessing
- JSON schema requiring `file_path`, `old_string`, `new_string`, registered in `call_function.py`'s `function_map` and `available_functions`
- Update `prompts.py` so the model prefers `edit_file` for existing files and reserves `write_file` for creating new ones
- `test_edit_file.py` following the existing test-script pattern

### 2. Parameterize the working directory

`call_function.py` hardcodes `working_directory = "./calculator"`, so trying
the agent on another codebase currently means editing source. Make it a
runtime option.

**Requirements:**
- `--working-dir` CLI flag on `main.py`, defaulting to `calculator` to preserve current behavior
- Thread the value through to `call_function()` instead of the hardcoded literal
- Validate the path exists and is a directory before entering the agent loop; fail fast with a clear error otherwise
- Update the README usage section with an example pointed at a different project

### 3. Search/grep tool

With only `get_files_info` and `get_file_content`, the agent can only
discover code by crawling directories one level at a time. That doesn't
scale past a toy project. Add a tool that searches file contents directly.

**Requirements:**
- New `functions/search_files.py` with `search_files(working_directory, pattern, directory=".")`, recursively matching `pattern` (plain text or regex) across files under `directory`, sandboxed via `resolve_within`
- Return results as `path:line: content` strings, truncated with the same style of `[...truncated]` marker `get_file_content` uses, so a broad pattern can't blow up the context
- JSON schema + `function_map`/`available_functions` registration
- Update `prompts.py` to suggest searching before reading files one by one

### 4. Pin a specific `:free` model

`main.py` hardcodes `model="openrouter/free"`, which routes to whichever
free model OpenRouter currently has available, so behavior isn't
reproducible run to run. Make the model configurable and pin a known one.

**Requirements:**
- Replace the hardcoded model string with a `MODEL` constant (or a `--model` CLI flag with that constant as the default)
- Pick a specific `:free`-suffixed model from [openrouter.ai/models](https://openrouter.ai/models) as the default and note it in this README
- Confirm the chosen model still supports the `tools` parameter (not all free models do) by re-running the four core scenarios from the course (list/read/write/run)

## Safety note

This agent gives an LLM read, write, and execute access to a directory on
your machine. It's a learning toy. Don't point it at anything you don't have
backed up, and don't give it credentials or access beyond its sandboxed
working directory.
