# Azure DevOps MCP Server

Model Context Protocol (MCP) server for Azure DevOps integration with GitHub Copilot in VS Code. Query work items, manage tasks, and interact with Azure DevOps directly through natural language in Copilot Chat.

## Features

### 🎯 Work Item Management
- Get your assigned work items
- Query work items using WIQL
- View detailed work item information
- Create and update work items
- Add and view comments

### 📊 Project & Team Operations
- List all projects in your organization
- Get project details
- List teams within projects

### 💬 Natural Language Interface
Use plain English in Copilot Chat:
- "Show me all my active bugs"
- "Get details for work item #12345"
- "Create a new task titled 'Update documentation'"
- "List all teams in MyProject"

## Quick Start

### Prerequisites
- Python 3.7 or higher
- VS Code with GitHub Copilot installed
- Azure DevOps Personal Access Token (PAT)
- Access to your Azure DevOps organization

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd TFS
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Get your PAT token**
   
   **For Azure DevOps Services:**
   - Visit: `https://dev.azure.com/YourOrganization/_usersSettings/tokens`
   
   **For TFS/Azure DevOps Server:**
   - Visit: `https://your-tfs-server/tfs/YourCollection/_usersSettings/tokens`
   
   - Create a new token with "Work Items (Read & Write)" scope
   - Copy the token to `.env` file

5. **Configure VS Code**
   
   Add to `~/.config/Code/User/mcp.json` (Linux) or equivalent on your OS:
   ```json
   {
     "servers": {
       "azure-devops": {
         "command": "python3",
         "args": ["/full/path/to/azure_devops_mcp_server.py"]
       }
     }
   }
   ```
   
   Or if using a virtual environment:
   ```json
   {
     "servers": {
       "azure-devops": {
         "command": "/path/to/venv/bin/python3",
         "args": ["/full/path/to/azure_devops_mcp_server.py"]
       }
     }
   }
   ```

6. **Reload VS Code**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type: "Developer: Reload Window"

7. **Test it!**
   - Open Copilot Chat (`Ctrl+Shift+I`)
   - Type: "Show me my Azure DevOps work items"

## Available Tools

| Tool | Description |
|------|-------------|
| `get_my_work_items` | Get work items assigned to you |
| `get_work_item` | Get detailed information about a work item |
| `query_work_items` | Query work items using WIQL |
| `create_work_item` | Create a new work item |
| `update_work_item` | Update an existing work item |
| `add_work_item_comment` | Add a comment to a work item |
| `get_work_item_comments` | Get all comments for a work item |
| `list_projects` | List all projects |
| `get_project` | Get project details |
| `list_teams` | List teams in a project |

## Usage Examples

### Get Your Work Items
```
Show me all my active work items
```

### Query Specific Work Items
```
Find all high priority bugs assigned to me
```

### Get Work Item Details
```
Get details for work item #12345
```

### Create a Work Item
```
Create a new bug titled "Login page error" with description "Users can't login after password reset"
```

### Update a Work Item
```
Update work item #12345: change state to Resolved
```

### WIQL Queries
You can use custom WIQL queries:
```
Query Azure DevOps: SELECT * FROM WorkItems WHERE [State] = 'Active' AND [Priority] = 1
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `AZURE_DEVOPS_PAT` | Yes | Personal Access Token |
| `AZURE_DEVOPS_ORG_URL` | Yes | Organization URL |
| `AZURE_DEVOPS_USERNAME` | Optional | Your username |
| `AZURE_DEVOPS_PROJECT` | Optional | Default project name |

### VS Code MCP Configuration Locations

- **Linux:** `~/.config/Code/User/mcp.json`
- **macOS:** `~/Library/Application Support/Code/User/mcp.json`
- **Windows:** `%APPDATA%\Code\User\mcp.json`

## Testing

Test the connection:
```bash
python3 test_connection.py
```

Test individual tools:
```bash
python3 test_mcp_tools.py
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'mcp'"
```bash
pip install -r requirements.txt
```

### "Connection failed" errors
- Verify your PAT token is valid and not expired
- Check you have network access to the TFS server
- Ensure PAT has correct permissions (Work Items: Read & Write)

### MCP server not appearing in VS Code
1. Check the Output panel (View → Output)
2. Select "MCP Servers" from dropdown
3. Look for error messages
4. Verify the file paths in `mcp.json` are absolute and correct
5. Try reloading VS Code

### Permission errors
Ensure your PAT has these scopes:
- Work Items (Read, Write)
- Project and Team (Read)

## Security

⚠️ **Important Security Notes:**
- Never commit `.env` file to version control
- Keep your PAT token secure and private
- Rotate PAT tokens regularly
- Use minimum required permissions for PAT
- Don't share your `.env` file with others

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [Discussions](../../discussions) tab
- Review [Troubleshooting](#troubleshooting) section

## Resources

- [Azure DevOps Python API](https://github.com/microsoft/azure-devops-python-api)
- [Azure DevOps REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [WIQL Syntax](https://learn.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax)

---

**Built with ❤️ for Azure DevOps Teams**
