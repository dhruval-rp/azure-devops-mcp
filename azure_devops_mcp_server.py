#!/usr/bin/env python3
"""
Azure DevOps MCP Server

This MCP server provides tools to interact with Azure DevOps work items,
projects, and teams using the Azure DevOps Python API.

Author: Generated for Azure DevOps Integration
Date: April 16, 2026
"""

import os
import sys
import logging
from typing import Any, Optional
from dotenv import load_dotenv

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking import WorkItemTrackingClient
from azure.devops.v7_1.core import CoreClient


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger('azure-devops-mcp')

# Load environment variables
load_dotenv()

# Azure DevOps configuration
AZURE_DEVOPS_PAT = os.getenv('AZURE_DEVOPS_PAT')
AZURE_DEVOPS_ORG_URL = os.getenv('AZURE_DEVOPS_ORG_URL')
AZURE_DEVOPS_USERNAME = os.getenv('AZURE_DEVOPS_USERNAME', '')
AZURE_DEVOPS_PROJECT = os.getenv('AZURE_DEVOPS_PROJECT', '')

# Validate configuration
if not AZURE_DEVOPS_PAT:
    logger.error("AZURE_DEVOPS_PAT not found in environment variables")
    raise ValueError("AZURE_DEVOPS_PAT must be set in .env file")

if not AZURE_DEVOPS_ORG_URL:
    logger.error("AZURE_DEVOPS_ORG_URL not found in environment variables")
    raise ValueError("AZURE_DEVOPS_ORG_URL must be set in .env file")


class AzureDevOpsConnection:
    """Manages Azure DevOps connection and clients"""
    
    def __init__(self):
        self.credentials = BasicAuthentication(AZURE_DEVOPS_USERNAME, AZURE_DEVOPS_PAT)
        self.connection = Connection(base_url=AZURE_DEVOPS_ORG_URL, creds=self.credentials)
        self.wit_client: Optional[WorkItemTrackingClient] = None
        self.core_client: Optional[CoreClient] = None
        logger.info(f"Connected to Azure DevOps: {AZURE_DEVOPS_ORG_URL}")
    
    def get_wit_client(self) -> WorkItemTrackingClient:
        """Get Work Item Tracking client"""
        if not self.wit_client:
            self.wit_client = self.connection.clients.get_work_item_tracking_client()
        return self.wit_client
    
    def get_core_client(self) -> CoreClient:
        """Get Core client for projects and teams"""
        if not self.core_client:
            self.core_client = self.connection.clients.get_core_client()
        return self.core_client


# Initialize Azure DevOps connection
try:
    ado_connection = AzureDevOpsConnection()
    logger.info("Azure DevOps connection initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Azure DevOps connection: {e}")
    raise


