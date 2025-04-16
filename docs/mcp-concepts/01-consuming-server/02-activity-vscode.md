---
sidebar_position: 2
---

# Activity: Consume server with Visual Studio Code

For a server built with stdio you need to do the following at high level:

- Create an mcp.json file in .vscode folder
- Enter absolute path to the server
- Start the server via the JSON file
- Run the tool via GitHub Copilot chat

To do this, follow the steps below:

1. Create a `.vscode` folder in the root directory of your project and add a `mcp.json` file in the `.vscode` folder.
1. Start the server via the JSON file.
1. Run the tool via GitHub Copilot chat. 

## Create a config file

The config file is used to configure the server. It can contain both input, and server configurations.

We need a folder for our configuration file.

1. Create a `.vscode` folder in the root directory of your project and add a `mcp.json` file in the `.vscode` folder.

    ```bash
    mkdir .vscode
    ```

    Next, we need the actual configuration file.

1. Create a `mcp.json` file in the `.vscode` folder with the following content:

    ```json
    {
        "inputs": [],
        "servers": {
           "hello-mcp": {
               "command": "cmd",
               "args": [
                   "/c", "node", "<absolute path>\\build\\index.js"
               ]
           }
        }
    }
    ```

    The path to your server should be the build folder. To find the path, run the following command in the terminal:
    
    ```bash
    pwd
    ```

    This will give you the absolute path to your project. You can then copy the path and paste it in the `mcp.json` file.

## Start the server

To start the server, open the _mcp.json_ file in Visual Studio Code and click on the play button.

![Start server](/img/vscode-start-server.png)

## Run the tool via GitHub Copilot chat

Now that the server have hopefully started up, let's use it.

1. Click tools icon to bring up a list of tools

  ![VS Code available tools](/img/vscode-tool.png)

1. Inspect the tools result list, your server should be listed there.

  ![VS Code inspect tools](/img/vscode-tool-info.png)

## Run the tool

1. To run the tool, type a prompt in the chat like so:

    ```text
    add 22 to 1
    ```

    You should see a result like so indicating that you allow the agent to run the tool:
    
    ![VS Code run tool](/img/vscode-agent.png)

1. Click the down arrow to expand the tool and see the arguments that are passed to the tool.

    ![VS Code run tool](/img/vscode-tool-args.png)

    Here you can see what server the selected tool is running on and the arguments that are passed to the tool.

1. Click on the "Continue" button to run the tool.

    You should see a result like so:

    ![VS Code run tool result](/img/vscode-tool-result.png)

## Summary

Congrats, you've managed to consume a server with Visual Studio Code and run a tool via GitHub Copilot chat!