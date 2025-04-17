---
sidebar_position: 1
---

# Consuming external servers

## Example servers

There are many example servers as part of the SDK that you can use to test and experiment with.

Here's an example from the SDK showing you how you can wrap a database in a server:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import sqlite3 from "sqlite3";
import { promisify } from "util";
import { z } from "zod";

const server = new McpServer({
  name: "SQLite Explorer",
  version: "1.0.0"
});

// Helper to create DB connection
const getDb = () => {
  const db = new sqlite3.Database("database.db");
  return {
    all: promisify<string, any[]>(db.all.bind(db)),
    close: promisify(db.close.bind(db))
  };
};

server.resource(
  "schema",
  "schema://main",
  async (uri) => {
    const db = getDb();
    try {
      const tables = await db.all(
        "SELECT sql FROM sqlite_master WHERE type='table'"
      );
      return {
        contents: [{
          uri: uri.href,
          text: tables.map((t: {sql: string}) => t.sql).join("\n")
        }]
      };
    } finally {
      await db.close();
    }
  }
);

server.tool(
  "query",
  { sql: z.string() },
  async ({ sql }) => {
    const db = getDb();
    try {
      const results = await db.all(sql);
      return {
        content: [{
          type: "text",
          text: JSON.stringify(results, null, 2)
        }]
      };
    } catch (err: unknown) {
      const error = err as Error;
      return {
        content: [{
          type: "text",
          text: `Error: ${error.message}`
        }],
        isError: true
      };
    } finally {
      await db.close();
    }
  }
);
```

Read more [here](https://github.com/modelcontextprotocol/typescript-sdk?tab=readme-ov-file#sqlite-explorer)

## External servers

There's many MCP servers built already reading for you to just add them and the way to add them is by adding entries in your `mcp.json` file. Here's some examples of servers you can add:

```json
"filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    }
```

This MCP server allows you to read and write files on your filesystem.

:::important
Be aware that this is operating on your file system. So only grant access to specific folders e.g C:/temp or /tmp. Do not give access to your home directory or any other folder that contains sensitive information.
:::

Another example is GitHub, here you add the following entry:

```json
"github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
}
```

For each server you add, some servers may have requirements on how to add them. For example, the GitHub server requires you to add a personal access token and you need Docker installed and running. Learn more here about [GitHub MCP Sever](https://github.com/github/github-mcp-server?tab=readme-ov-file#prerequisites)