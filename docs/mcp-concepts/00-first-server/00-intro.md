---
sidebar_position: 1
---

# MCP, what is it and why use it?

> TLDR; If you build AI apps, you know that you can add tools and other resources to your LLM (large language model), to make the LLM more knowledgeable. However if you place those tools and resources on a server, the app and the server capabilities can be used by any client with/without an LLM.

The Model Context Protocol (MCP) is an open standard designed to facilitate the connection between AI models and various data sources and tools. Here are some key points about MCP:

## Purpose 

MCP standardizes how applications provide context to large language models (LLMs). It aims to replace fragmented integrations with a single, universal protocol, making it easier for AI systems to access the data they need12.

## Architecture: MCP follows a client-server architecture:

- **MCP Hosts**: Programs like IDEs or AI tools that want to access data through MCP.
- **MCP Clients**: Protocol clients that maintain 1:1 connections with servers.
- **MCP Servers**: Lightweight programs that expose specific capabilities through MCP.
- **Local Data Sources**: Files, databases, and services on your computer that MCP servers can securely access.
- **Remote Services**: External systems available over the internet (e.g., APIs) that MCP servers can connect to1.
Components:

![MCP Diagram](/img/diagram.png)

*Image credit https://modelcontextprotocol.io/introduction*

- **MCP Specification and SDKs**: Tools and guidelines for developers to implement MCP.
Local MCP Server Support: Available in applications like Claude Desktop.
Open-Source Repository: Pre-built MCP servers for popular systems like Google Drive, Slack, GitHub, etc.2.
Benefits:

## Integration

MCP helps build agents and complex workflows on top of LLMs by providing a standardized way to connect to various data sources.

## Flexibility

It allows switching between different LLM providers and vendors.
Security: Best practices for securing data within your infrastructure.
Use Cases: Early adopters like Block and Apollo have integrated MCP into their systems, and development tools companies like Zed, Replit, Codeium, and Sourcegraph are using MCP to enhance their platforms
