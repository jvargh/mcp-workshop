---
sidebar_position: 3
---

# Consuming a server with an MCP client

Another way to connect and consume an MCP server is by using a client. This is similar to how you would connect to a server using a web browser or a command line tool like `curl`. The client programmatically connects to the server and sends requests for tools, resources and more, receiving responses in return.

Here's what a simple client might look like:

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "node",
  args: ["server.js"]
});

const client = new Client(
  {
    name: "example-client",
    version: "1.0.0"
  }
);

await client.connect(transport);

// List prompts
const prompts = await client.listPrompts();

// Get a prompt
const prompt = await client.getPrompt({
  name: "example-prompt",
  arguments: {
    arg1: "value"
  }
});

// List resources
const resources = await client.listResources();

// Read a resource
const resource = await client.readResource({
  uri: "file:///example.txt"
});

// Call a tool
const result = await client.callTool({
  name: "example-tool",
  arguments: {
    arg1: "value"
  }
});
```

In the preceding code, the client connects to the server using the `StdioClientTransport` transport, which allows it to communicate with the server via standard input and output. The client can then list prompts, resources, and tools, as well as read resources and call tools.

Let's learn to build this client step by step in our next activity.