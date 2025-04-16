---
sidebar_position: 2
---

# Activity: Create a first MCP server

## What a server can do

An MCP Server is a program that exposes specific capabilities through the MCP protocol. It can be a simple script or a complex application, depending on the use case. The server can interact with local data sources, remote services, and other tools to provide context to LLMs.

For example, an MCP server can:

- Access local files and databases
- Connect to remote APIs
- Perform computations
- Integrate with other tools and services
- Provide a user interface for interaction

## Creating a simple server

To create a server, you need to follow these steps:

- Install the MCP SDK.
- Create a new Node.js project and set up the project structure.
- Write the server code.
- Test the server.

### -1- Install the MCP SDK

:::note
Make sure you have installed Node.js before running the code below. You can check if you have it installed by running `node -v` in your terminal.
:::

1. Install dependencies:

    ```bash
    npm install @modelcontextprotocol/sdk zod
    npm install -D @types/node typescript
    ```

### -2- Create a new Node.js project

Create the project structure by following these steps:

1. Create a `src` folder
    
    ```bash
    mkdir src
    ```

1. Create a file named `index.ts` in `src` folder.
 
1. Scaffold a new Node.js project by running the following command in the root folder:

    ```bash
    npm init -y
    ```

1. Update the `package.json` to include the following:

   ```json
   {
      "type": "module",
      "bin": {
        "weather": "./build/index.js"
      },
      "scripts": {
        "build": "tsc && chmod 755 build/index.js"
      },
      "files": [
        "build"
      ],
   }
   ```

   For Windows, change `build` to:

   ```json
   "build": "tsc && node ./build/index.js"
   ```
   

1. Create `tsconfig.json` in the root folder with the following content:

    ```json
    {
      "compilerOptions": {
        "target": "ES2022",
        "module": "Node16",
        "moduleResolution": "Node16",
        "outDir": "./build",
        "rootDir": "./src",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true
      },
      "include": ["src/**/*"],
      "exclude": ["node_modules"]
    }
    ```

### -3- Create the server

1. Let's start by adding code to `index.ts` to create a simple MCP server:

   ```typescript
   import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
   import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
   import { z } from "zod";
    
   // Create an MCP server
   const server = new McpServer({
     name: "Demo",
     version: "1.0.0"
   });
   ```

   Next, let's add tools to the server.

1. Add a tool by adding the following code to `index.ts`:

   ```typescript
   server.tool("add",
      { a: z.number(), b: z.number() },
      async ({ a, b }) => ({
        content: [{ type: "text", text: String(a + b) }]
      })
    );
   ```

   The code above adds a tool called "add" with input parameters `a` and `b`, both of type `number`. The tool returns the sum of `a` and `b` as a text message. We will later show how you can call this tool from a client.

1. Add a resource by adding the following code to `index.ts`:

   ```typescript
   server.resource(
      "greeting",
      new ResourceTemplate("greeting://{name}", { list: undefined }),
      async (uri, { name }) => ({
        contents: [{
          uri: uri.href,
          text: `Hello, ${name}!`
        }]
      })
    );
   ```

   The preceding code adds a resource called "greeting" with a URI template `greeting://{name}`. The idea is that if you invoke this resource with a name, e.g `greeting://John`, it will return a greeting message "Hello, John!".

1. Lastly, let's add code to start the server and listen for incoming messages. Add the following code to `index.ts`:

   ```typescript
   // Start receiving messages on stdin and sending messages on stdout
   const transport = new StdioServerTransport();
   await server.connect(transport);
   ```

Here's the full code for reference:

```typescript
// index.ts
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server
const server = new McpServer({
  name: "Demo",
  version: "1.0.0"
});

// Add an addition tool
server.tool("add",
  { a: z.number(), b: z.number() },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a + b) }]
  })
);

// Add a dynamic greeting resource
server.resource(
  "greeting",
  new ResourceTemplate("greeting://{name}", { list: undefined }),
  async (uri, { name }) => ({
    contents: [{
      uri: uri.href,
      text: `Hello, ${name}!`
    }]
  })
);

// Start receiving messages on stdin and sending messages on stdout
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Testing our server

So far, you've created a simple MCP server and your file directory structure should look like this:

```bash
src/
├── index.ts
package.json
package-lock.json
tsconfig.json
```

Your server has a tool "add" and a resource "greeting". The server is ready to receive messages on stdin and send messages on stdout.

### -1- Run the inspector tool

The easiest way to test your server is to use the inspector tool. It's a tool we can run via `npx`, let's add it as a command to `package.json`:

```json
{
  "scripts": {
    "build": "tsc && chmod 755 build/index.js",
    "inspector": "npx @modelcontextprotocol/inspector node build/index.js"
  }
}
```

- Run the inspector tool by running the following command in your terminal:

    ```bash
    npm run inspector
    ```

    You should see a window like this:

    ![Connect](/img/connect.png)

### -2- Connect to the server

- Select to "Connect" and you should see the window below:

    ![Connect](/img/connected.png)

- Select "List tools", to see what tools are available:

   ![Connect](/img/tools-listed.png)

### -3- Run the tool

- Select "add" and a dialog on your right will ask you to fill in the parameters:

   ![Connect](/img/running-tool.png)  

- You should see the result of the tool in the inspector, see **16** in the bottom result:

   ![Connect](/img/ran-tool.png)

Congrats, you've managed to create a simple MCP server and run the inspector tool to test it!

You're ready for your next challenge, creating a client that can call the server and use the tools and resources you've created.