---
sidebar_position: 3
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Activity: Add API to server

A tool like `add` is interesting to see how things work, but the real value comes from seeing how to use it in a real application. In this activity, you will add an API to the server you created in the previous activity.

So far, you've seen how we added a simple tool like `add` to the server. But what if we want to call a Web API? In this activity, you will add an API to the server you created in the previous activity.

## -1- Adding a tool calling an API

<Tabs>
<TabItem value="typescript" label="TypeScript">

Let's create a new file called `server-api.ts` with the following content:

```typescript

server.tool("random-joke","A joke returned by the chuck norris api",{},
    async () => {
      const response = await fetch("https://api.chucknorris.io/jokes/random");
      const data = await response.json();

      return {
        content: [
          {
            type: "text",
            text: data.value
          }
        ]
      };
    }
)
```

In the preceding code:

- The tool `random-joke` is created with a description saying "A joke returned by the chuck norris api". The input schema is empty, meaning it doesn't take any input, you can also omit this input parameter but I wanted to show you where the input schema goes.
- Then, we call the `fetch` function to call the API and get a random joke. The response is then parsed as JSON and returned as a text message.

</TabItem>
<TabItem value="python" label="Python" default>

Let's create a file `server-api.py`

```python
@mcp.tool()
async def joke() -> str:
    """Get joke"""
    res = requests.get("https://api.chucknorris.io/jokes/random")
    json_response = res.json()

    return json_response.get("value", "No joke found.")
```

</TabItem>
</Tabs>

## -2- Adding a tool that takes input

You saw how simply we can call an API, but what if we want to pass some input to the API? 


<Tabs>
<TabItem value="typescript" label="TypeSCript">

Add the following code to the `server-api.ts` file:

```typescript
const JokeByCategoryInputSchema = z.object({
    category: z.array(z.string())
}).shape;

server.tool("random-joke-by-category","A joke by category, from Chuck Norris API",
    JokeByCategoryInputSchema,
    async (input) => {
      const response = await fetch(`https://api.chucknorris.io/jokes/random?category=${input.category}`);
      const data = await response.json();

      if (!data.value) {
        throw new Error("No joke found for the specified category.");
      }
      return {
        content: [
          {
            type: "text",
            text: data.value
          }
        ]
      };
    }
)
```

In the preceding code:

- The tool `random-joke-by-category` is created with a description saying "A joke by category, from Chuck Norris API". The input schema is defined using Zod, which takes a category as input.
- Finally, we call the `fetch` function to call the API and get a random joke by category, see how we call the url `https://api.chucknorris.io/jokes/random?category=${input.category}`.

:::note
It's a good idea to define an input schema like we did here in a separate variable, both to make it easy to see what the input is and to reuse it in multiple places. 
:::

The full code for the server should look like this:

```typescript
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server
const server = new McpServer({
  name: "Chuck",
  version: "1.0.0"
});

// Add tool for getting a chuck norris joke

server.tool("random-joke","A joke returned by the chuck norris api",{},
    async () => {
      const response = await fetch("https://api.chucknorris.io/jokes/random");
      const data = await response.json();

      return {
        content: [
          {
            type: "text",
            text: data.value
          }
        ]
      };
    }
)

const JokeByCategoryInputSchema = z.object({
    category: z.array(z.string())
}).shape;

server.tool("random-joke-by-category","A joke by category, from Chuck Norris API",
    JokeByCategoryInputSchema,
    async (input) => {
      const response = await fetch(`https://api.chucknorris.io/jokes/random?category=${input.category}`);
      const data = await response.json();

      if (!data.value) {
        throw new Error("No joke found for the specified category.");
      }
      return {
        content: [
          {
            type: "text",
            text: data.value
          }
        ]
      };
    }
)


// Start receiving messages on stdin and sending messages on stdout
const transport = new StdioServerTransport();
await server.connect(transport);
console.log("Server started and listening for messages...");
```

</TabItem>
<TabItem value="python" label="Python" default>

```python
@mcp.tool()
async def joke_param(category: str = "sport") -> str:
    """Get joke with parameter"""
    
    res = requests.get(f"https://api.chucknorris.io/jokes/random?category={category}")
    json_response = res.json()

    return json_response.get("value", "No joke found.")
```

Here we add a new function `joke_param` and a parameter `category`.

</TabItem>
</Tabs>

## -3- Testing the server

Get in the habit of testing the server after each change. You can do this in several ways:

- Calling the inspector tool `npx @modelcontextprotocol/inspector node build/index.js`.
- You can also use a tool like curl or Postman to call the API directly (if this is a server using SSE or streamable HTTP). For example, you can call the API using curl like this:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"category": ["dev"]}' http://localhost:3000/random-joke-by-category
```

<Tabs>
<TabItem value="typescript" label="TypeScript">

```bash
```

</TabItem>
<TabItem value="python" label="Python" default>

Run the first tool:

```bash
npx @modelcontextprotocol/inspector --cli mcp run server-api.py --method tools/call --tool-name joke
```

Run the second tool with a param

```bash
npx @modelcontextprotocol/inspector --cli mcp run server-api.py --method tools/call --tool-name joke_param --tool-arg category=travel
```

</TabItem>
</Tabs>

## -4- Summary

You've learned to add an API in one of your tools. You can either add this code to your existing server, if you created from the previous activity, or you can work in that code into below GitHub repository:

```bash
git clone https://github.com/softchris/mcp-workshop.git
cd mcp-workshop
```

Follow the instructions in the README file.
