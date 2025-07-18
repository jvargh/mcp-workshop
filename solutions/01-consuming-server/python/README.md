# Run the sample code

To run this sample, follow the below instructions.

## Create virtual environment

```sh
python -m venv venv
```

```sh
source ./venv/bin/activate
```

## Install dependencies

```sh
pip install "mcp[cli]"
```

## Run sample

```sh
python client.py
```

You should see output similar to:

```text
LISTING RESOURCES
Resource:  ('meta', None)
Resource:  ('nextCursor', None)
Resource:  ('resources', [])
                    INFO     Processing request of type ListToolsRequest                                       server.py:625
LISTING TOOLS
Tool:  add
READING RESOURCE
                    INFO     Processing request of type ReadResourceRequest                                    server.py:625
CALL TOOL
                    INFO     Processing request of type CallToolRequest                                        server.py:625
[TextContent(type='text', text='8', annotations=None, meta=None)]
```

Call tool response is the result of adding 1 to 7. Modify this row ` result = await session.call_tool("add", arguments={"a": 1, "b": 7})` for a different response.

## Run LLM Client

You need to install the following:

```sh
pip install "mcp[cli]"
pip install openai
pip install azure-ai-inference
```

Run the client:

```sh
python client.py
```

You should see an output similar to:

```text
LISTING RESOURCES
Resource:  ('meta', None)
Resource:  ('nextCursor', None)
Resource:  ('resources', [])
                    INFO     Processing request of type ListToolsRequest                                       server.py:625
LISTING TOOLS
Tool:  add
Tool {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}
CALLING LLM
TOOL:  {'function': {'arguments': '{"a":2,"b":20}', 'name': 'add'}, 'id': 'call_2ByUW3oX5f2eNvJ6Vn4tdSrK', 'type': 'function'}
[07/18/25 19:07:08] INFO     Processing request of type CallToolRequest                                        server.py:625
TOOLS result:  [TextContent(type='text', text='22', annotations=None, meta=None)]
```

Locate the following line `prompt = "Add 2 to 20"` and modify it if you want to see a different response. Experiment by adding more tools on the server and ensure the client is able to call them.

