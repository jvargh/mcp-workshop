---
sidebar_position: 1
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Servers with SSE

The stdio transport, that you've been using so far, enables communication through standard input and output streams. This is particularly useful for local integrations and command-line tools.

Now, we will cover SSE [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) transport. SSE is a standard for server-to-client streaming, allowing servers to push real-time updates to clients over HTTP. This is particularly useful for applications that require live updates, such as chat applications, notifications, or real-time data feeds. Also, your server can be used by multiple clients at the same time as it lives on a server that can be run somewhere in the cloud for example.

Here's what such a server can look like:

<Tabs>
<TabItem value="typescript" label="TypeScript">

```typescript
import express, { Request, Response } from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

const server = new McpServer({
  name: "example-server",
  version: "1.0.0"
});

// ... set up server resources, tools, and prompts ...

const app = express();

// to support multiple simultaneous connections we have a lookup object from
// sessionId to transport
const transports: {[sessionId: string]: SSEServerTransport} = {};

app.get("/sse", async (_: Request, res: Response) => {
  const transport = new SSEServerTransport('/messages', res);
  transports[transport.sessionId] = transport;
  res.on("close", () => {
    delete transports[transport.sessionId];
  });
  await server.connect(transport);
});

app.post("/messages", async (req: Request, res: Response) => {
  const sessionId = req.query.sessionId as string;
  const transport = transports[sessionId];
  if (transport) {
    await transport.handlePostMessage(req, res);
  } else {
    res.status(400).send('No transport found for sessionId');
  }
});

app.listen(3001);
```

In the preceding code we set up an Express server that listens to two endpoints:

- `/sse`: This endpoint is used to establish a connection with the server. When a client connects to this endpoint, a new `SSEServerTransport` instance is created and added to the `transports` object. The server then calls `server.connect(transport)` to start receiving messages from the client.
- `/messages`: This endpoint is used to handle incoming messages from the client. When a message is received, the server looks up the corresponding `SSEServerTransport` instance in the `transports` object and calls `transport.handlePostMessage(req, res)` to process the message.

</TabItem>
<TabItem value="python" label="Python" default>

```python
from starlette.applications import Starlette
from starlette.routing import Mount, Host
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("My App")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Mount the SSE server to the existing ASGI server
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)
```

In the preceding code we set up a Starlette server that listens to two endpoints:

- `/sse`: This endpoint is used to establish a connection with the server. When a client connects to this endpoint, a new `SSEServerTransport` instance is created and added to the `transports` object. The server is then ready to start receiving messages from the client.
- `/messages`: This endpoint is used to handle incoming messages from the client. When a message is received, the server looks up the corresponding `SSEServerTransport` instance and then proceeds to handle the message.

</TabItem>

</Tabs>


Now that we understand what SSE is, how to create such a server, let's practice it in the next activity.