# Initialize MCP server
app = Server("azure-devops-mcp")
logger.info("MCP Server initialized")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available Azure DevOps tools"""
    return [
        Tool(
            name="get_my_work_items",
            description="Get work items assigned to you. Returns active work items by default.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": f"Project name (default: {AZURE_DEVOPS_PROJECT})"
                    },
                    "state": {
                        "type": "string",
                        "description": "Filter by state (e.g., 'Active', 'Closed', 'Resolved'). Leave empty for all states.",
                        "default": "Active"
                    },
                    "type": {
                        "type": "string",
                        "description": "Filter by work item type (e.g., 'Bug', 'Task', 'User Story')"
                    }
                }
            }
        ),
        Tool(
            name="get_work_item",
            description="Get detailed information about a specific work item by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "number",
                        "description": "Work item ID"
                    },
                    "expand": {
                        "type": "string",
                        "description": "Expand options: 'all', 'relations', 'fields', 'links'",
                        "default": "all"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="query_work_items",
            description="Query work items using WIQL (Work Item Query Language)",
            inputSchema={
                "type": "object",
                "properties": {
                    "wiql": {
                        "type": "string",
                        "description": "WIQL query string (e.g., 'SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.State] = \"Active\"')"
                    },
                    "project": {
                        "type": "string",
                        "description": f"Project name (default: {AZURE_DEVOPS_PROJECT})"
                    }
                },
                "required": ["wiql"]
            }
        ),
        Tool(
            name="create_work_item",
            description="Create a new work item",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": f"Project name (default: {AZURE_DEVOPS_PROJECT})"
                    },
                    "work_item_type": {
                        "type": "string",
                        "description": "Type of work item (e.g., 'Bug', 'Task', 'User Story', 'Feature')"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title of the work item"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description/Details of the work item"
                    },
                    "assigned_to": {
                        "type": "string",
                        "description": "Email or name of the person to assign to"
                    },
                    "priority": {
                        "type": "number",
                        "description": "Priority (1-4, where 1 is highest)"
                    },
                    "tags": {
                        "type": "string",
                        "description": "Comma-separated tags"
                    }
                },
                "required": ["work_item_type", "title"]
            }
        ),
        Tool(
            name="update_work_item",
            description="Update an existing work item",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "number",
                        "description": "Work item ID to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    },
                    "state": {
                        "type": "string",
                        "description": "New state (e.g., 'Active', 'Resolved', 'Closed')"
                    },
                    "assigned_to": {
                        "type": "string",
                        "description": "New assignee (email or name)"
                    },
                    "priority": {
                        "type": "number",
                        "description": "New priority (1-4)"
                    },
                    "tags": {
                        "type": "string",
                        "description": "New tags (comma-separated)"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="add_work_item_comment",
            description="Add a comment to a work item",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "number",
                        "description": "Work item ID"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Comment text to add"
                    }
                },
                "required": ["id", "comment"]
            }
        ),
        Tool(
            name="get_work_item_comments",
            description="Get all comments for a work item",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "number",
                        "description": "Work item ID"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="list_projects",
            description="List all projects in the organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "top": {
                        "type": "number",
                        "description": "Maximum number of projects to return (default: 100)"
                    }
                }
            }
        ),
        Tool(
            name="get_project",
            description="Get details of a specific project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project name or ID"
                    }
                },
                "required": ["project"]
            }
        ),
        Tool(
            name="list_teams",
            description="List all teams in a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": f"Project name (default: {AZURE_DEVOPS_PROJECT})"
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    try:
        logger.info(f"Tool called: {name} with arguments: {arguments}")
        
        # Route to appropriate handler
        if name == "get_my_work_items":
            result = await handle_get_my_work_items(arguments)
        elif name == "get_work_item":
            result = await handle_get_work_item(arguments)
        elif name == "query_work_items":
            result = await handle_query_work_items(arguments)
        elif name == "create_work_item":
            result = await handle_create_work_item(arguments)
        elif name == "update_work_item":
            result = await handle_update_work_item(arguments)
        elif name == "add_work_item_comment":
            result = await handle_add_work_item_comment(arguments)
        elif name == "get_work_item_comments":
            result = await handle_get_work_item_comments(arguments)
        elif name == "list_projects":
            result = await handle_list_projects(arguments)
        elif name == "get_project":
            result = await handle_get_project(arguments)
        elif name == "list_teams":
            result = await handle_list_teams(arguments)
        else:
            result = f"Unknown tool: {name}"
        
        return [TextContent(type="text", text=str(result))]
    
    except Exception as e:
        logger.error(f"Error in {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


# Tool handler functions
async def handle_get_my_work_items(args: dict) -> str:
    """Get work items assigned to current user"""
    try:
        wit_client = ado_connection.get_wit_client()
        project = args.get('project', AZURE_DEVOPS_PROJECT)
        state = args.get('state', 'Active')
        work_item_type = args.get('type', '')
        
        # Build WIQL query
        wiql_parts = [
            "SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType], [System.AssignedTo]",
            "FROM WorkItems",
            "WHERE [System.AssignedTo] = @Me"
        ]
        
        if project:
            wiql_parts.append(f"AND [System.TeamProject] = '{project}'")
        
        if state:
            wiql_parts.append(f"AND [System.State] = '{state}'")
        
        if work_item_type:
            wiql_parts.append(f"AND [System.WorkItemType] = '{work_item_type}'")
        
        wiql_parts.append("ORDER BY [System.ChangedDate] DESC")
        wiql_query = " ".join(wiql_parts)
        
        # Execute query
        from azure.devops.v7_1.work_item_tracking.models import Wiql
        wiql = Wiql(query=wiql_query)
        result = wit_client.query_by_wiql(wiql)
        
        if not result.work_items:
            return "No work items found matching the criteria."
        
        # Get work item IDs
        ids = [item.id for item in result.work_items]
        
        # Fetch full work items
        work_items = wit_client.get_work_items(ids=ids, expand='All')
        
        # Format output
        output = [f"Found {len(work_items)} work item(s):\n"]
        for wi in work_items:
            fields = wi.fields
            output.append(f"ID: {wi.id}")
            output.append(f"  Title: {fields.get('System.Title', 'N/A')}")
            output.append(f"  Type: {fields.get('System.WorkItemType', 'N/A')}")
            output.append(f"  State: {fields.get('System.State', 'N/A')}")
            output.append(f"  Assigned To: {fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned')}")
            output.append(f"  Priority: {fields.get('Microsoft.VSTS.Common.Priority', 'N/A')}")
            output.append(f"  Changed Date: {fields.get('System.ChangedDate', 'N/A')}")
            output.append("")
        
        return "\n".join(output)
    
    except Exception as e:
        logger.error(f"Error in handle_get_my_work_items: {e}", exc_info=True)
        return f"Error retrieving work items: {str(e)}"


async def handle_get_work_item(args: dict) -> str:
    """Get specific work item by ID"""
    try:
        wit_client = ado_connection.get_wit_client()
        work_item_id = int(args['id'])
        expand = args.get('expand', 'all')
        
        # Map expand option to API constant
        from azure.devops.v7_1.work_item_tracking.models import WorkItemExpand
        expand_option = WorkItemExpand.all
        if expand.lower() == 'relations':
            expand_option = WorkItemExpand.relations
        elif expand.lower() == 'fields':
            expand_option = WorkItemExpand.fields
        elif expand.lower() == 'links':
            expand_option = WorkItemExpand.links
        
        # Get work item
        work_item = wit_client.get_work_item(id=work_item_id, expand=expand_option)
        
        if not work_item:
            return f"Work item {work_item_id} not found."
        
        # Format output
        fields = work_item.fields
        output = [f"Work Item #{work_item.id}\n"]
        output.append(f"Title: {fields.get('System.Title', 'N/A')}")
        output.append(f"Type: {fields.get('System.WorkItemType', 'N/A')}")
        output.append(f"State: {fields.get('System.State', 'N/A')}")
        output.append(f"Assigned To: {fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned')}")
        output.append(f"Created By: {fields.get('System.CreatedBy', {}).get('displayName', 'N/A')}")
        output.append(f"Created Date: {fields.get('System.CreatedDate', 'N/A')}")
        output.append(f"Changed Date: {fields.get('System.ChangedDate', 'N/A')}")
        output.append(f"Priority: {fields.get('Microsoft.VSTS.Common.Priority', 'N/A')}")
        output.append(f"Severity: {fields.get('Microsoft.VSTS.Common.Severity', 'N/A')}")
        output.append(f"Area Path: {fields.get('System.AreaPath', 'N/A')}")
        output.append(f"Iteration Path: {fields.get('System.IterationPath', 'N/A')}")
        output.append(f"Tags: {fields.get('System.Tags', 'None')}")
        
        # Description
        description = fields.get('System.Description', '')
        if description:
            # Strip HTML tags for cleaner output
            import re
            description_text = re.sub('<[^<]+?>', '', description)
            output.append(f"\nDescription:\n{description_text[:500]}{'...' if len(description_text) > 500 else ''}")
        
        # Relations
        if work_item.relations:
            output.append(f"\nRelations ({len(work_item.relations)}):")
            for rel in work_item.relations[:10]:  # Show first 10
                rel_type = rel.attributes.get('name', 'Unknown') if rel.attributes else 'Unknown'
                output.append(f"  - {rel_type}: {rel.url}")
        
        output.append(f"\nURL: {work_item.url}")
        
        return "\n".join(output)
    
    except Exception as e:
        logger.error(f"Error in handle_get_work_item: {e}", exc_info=True)
        return f"Error retrieving work item: {str(e)}"


async def handle_query_work_items(args: dict) -> str:
    """Query work items using WIQL"""
    try:
        wit_client = ado_connection.get_wit_client()
        wiql_query = args['wiql']
        project = args.get('project', AZURE_DEVOPS_PROJECT)
        
        # Execute WIQL query
        from azure.devops.v7_1.work_item_tracking.models import Wiql
        wiql = Wiql(query=wiql_query)
        result = wit_client.query_by_wiql(wiql)
        
        if not result.work_items:
            return "Query returned no work items."
        
        # Get work item IDs
        ids = [item.id for item in result.work_items[:100]]  # Limit to 100
        
        # Fetch full work items
        work_items = wit_client.get_work_items(ids=ids, expand='Fields')
        
        # Format output
        output = [f"Query returned {len(result.work_items)} work item(s) (showing first {len(ids)}):\n"]
        for wi in work_items:
            fields = wi.fields
            output.append(f"ID: {wi.id}")
            output.append(f"  Title: {fields.get('System.Title', 'N/A')}")
            output.append(f"  Type: {fields.get('System.WorkItemType', 'N/A')}")
            output.append(f"  State: {fields.get('System.State', 'N/A')}")
            output.append(f"  Assigned To: {fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned')}")
            output.append("")
        
        return "\n".join(output)
    
    except Exception as e:
        logger.error(f"Error in handle_query_work_items: {e}", exc_info=True)
        return f"Error executing query: {str(e)}"


async def handle_create_work_item(args: dict) -> str:
    """Create a new work item"""
    try:
        wit_client = ado_connection.get_wit_client()
        project = args.get('project', AZURE_DEVOPS_PROJECT)
        work_item_type = args['work_item_type']
        title = args['title']
        
        # Build document for work item creation
        from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation
        document = []
        
        # Add title (required)
        document.append(JsonPatchOperation(
            op='add',
            path='/fields/System.Title',
            value=title
        ))
        
        # Add description if provided
        if 'description' in args and args['description']:
            document.append(JsonPatchOperation(
                op='add',
                path='/fields/System.Description',
                value=args['description']
            ))
        
        # Add assigned to if provided
        if 'assigned_to' in args and args['assigned_to']:
            document.append(JsonPatchOperation(
                op='add',
                path='/fields/System.AssignedTo',
                value=args['assigned_to']
            ))
        
        # Add priority if provided
        if 'priority' in args and args['priority']:
            document.append(JsonPatchOperation(
                op='add',
                path='/fields/Microsoft.VSTS.Common.Priority',
                value=args['priority']
            ))
        
        # Add tags if provided
        if 'tags' in args and args['tags']:
            document.append(JsonPatchOperation(
                op='add',
                path='/fields/System.Tags',
                value=args['tags']
            ))
        
        # Create work item
        created_work_item = wit_client.create_work_item(
            document=document,
            project=project,
            type=work_item_type
        )
        
        # Format response
        fields = created_work_item.fields
        output = [f"Work item created successfully!\n"]
        output.append(f"ID: {created_work_item.id}")
        output.append(f"Title: {fields.get('System.Title', 'N/A')}")
        output.append(f"Type: {fields.get('System.WorkItemType', 'N/A')}")
        output.append(f"State: {fields.get('System.State', 'N/A')}")
        output.append(f"Assigned To: {fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned')}")
        output.append(f"\nURL: {created_work_item._links.additional_properties.get('html', {}).get('href', 'N/A')}")
        
        return "\n".join(output)
    
    except Exception as e:
        logger.error(f"Error in handle_create_work_item: {e}", exc_info=True)
        return f"Error creating work item: {str(e)}"


async def handle_update_work_item(args: dict) -> str:
    """Update an existing work item"""
    try:
        wit_client = ado_connection.get_wit_client()
        work_item_id = int(args['id'])
        
        # Build document for work item update
        from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation
        document = []
        
        # Update title if provided
        if 'title' in args and args['title']:
            document.append(JsonPatchOperation(
                op='replace',
                path='/fields/System.Title',
                value=args['title']
            ))
        
        # Update description if provided
        if 'description' in args and args['description']:
            document.append(JsonPatchOperation(
                op='replace',
                path='/fields/System.Description',
                value=args['description']
            ))
        
        # Update state if provided
        if 'state' in args and args['state']:
            document.append(JsonPatchOperation(
                op='replace',
                path='/fields/System.State',
                value=args['state']
            ))
        
        # Update assigned to if provided
        if 'assigned_to' in args and args['assigned_to']:
            document.append(JsonPatchOperation(
                op='replace',
                path='/fields/System.AssignedTo',
                value=args['assigned_to']
            ))
        
        # Update priority if provided
        if 'priority' in args and args['priority']:
            document.append(JsonPatchOperation(
                op='replace',
                path='/fields/Microsoft.VSTS.Common.Priority',
                value=args['priority']
            ))
        
        # Update tags if provided
        if 'tags' in args and args['tags']:
            document.append(JsonPatchOperation(
                op='replace',
                path='/fields/System.Tags',
                value=args['tags']
            ))
        
        if not document:
            return "No fields to update were provided."
        
        # Update work item
        updated_work_item = wit_client.update_work_item(
            document=document,
            id=work_item_id
        )
        
        # Format response
        fields = updated_work_item.fields
        output = [f"Work item #{work_item_id} updated successfully!\n"]
        output.append(f"Title: {fields.get('System.Title', 'N/A')}")
        output.append(f"Type: {fields.get('System.WorkItemType', 'N/A')}")
        output.append(f"State: {fields.get('System.State', 'N/A')}")
        output.append(f"Assigned To: {fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned')}")
        output.append(f"Priority: {fields.get('Microsoft.VSTS.Common.Priority', 'N/A')}")
        
        return "\n".join(output)
    
    except Exception as e:
        logger.error(f"Error in handle_update_work_item: {e}", exc_info=True)
        return f"Error updating work item: {str(e)}"


async def handle_add_work_item_comment(args: dict) -> str:
    """Add comment to work item"""
    try:
        wit_client = ado_connection.get_wit_client()
        work_item_id = int(args['id'])
        comment_text = args['comment']
        
        # Add comment using work item update
        from azure.devops.v7_1.work_item_tracking.models import CommentCreate
        comment_create = CommentCreate(text=comment_text)
        
        # Add comment to work item
        comment = wit_client.add_comment(
            project=AZURE_DEVOPS_PROJECT,
            work_item_id=work_item_id,
            request=comment_create
        )
        
        return f"Comment added successfully to work item #{work_item_id}\nComment ID: {comment.id}\nText: {comment.text}"
    
    except Exception as e:
        logger.error(f"Error in handle_add_work_item_comment: {e}", exc_info=True)
        return f"Error adding comment: {str(e)}"


async def handle_get_work_item_comments(args: dict) -> str:
    """Get work item comments"""
    try:
        wit_client = ado_connection.get_wit_client()
        work_item_id = int(args['id'])
        
        # Get comments
        comments = wit_client.get_comments(
            project=AZURE_DEVOPS_PROJECT,
            work_item_id=work_item_id
        )
        
        if not comments.comments:
            return f"No comments found for work item #{work_item_id}"
        
        # Format output
        output = [f"Comments for work item #{work_item_id} ({comments.total_count} total):\n"]
        for comment in comments.comments:
            created_by = comment.created_by.display_name if comment.created_by else 'Unknown'
            created_date = comment.created_date if comment.created_date else 'N/A'
            output.append(f"Comment ID: {comment.id}")
            output.append(f"  By: {created_by}")
            output.append(f"  Date: {created_date}")
            output.append(f"  Text: {comment.text}")
            output.append("")
        
        return "\n".join(output)
    
    except Exception as e:
        logger.error(f"Error in handle_get_work_item_comments: {e}", exc_info=True)
        return f"Error retrieving comments: {str(e)}"


async def handle_list_projects(args: dict) -> str:
    """List all projects"""
    try:
        core_client = ado_connection.get_core_client()
        top = args.get('top', 100)
        
        # Get projects
        projects = core_client.get_projects(top=top)
        
        if not projects:
            return "No projects found."
        
        # Format output
        output = [f"Found {len(projects)} project(s):\n"]
        for project in projects:
            output.append(f"Name: {project.name}")
            output.append(f"  ID: {project.id}")
            output.append(f"  Description: {project.description or 'N/A'}")
            output.append(f"  State: {project.state}")
            output.append(f"  Visibility: {project.visibility}")
            output.append(f"  Last Update: {project.last_update_time}")
            output.append("")
        
        return "\n".join(output)
    
    except Exception as e:
        logger.error(f"Error in handle_list_projects: {e}", exc_info=True)
        return f"Error listing projects: {str(e)}"


async def handle_get_project(args: dict) -> str:
    """Get project details"""
    try:
        core_client = ado_connection.get_core_client()
        project_name = args['project']
        
        # Get project
        project = core_client.get_project(project_name)
        
        if not project:
            return f"Project '{project_name}' not found."
        
        # Format output
        output = [f"Project: {project.name}\n"]
        output.append(f"ID: {project.id}")
        output.append(f"Description: {project.description or 'N/A'}")
        output.append(f"State: {project.state}")
        output.append(f"Visibility: {project.visibility}")
        output.append(f"Revision: {project.revision}")
        output.append(f"Last Update: {project.last_update_time}")
        output.append(f"URL: {project.url}")
        
        # Get default team
        if project.default_team:
            output.append(f"\nDefault Team: {project.default_team.name}")
            output.append(f"  Team ID: {project.default_team.id}")
        
        # Get capabilities
        if project.capabilities:
            output.append("\nCapabilities:")
            for key, value in project.capabilities.items():
                output.append(f"  {key}: {value}")
        
        return "\n".join(output)
    
    except Exception as e:
        logger.error(f"Error in handle_get_project: {e}", exc_info=True)
        return f"Error getting project: {str(e)}"


async def handle_list_teams(args: dict) -> str:
    """List teams in project"""
    try:
        core_client = ado_connection.get_core_client()
        project = args.get('project', AZURE_DEVOPS_PROJECT)
        
        # Get teams
        teams = core_client.get_teams(project)
        
        if not teams:
            return f"No teams found in project '{project}'."
        
        # Format output
        output = [f"Teams in project '{project}' ({len(teams)} total):\n"]
        for team in teams:
            output.append(f"Name: {team.name}")
            output.append(f"  ID: {team.id}")
            output.append(f"  Description: {team.description or 'N/A'}")
            output.append(f"  URL: {team.url}")
            output.append("")
        
        return "\n".join(output)
    
    except Exception as e:
        logger.error(f"Error in handle_list_teams: {e}", exc_info=True)
        return f"Error listing teams: {str(e)}"


async def main():
    """Run the MCP server"""
    logger.info("Starting Azure DevOps MCP Server...")
    
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
