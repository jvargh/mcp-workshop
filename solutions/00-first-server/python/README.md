# Run samples

There are two samples here:

- `server.py`, showing a first server
- `server-api.py`, showing how to wrap an API.

## Create virtual environment

```bash
python -m venv venv
source ./venv/bin/activate
```

## Run first server

```bash
python server.py
```

You should see a message saying "Running the server"

### Try inspector

```bash
mcp dev server.py
```

OR 

```bash
npx @modelcontextprotocol/inspector
```

1. Go to configuration **Proxy session token** and paste the MCP_PROXY_AUTH_TOKEN value into it. 

1. Now try clicking "Connect"


## Try inspector CLI mode

```bash
npx @modelcontextprotocol/inspector --cli mcp run server.py --method tools/list
```

You should see:

```json
{
  "tools": [
    {
      "name": "add",
      "description": "Add two numbers",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "title": "A",
            "type": "integer"
          },
          "b": {
            "title": "B",
            "type": "integer"
          }
        },
        "required": [
          "a",
          "b"
        ],
        "title": "addArguments"
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "result": {
            "title": "Result",
            "type": "integer"
          }
        },
        "required": [
          "result"
        ],
        "title": "addOutput"
      }
    }
  ]
}
```

## Run server with wrapped API

```bash
python server-api.py
```

You should see the text "Running the server"

### Run tool

```bash
npx @modelcontextprotocol/inspector --cli mcp run server-api.py --method tools/call --tool-name joke
```

You should see a response similar to:

```json
{
  "content": [
    {
      "type": "text",
      "text": "Chuck Norris doent have to pray to the gods.the gods pray to Chuck Norris"
    }
  ],
  "structuredContent": {
    "result": "Chuck Norris doent have to pray to the gods.the gods pray to Chuck Norris"
  },
  "isError": false
}
```

Or try the other tool with:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server-api.py --method tools/call --tool-name joke_param --tool-arg category=travel
```

You should see a response similar to:

```text
{
  "content": [
    {
      "type": "text",
      "text": "Chuck Norris did in fact, build Rome in a day."
    }
  ],
  "structuredContent": {
    "result": "Chuck Norris did in fact, build Rome in a day."
  },
  "isError": false
}
```