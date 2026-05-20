# n8n-builder

Julius uses this project to build production-ready n8n workflows. Claude Code has access to the n8n MCP server and n8n skills — use them together to design, validate, and deploy workflows in Julius's n8n instance.

## Available MCP tools

### Core tools (always available)
- `tools_documentation` — look up guidance on any MCP tool before using it
- `search_nodes` — full-text search across 1,650+ nodes with filters and example configs
- `get_node` — detailed node info: properties, operations, versions (minimal/standard/full modes)
- `validate_node` — validate a single node configuration before including it in a workflow
- `validate_workflow` — validate a complete workflow including AI agent checks
- `search_templates` — find existing templates by keyword, node type, task, or metadata
- `get_template` — retrieve complete workflow JSON from a template

### n8n management tools (requires API config)
- Workflow: create, get, update, delete, list, autofix, version management, deploy from template
- Execution: run tests, retrieve execution history
- Credential: list, get, create, update, delete
- Security: audit workflows
- System: health check for n8n API connectivity

## Available skills

These 7 skills are installed from https://github.com/czlonkowski/n8n-skills. Invoke them when relevant:

- **n8n MCP Tools Expert** — which MCP tool to use and how to format parameters (invoke first when unsure about tool usage)
- **n8n Workflow Patterns** — proven architectural patterns from 2,653+ templates
- **n8n Expression Syntax** — correct `{{ }}` expression syntax, variables, common mistakes
- **n8n Validation Expert** — interpreting validation errors and distinguishing real errors from false positives
- **n8n Node Configuration** — operation-aware node setup, property dependencies
- **n8n Code JavaScript** — production patterns for Code nodes (JS)
- **n8n Code Python** — Python in Code nodes and its limitations (no external libraries)

## How to build a workflow

1. **Understand the request** — ask clarifying questions if the trigger, data shape, or destination is ambiguous
2. **Search first** — run `search_templates` and `search_nodes` before building from scratch; reuse existing patterns where possible
3. **Build the full draft** — construct the complete workflow JSON autonomously
4. **Validate** — always run `validate_workflow` (and `validate_node` on complex nodes) before presenting
5. **Present with rationale** — explain key design decisions, node choices, and any tradeoffs
6. **Deploy only when asked** — use `workflow_deploy` or `create_workflow` only on explicit instruction from Julius

## Do not
- Deploy or modify workflows in the live instance without Julius saying to
- Create or delete credentials without confirmation
- Skip validation — always validate before presenting a workflow
- Invent node names or parameters — use `search_nodes` / `get_node` to confirm they exist
