---
sidebar_position: 6
---

# Activity: Create an MCP client using LLM

Let's add an LLM and ensure the LLM is what's between the user and the server. Here's how it will work on high level:

1. The client will call the server and get information about its tools. Based on this response, the client will remember the tools and their parameters.
2. The user then asks the client a question which in turn will call the LLM to get a response. If the LLM deems it necessary, it will call the server's tools to get more information. 

Next, let's implement this in code.

## -1- Create a client file

Use your existing Node.js project but add a `Client.ts` file.

1. Add the following code to `Client.ts`:

    ```typescript
    import { Client } from "@modelcontextprotocol/sdk/client/index.js";
    import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
    import { Transport } from "@modelcontextprotocol/sdk/shared/transport.js";
    import OpenAI from "openai";
    import { z } from "zod"; // Import zod for schema validation
    ```

    Now you have all the imports you need including OpenAI and you've instantiated an openai client. Next, let's add code to create the client and connect to the server.

1. Add the following code to create a client class:

    ```typescript
    class MCPClient {
        private openai: OpenAI;
        private client: Client;
        constructor(){
            this.openai = new OpenAI({
                baseURL: "https://models.inference.ai.azure.com", 
                apiKey: process.env.GITHUB_TOKEN,
            });
    
            this.client = new Client(
                {
                    name: "example-client",
                    version: "1.0.0"
                },
                {
                    capabilities: {
                    prompts: {},
                    resources: {},
                    tools: {}
                    }
                }
                );    
        }
    }
    ```

    In the preceding code:

    - `MCPClient` is defined as a class that will handle the connection to the server and the LLM.
    - A constructor is defined that initializes the OpenAI client and the MCP client. The OpenAI client is initialized with the base URL and API key. The MCP client is initialized with the name and version.  

    Great, we now have a client that can connect to the server. Next, let's add more code to wire up the LLM and the server.

1. Add the following so we can connect to the server:

   ```typescript
   async connectToServer(transport: Transport) {
        await this.client.connect(transport);
        this.run();
        console.error("MCPClient started on stdin/stdout");
   }
   ```
    
    It doesn't do much other than connect to the server and run the client. 

1. Let's add the following code to help us convert an MCP tool response into a tool an LLM can understand:

   ```typescript
   openAiToolAdapter(tool: {
        name: string;
        description?: string;
        input_schema: any;
          }) {
          // Create a zod schema based on the input_schema
          const schema = z.object(tool.input_schema);
      
          return {
            type: "function" as const, // Explicitly set type to "function"
            function: {
              name: tool.name,
              description: tool.description,
              parameters: {
              type: "object",
              properties: tool.input_schema.properties,
              required: tool.input_schema.required,
              },
            },
          };
    }
    ```

1. Next, let's add a function that lets us process a response from an LLM and make a tool call if the LLM indicates a tool should be called:

    ```typescript
    async callTools(
        tool_calls: OpenAI.Chat.Completions.ChatCompletionMessageToolCall[],
        toolResults: any[]
      ) {
        for (const tool_call of tool_calls) {
          const toolName = tool_call.function.name;
          const args = tool_call.function.arguments;
    
          console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);
    
    
          // 2. Call the server's tool 
          const toolResult = await this.client.callTool({
            name: toolName,
            arguments: JSON.parse(args),
          });
    
          console.log("Tool result: ", toolResult);
    
          // 3. Do something with the result
          // TODO  
    
         }
    }
    ```

    In the preceding code:

    - The `callTools` function takes an array of tool calls and their results. It iterates over the tool calls, calling each tool on the server and logging the result.
    - See the part where we call `callTool` with a tool name and arguments. This is how we call a tool on the server. The result is then logged to the console.

