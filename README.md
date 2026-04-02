# Oura MCP Server (Enhanced)

An MCP (Model Context Protocol) server that provides comprehensive access to the [Oura Ring API v2](https://cloud.ouraring.com/v2/docs). Exposes 17 tools covering sleep, activity, heart rate, stress, SpO2, workouts, and more.

Built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk) and [httpx](https://www.python-httpx.org/).

## Tools

### Sleep & Recovery
| Tool | Description |
|------|-------------|
| `get_sleep_data` | Detailed sleep sessions -- stages, heart rate, HRV, breathing rate |
| `get_daily_sleep` | Daily sleep scores and contributor breakdown |
| `get_sleep_time` | Recommended and actual sleep timing windows |
| `get_daily_readiness` | Readiness scores and contributors (HRV balance, body temp, etc.) |
| `get_daily_resilience` | Recovery capacity and stress tolerance indicators |

### Activity & Fitness
| Tool | Description |
|------|-------------|
| `get_daily_activity` | Steps, calories, active time breakdown, MET levels |
| `get_workouts` | Workout sessions with type, calories, distance, duration |
| `get_sessions` | Guided sessions (meditation, breathing) with biometrics |
| `get_vo2_max` | VO2 max cardiovascular fitness estimates |

### Health Vitals
| Tool | Description |
|------|-------------|
| `get_heart_rate` | Heart rate at 5-minute intervals (uses datetime params) |
| `get_daily_spo2` | Daily blood oxygen saturation |
| `get_daily_stress` | Daily stress levels and recovery summary |
| `get_daily_cardiovascular_age` | Estimated cardiovascular age |

### User & Device
| Tool | Description |
|------|-------------|
| `get_personal_info` | User profile (age, weight, height) |
| `get_ring_configuration` | Ring model, color, firmware, setup date |
| `get_rest_mode` | Rest mode periods and schedules |
| `get_tags` | User-created lifestyle tags and annotations |

All tools with date parameters accept optional `start_date` and `end_date` in `YYYY-MM-DD` format. When omitted, the Oura API defaults to recent data.

## Setup

### Option A: Claude Desktop Extension (recommended)

1. Download the latest `oura-mcp-server-enhanced.mcpb` from [Releases](https://github.com/josuhr/oura-mcp-server-enhanced/releases)
2. Open Claude Desktop > Settings > Extensions
3. Select the `.mcpb` file and follow the prompts
4. Enter your [Oura API Token](https://cloud.ouraring.com/personal-access-tokens) when prompted

### Option B: Manual Setup

#### 1. Get an Oura API Token

Go to [Oura Personal Access Tokens](https://cloud.ouraring.com/personal-access-tokens) and create a new token.

#### 2. Install

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/josuhr/oura-mcp-server-enhanced.git
cd oura-mcp-server-enhanced
uv venv && uv pip install -e .
```

#### 3. Configure Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "oura": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/oura-mcp-server-enhanced", "oura-mcp-server"],
      "env": {
        "OURA_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

Replace `/path/to/oura-mcp-server-enhanced` with the actual path and `your_token_here` with your Oura API token.

#### 4. Run Standalone (optional)

```bash
export OURA_API_TOKEN="your_token_here"
oura-mcp-server
```

### Building the Extension

To build the `.mcpb` extension bundle from source:

```bash
zip -r oura-mcp-server-enhanced.mcpb manifest.json pyproject.toml uv.lock src/ .python-version -x "src/**/__pycache__/*"
```

## Project Structure

```
src/oura_mcp_server/
├── __init__.py       # Package entry point
├── server.py         # FastMCP tool definitions and main()
├── client.py         # Async HTTP client for Oura API v2
└── transforms.py     # Human-readable data formatting
```

## Credits

Inspired by [tomekkorbak/oura-mcp-server](https://github.com/tomekkorbak/oura-mcp-server), extended to cover the full Oura API v2.
