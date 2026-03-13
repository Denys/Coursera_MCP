# Coursera MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that connects Claude to [Coursera](https://www.coursera.org). It exposes course browsing, search, instructor and partner lookup, and specialization details — giving Claude full context about the Coursera catalog.

## Features

| Tool | Description |
|------|-------------|
| `coursera_list_courses` | List courses from the catalog (paginated) |
| `coursera_get_course` | Get full course details by ID |
| `coursera_get_course_by_slug` | Look up a course by its URL slug |
| `coursera_search_courses` | Search courses by keyword |
| `coursera_get_instructor` | Get instructor details by ID |
| `coursera_list_instructors` | List instructors (paginated) |
| `coursera_get_partner` | Get partner (university/org) details by ID |
| `coursera_list_partners` | List partners (paginated) |
| `coursera_get_specialization` | Get specialization details and course list |
| `coursera_list_specializations` | List specializations (paginated) |

**MCP Resources:**

- `coursera://course/{course_id}` — browse a course as a read-only resource
- `coursera://specialization/{specialization_id}` — browse a specialization as a resource

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

```bash
git clone https://github.com/Denys/Coursera_MCP.git
cd Coursera_MCP
uv sync
```

Or install from the repo directly:

```bash
pip install .
```

## Authentication

The Coursera Catalog API is **public** — no authentication is needed for browsing courses, instructors, partners, and specializations.

For accessing enrolled course content (future enhancement), set a CAUTH cookie from your Coursera session:

```bash
export COURSERA_CAUTH=your_cauth_cookie_value
```

Copy `.env.example` to `.env` for local development.

## Running

```bash
# Via uv
uv run coursera-mcp

# Or directly
python -m coursera_mcp.server
```

## Claude Desktop Integration

Add the following to your Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "coursera": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/Coursera_MCP",
        "run",
        "coursera-mcp"
      ]
    }
  }
}
```

Restart Claude Desktop after saving. You should see the Coursera tools appear when starting a new conversation.

## Development

```bash
# Install dev dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Lint
uv run ruff check src tests

# Run the MCP Inspector for interactive testing
uv run mcp dev src/coursera_mcp/server.py
```

## Project Structure

```
src/coursera_mcp/
├── server.py              # FastMCP app, tool + resource registrations
├── config.py              # Environment variable configuration
├── client.py              # Async httpx wrapper for the Coursera API
├── models.py              # Pydantic models for API responses
├── resources.py           # MCP resource handlers
└── tools/
    ├── courses.py         # Course operations (list, get, get by slug)
    ├── search.py          # Course search
    ├── instructors.py     # Instructor operations
    ├── partners.py        # Partner (university/org) operations
    └── specializations.py # Specialization operations
```

## License

MIT
