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
    import { Transport } from "@modelcontextprotocol/sdk/shared/transport";
    import OpenAI from "openai";
    import { z } from "zod"; // Import zod for schema validation

    this.openai = new OpenAI({
        baseURL: "https://models.inference.ai.azure.com", // might need to change to this url in the future: https://models.github.ai/inference
        apiKey: process.env.GITHUB_TOKEN,
    });
    ```

    Now you have all the imports you need including OpenAI and you've instantiated an openai client. Next, let's add code to create the client and connect to the server.

1. Add the following code to create a client and connect to the server:

    ```typescript
    async function main() {
        const transport = new StdioClientTransport({
            command: "node",
            args: ["../build/index.js"]
        });
    
        const client = new Client(
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
    
        await client.connect(transport);
    }

    main().catch((error) => {
        console.error("Fatal error: ", error);
        process.exit(1);
    });
    ```

    Now you have a client, let's add the LLM part next.

1. Add the following code to help transform a server response to a tool description:

    ```typescript
    function openAiToolAdapter(tool: {
      name: string;
      description?: string;
      input_schema: any;
        }) {
        // Create a zod schema based on the input_schema
        const schema = z.object(tool.input_schema);
    
        return {
        type: "function",
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

    This function takes a tool description from the server and transforms it into a format that OpenAI can understand. Our next step is to make a call to the server and get the tools. 

1. Add the following code to `main()` to list the tools from the server:

    ```typescript
    const tools = await this.mcp.listTools();
      this.tools = toolsResult.tools.map((tool) => {
        return openAiToolAdapter({
          name: tool.name,
          description: tool.description,
          input_schema: tool.inputSchema,
        });
    });
    ```

    This sets us up nicely to call the LLM. Next, let's add the code to call the LLM and get a response and based on that response, determine if we need to call the server's tools.

1. Add the following to make the call to the LLM:

    ```typescript
    let response = await this.openai.chat.completions.create({
      model: "gpt-4o-mini",
      max_tokens: 1000,
      messages,
      tools: tools,
    });

    ```

    Once we've got the response, we need to check if the LLM has called any of the tools. If it has, we need to call the server's tools and get the result.

1. Add this code to inspect the LLM response:

    ```typescript
    results = any[];

    async callTools(
        tool_calls: OpenAI.Chat.Completions.ChatCompletionMessageToolCall[],
        toolResults: any[],
        finalText: string[]
      ) {
        for (const tool_call of tool_calls) {
          const toolName = tool_call.function.name;
          const args = tool_call.function.arguments;
    
          console.log(`Calling tool ${toolName} with args ${JSON.stringify(args)}`);
    

          // 2. Call the server's tool 
          const toolResult = await this.mcp.callTool({
            name: toolName,
            arguments: JSON.parse(args),
          });
    
          console.log("Tool result: ", toolResult);
    
          // 3. Do something with the result
          // TODO  
    
         }
    }

    // 1. Go through the LLM response,for each choice, check if it has tool calls 
    response.choices.map(async (choice) => {
      const message = choice.message;
      if (message.tool_calls) {
        toolResults.push(
          await callTools(message.tool_calls, results, finalText)
        );
      } else {
        console.log("Message response from LLM: ", message);
        finalText.push(message.content || "xx");
      }
    });
    ```

    Now we have a client with the capability to call the server's tools based on the LLM response. Let's test this code out next.

1.
        
    