1. Finally, we add the function that sets everything up called `run`

    ```typescript
    async run() {
        console.log("Asking server for available tools");
        const toolsResult = await this.client.listTools();
        const tools = toolsResult.tools.map((tool) => {
            return this.openAiToolAdapter({
              name: tool.name,
              description: tool.description,
              input_schema: tool.inputSchema,
            });
        });
    
        const messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [
            {
                role: "user",
                content: "What is the sum of 2 and 3?",
            },
        ];

        console.log("Querying LLM: ", messages[0].content);
        let response = this.openai.chat.completions.create({
            model: "gpt-4o-mini",
            max_tokens: 1000,
            messages,
            tools: tools,
        });    

        let results: any[] = [];
    
        // 1. Go through the LLM response,for each choice, check if it has tool calls 
        (await response).choices.map(async (choice: { message: any; }) => {
          const message = choice.message;
          if (message.tool_calls) {
              console.log("Making tool call")
              await this.callTools(message.tool_calls, results);
          }
        });
    }
    ```

    In the preceding code:

    - The `run` function first queries the server for available tools and converts them into a format that the LLM can understand.
    - It then sends a message to the LLM asking for the sum of 2 and 3.
    - If the LLM indicates that a tool should be called, it calls the `callTools` function to handle the tool call.
    
Here's the full code for reference:

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { Transport } from "@modelcontextprotocol/sdk/shared/transport.js";
import OpenAI from "openai";
import { z } from "zod"; // Import zod for schema validation

class MyClient {
    private openai: OpenAI;
    private client: Client;
    constructor(){
        this.openai = new OpenAI({
            baseURL: "https://models.inference.ai.azure.com", // might need to change to this url in the future: https://models.github.ai/inference
            apiKey: process.env.GITHUB_TOKEN,
        });

       
        
        this.client = new Client(
            {
                name: "example-client",
                version: "1.0.0"
            },
            {
                capabilities: {
                prompts: {},
                resources: {},
                tools: {}
                }
            }
            );    
    }

    async connectToServer(transport: Transport) {
        await this.client.connect(transport);
        this.run();
        console.error("MCPClient started on stdin/stdout");
    }

    openAiToolAdapter(tool: {
        name: string;
        description?: string;
        input_schema: any;
          }) {
          // Create a zod schema based on the input_schema
          const schema = z.object(tool.input_schema);
      
          return {
            type: "function" as const, // Explicitly set type to "function"
            function: {
              name: tool.name,
              description: tool.description,
              parameters: {
              type: "object",
              properties: tool.input_schema.properties,
              required: tool.input_schema.required,
              },
            },
          };
    }
    
    async callTools(
        tool_calls: OpenAI.Chat.Completions.ChatCompletionMessageToolCall[],
        toolResults: any[]
      ) {
        for (const tool_call of tool_calls) {
          const toolName = tool_call.function.name;
          const args = tool_call.function.arguments;
    
          console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);
    
    
          // 2. Call the server's tool 
          const toolResult = await this.client.callTool({
            name: toolName,
            arguments: JSON.parse(args),
          });
    
          console.log("Tool result: ", toolResult);
    
          // 3. Do something with the result
          // TODO  
    
         }
    }

    async run() {
        console.log("Asking server for available tools");
        const toolsResult = await this.client.listTools();
        const tools = toolsResult.tools.map((tool) => {
            return this.openAiToolAdapter({
              name: tool.name,
              description: tool.description,
              input_schema: tool.inputSchema,
            });
        });
    
        const messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [
            {
                role: "user",
                content: "What is the sum of 2 and 3?",
            },
        ];

        console.log("Querying LLM: ", messages[0].content);
        let response = this.openai.chat.completions.create({
            model: "gpt-4o-mini",
            max_tokens: 1000,
            messages,
            tools: tools,
        });    

        let results: any[] = [];
    
        // 1. Go through the LLM response,for each choice, check if it has tool calls 
        (await response).choices.map(async (choice: { message: any; }) => {
          const message = choice.message;
          if (message.tool_calls) {
              console.log("Making tool call")
              await this.callTools(message.tool_calls, results);
          }
        });
    }
    
}

let client = new MyClient();
 const transport = new StdioClientTransport({
            command: "node",
            args: ["./build/index.js"]
        });

client.connectToServer(transport);
```

That's it, now you have a working client.

## -2- Run the client

To test this client out, you're recommended to add a task to your _package.json_ called "client" that runs the client. This way you can run the client with `npm run client`.

```json
{
  "scripts": {
    "client": "tsx node build/client.js"
  }
}
```

Here's a repository you can clone if you want to test this out:

```bash
git clone https://github.com/softchris/tutorial-mcp.git
cd tutorial-mcp
npm run client
```

You should see the following output:

```bash
Asking server for available tools
Querying LLM:  What is the sum of 2 and 3?
Making tool call
Tool result:  { content: [ { type: 'text', text: '5' } ] }
```  