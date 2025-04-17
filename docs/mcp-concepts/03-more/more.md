---
sidebar_position: 2
---

# There's more than tools

On this workshop, we've covered tools, but there are other concepts that are important to understand. In this section, we'll cover some of them.

Additionally to tools, there's also 

- **Resources**, which are any type of data that can be used by the server. For example, text files, images or even a database schema.
- **Prompts**, these are templates that can be used to generate a response. As a client, you would then pass specific data to the server and the server would generate a response based on the template.

## Resources

All of the following are resources:

    - File contents
    - Database records
    - API responses
    - Live system data
    - Screenshots and images
    - Log files

Resources are accessed using a URI with the following schema:

```text
[protocol]://[host]/[path]
```

For example:

```text
file://localhost/path/to/file.txt
postgres://database/customers/schema
```

Here's how you could implement a resource in your server:

```typescript

// Static resource
server.resource(
  "file",
  "file://{path}",
  async (uri, { path }) => {

    // open file based on `path` and return contents    

    return {
      contents: [{
        uri: uri.href,
        text: "File content here"
      }]
    };
});
```

On the client side, you would then add code like so to read the resource:

```typescript
// Read a resource
const resource = await client.readResource({
  uri: "file:///example.txt"
});
```

## Prompts

Prompts, as we stated earlier, are templates that can be used to generate a response. It's convenient to store prompts that you know will product a good response.

Here's an example of a prompt:

```typescript
server.prompt(
  "product-prompt", 
  "A product query prompt that comes up with a slogan", 
  {
    name: z.string(),
    description: z.string()
  }, 
  async({ name, description }) => {
    console.log("Received request to generate a product prompt");
    return {
      messages: [{
        role: "user",
        content: {
          type: "text",
          text: `Please come up with a slogan for a product called ${name}. The product is described as: ${description}.`,
        }
      }]
    };
  } 
)
```

Above, we created a prompt that takes a name and description and generates a slogan for the product. The prompt is then used by the server to generate a response. 

This prompt can now be used by the client to generate a response when the client calls an LLM, like so:

```typescript
// 1. get the prompt from the server

const response = client.callPrompt({
  name: "product-prompt",
  arguments: {
    name: "My Product",
    description: "A product that does something"
  }
});

// 2. call the LLM with the generated response

response.then((result) => {
  console.log("Generated response: ", result);

  llm.chat.completion({
    messages: result.messages,
    model: "gpt-3.5-turbo",
    temperature: 0.7,
  }).then((response) => {
    console.log("LLM response: ", response);
  });
});
```

Putting prompts on the server like this offloads the responsibility of generating the prompt to the server, which means your client code can be simpler and cleaner. It also means that you can change the prompt on the server without having to change the client code.

Imagine now how someone in the marketing department of an e-commerce using this prompt for new products. They could just call the server with the name and description of the product and get a slogan back. This is a great example of how you can use MCP to create a more efficient workflow.