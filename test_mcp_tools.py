#!/usr/bin/env python3
"""
Test script for Azure DevOps MCP Server
This script tests individual tool functions to verify they work correctly.
"""

import asyncio
import sys
from azure_devops_mcp_server import (
    list_projects,
    get_project,
    list_teams,
    get_my_work_items,
    logger
)

async def test_tools():
    """Test each tool function"""
    print("=" * 60)
    print("Testing Azure DevOps MCP Server Tools")
    print("=" * 60)
    
    # Test 1: List Projects
    print("\n1. Testing list_projects...")
    try:
        result = await list_projects(top=5)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("✓ list_projects works!")
    except Exception as e:
        print(f"✗ list_projects failed: {e}")
    
    # Test 2: Get Project
    print("\n2. Testing get_project...")
    try:
        # TODO: Replace 'YourProjectName' with an actual project from your organization
        result = await get_project(project='Consumer Solutions')
        print(result[:500] + "..." if len(result) > 500 else result)
        print("✓ get_project works!")
    except Exception as e:
        print(f"✗ get_project failed: {e}")
    
    # Test 3: List Teams
    print("\n3. Testing list_teams...")
    try:
        # TODO: Replace 'YourProjectName' with an actual project from your organization
        result = await list_teams(project='Consumer Solutions')
        print(result[:500] + "..." if len(result) > 500 else result)
        print("✓ list_teams works!")
    except Exception as e:
        print(f"✗ list_teams failed: {e}")
    
    # Test 4: Get My Work Items
    print("\n4. Testing get_my_work_items...")
    try:
        result = await get_my_work_items(state='Active')
        print(result[:500] + "..." if len(result) > 500 else result)
        print("✓ get_my_work_items works!")
    except Exception as e:
        print(f"✗ get_my_work_items failed: {e}")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(test_tools())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nTest failed with error: {e}")
        sys.exit(1)
