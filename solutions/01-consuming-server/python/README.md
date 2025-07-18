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