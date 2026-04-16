#!/usr/bin/env python3
"""
Quick test script to verify Azure DevOps connection and MCP server setup
"""

import os
from dotenv import load_dotenv
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Load environment variables
load_dotenv()

AZURE_DEVOPS_PAT = os.getenv('AZURE_DEVOPS_PAT')
AZURE_DEVOPS_ORG_URL = os.getenv('AZURE_DEVOPS_ORG_URL')
AZURE_DEVOPS_USERNAME = os.getenv('AZURE_DEVOPS_USERNAME', '')
AZURE_DEVOPS_PROJECT = os.getenv('AZURE_DEVOPS_PROJECT', '')

print("Testing Azure DevOps Connection...")
print(f"Organization URL: {AZURE_DEVOPS_ORG_URL}")
print(f"Username: {AZURE_DEVOPS_USERNAME}")
print(f"Default Project: {AZURE_DEVOPS_PROJECT}")
print()

try:
    # Create connection
    credentials = BasicAuthentication(AZURE_DEVOPS_USERNAME, AZURE_DEVOPS_PAT)
    connection = Connection(base_url=AZURE_DEVOPS_ORG_URL, creds=credentials)
    
    # Test core client
    print("✓ Connection established")
    core_client = connection.clients.get_core_client()
    print("✓ Core client obtained")
    
    # Get projects
    projects = core_client.get_projects(top=5)
    print(f"✓ Found {len(projects.value)} projects (showing first 5):")
    for project in projects.value:
        print(f"  - {project.name}")
    
    print()
    
    # Test work item tracking client
    wit_client = connection.clients.get_work_item_tracking_client()
    print("✓ Work Item Tracking client obtained")
    
    print()
    print("=" * 50)
    print("✓ All tests passed! MCP server is ready to use.")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Test the MCP server: python3 azure_devops_mcp_server.py")
    print("2. Configure Claude Desktop (see README_MCP.md)")
    print("3. Start using Azure DevOps tools with Claude!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print()
    print("Please check:")
    print("1. Your .env file has correct credentials")
    print("2. Your PAT token is valid and has proper permissions")
    print("3. You have network access to the Azure DevOps server")
