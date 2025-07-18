# Run sample

## Create virtual environment

## Install dependencies

## Run server

```sh
uvicorn server:app --reload --port 8000
```

## List tools

Now that the server is up and running, try listing its tools with the following command (in a new terminal):

```sh
npx @modelcontextprotocol/inspector --cli http://localhost:8000/sse --method tools/list
```

You should see an outcome similar to:

```text
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

