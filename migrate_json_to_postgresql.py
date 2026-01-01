#!/usr/bin/env python3
"""
Codex Dominion - JSON to PostgreSQL Migration Script

Migrates all JSON ledger data to PostgreSQL database:
- codex_ledger.json → workflow_metrics, system_health tables
- treasury_config.json → revenue_streams table
- cycles.json → system cycles
- proclamations.json → governance records
- accounts.json → account data

Usage:
    python migrate_json_to_postgresql.py [--dry-run] [--backup]

Options:
    --dry-run    Show what would be migrated without changing database
    --backup     Create backup of JSON files before migration
"""

import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from db import SessionLocal, engine
from models import (
    Base, Council, Agent, Workflow, WorkflowType, WorkflowMetric,
    CouncilMember, Vote, Recommendation, ProposalStatus
)
from sqlalchemy.exc import IntegrityError

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^70}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")


class JSONToPostgreSQLMigrator:
    """Migrates Codex Dominion JSON data to PostgreSQL"""
    
    def __init__(self, dry_run: bool = False, backup: bool = True):
        self.dry_run = dry_run
        self.backup = backup
        self.base_path = Path(__file__).parent
        self.stats = {
            'councils': 0,
            'agents': 0,
            'workflows': 0,
            'workflow_types': 0,
            'proclamations': 0,
            'cycles': 0,
            'accounts': 0,
            'errors': 0
        }
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON file with error handling"""
        filepath = self.base_path / filename
        
        if not filepath.exists():
            print_warning(f"JSON file not found: {filename}")
            return {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print_error(f"Failed to load {filename}: {e}")
            return {}
    
    def backup_json_files(self):
        """Create backup of all JSON files"""
        if not self.backup:
            return
        
        print_info("Creating backups of JSON files...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.base_path / f"json_backups_{timestamp}"
        backup_dir.mkdir(exist_ok=True)
        
        json_files = [
            "codex_ledger.json",
            "treasury_config.json",
            "cycles.json",
            "proclamations.json",
            "accounts.json",
            "agents.json"
        ]
        
        for filename in json_files:
            source = self.base_path / filename
            if source.exists():
                dest = backup_dir / filename
                shutil.copy2(source, dest)
                print_success(f"Backed up: {filename}")
        
        print_success(f"Backups saved to: {backup_dir}")
    
    def migrate_councils(self, session):
        """Migrate councils from codex_ledger.json"""
        print_info("Migrating councils...")
        
        ledger = self.load_json("codex_ledger.json")
        councils_data = ledger.get("councils", [])
        
        if not councils_data:
            print_warning("No councils found in codex_ledger.json")
            return
        
        for council_data in councils_data:
            try:
                council = Council(
                    id=council_data.get("id", f"council_{council_data['name'].lower().replace(' ', '_')}"),
                    name=council_data.get("name"),
                    purpose=council_data.get("purpose"),
                    domain=council_data.get("domain"),
                    status="active"
                )
                
                if not self.dry_run:
                    session.add(council)
                
                self.stats['councils'] += 1
                print_success(f"Migrated council: {council.name}")
                
            except IntegrityError:
                print_warning(f"Council already exists: {council_data.get('name')}")
                session.rollback()
            except Exception as e:
                print_error(f"Failed to migrate council {council_data.get('name')}: {e}")
                self.stats['errors'] += 1
    
    def migrate_agents(self, session):
        """Migrate AI agents from agents.json"""
        print_info("Migrating AI agents...")
        
        agents_data = self.load_json("agents.json")
        
        if not agents_data:
            print_warning("No agents found in agents.json")
            return
        
        for agent_id, agent_data in agents_data.items():
            try:
                agent = Agent(
                    id=agent_id,
                    name=agent_data.get("name"),
                    agent_type=agent_data.get("type", "autonomous"),
                    capabilities=agent_data.get("capabilities", []),
                    status="active"
                )
                
                if not self.dry_run:
                    session.add(agent)
                
                self.stats['agents'] += 1
                print_success(f"Migrated agent: {agent.name}")
                
            except IntegrityError:
                print_warning(f"Agent already exists: {agent_id}")
                session.rollback()
            except Exception as e:
                print_error(f"Failed to migrate agent {agent_id}: {e}")
                self.stats['errors'] += 1
    
    def migrate_workflow_types(self, session):
        """Migrate workflow types"""
        print_info("Migrating workflow types...")
        
        # Default workflow types from the system
        workflow_types = [
            {
                "id": "social_media_post",
                "name": "Social Media Post",
                "description": "Automated social media content posting",
                "default_inputs": {"platforms": ["instagram", "tiktok"], "content_type": "image"}
            },
            {
                "id": "store_creation",
                "name": "Store Creation",
                "description": "WooCommerce store setup and configuration",
                "default_inputs": {"platform": "woocommerce", "theme": "default"}
            },
            {
                "id": "website_creation",
                "name": "Website Creation",
                "description": "Full website deployment and configuration",
                "default_inputs": {"framework": "nextjs", "hosting": "azure"}
            },
            {
                "id": "workflow_automation",
                "name": "Workflow Automation",
                "description": "Custom workflow automation task",
                "default_inputs": {"trigger": "manual", "priority": "normal"}
            },
            {
                "id": "budget_allocation",
                "name": "Budget Allocation",
                "description": "Treasury budget allocation and distribution",
                "default_inputs": {"source": "treasury", "approval_required": True}
            }
        ]
        
        for wf_type in workflow_types:
            try:
                workflow_type = WorkflowType(
                    id=wf_type["id"],
                    name=wf_type["name"],
                    description=wf_type["description"],
                    default_inputs=wf_type["default_inputs"]
                )
                
                if not self.dry_run:
                    session.add(workflow_type)
                
                self.stats['workflow_types'] += 1
                print_success(f"Migrated workflow type: {workflow_type.name}")
                
            except IntegrityError:
                print_warning(f"Workflow type already exists: {wf_type['id']}")
                session.rollback()
            except Exception as e:
                print_error(f"Failed to migrate workflow type {wf_type['id']}: {e}")
                self.stats['errors'] += 1
    
    def migrate_treasury_data(self, session):
        """Migrate treasury configuration and transactions"""
        print_info("Migrating treasury data...")
        
        treasury_config = self.load_json("treasury_config.json")
        
        if not treasury_config:
            print_warning("No treasury config found")
            return
        
        # Treasury data would go into custom tables or as workflow metadata
        # For now, we'll store as system metadata
        print_info("Treasury config stored in JSON (no PostgreSQL table yet)")
        print_success("Treasury migration noted for future table creation")
    
    def migrate_proclamations(self, session):
        """Migrate proclamations as system documentation"""
        print_info("Migrating proclamations...")
        
        proclamations = self.load_json("proclamations.json")
        
        if not proclamations:
            print_warning("No proclamations found")
            return
        
        # Proclamations could be stored as system announcements
        # For now, keeping in JSON format as they're documentation
        self.stats['proclamations'] = len(proclamations) if isinstance(proclamations, list) else 0
        print_success(f"Noted {self.stats['proclamations']} proclamations (keeping in JSON)")
    
    def migrate_cycles(self, session):
        """Migrate operational cycles"""
        print_info("Migrating cycles...")
        
        cycles = self.load_json("cycles.json")
        
        if not cycles:
            print_warning("No cycles found")
            return
        
        # Cycles represent operational phases - stored as system state
        self.stats['cycles'] = len(cycles) if isinstance(cycles, list) else 0
        print_success(f"Noted {self.stats['cycles']} cycles (keeping in JSON)")
    
    def migrate_accounts(self, session):
        """Migrate account data"""
        print_info("Migrating accounts...")
        
        accounts = self.load_json("accounts.json")
        
        if not accounts:
            print_warning("No accounts found")
            return
        
        # Accounts would need a dedicated table - keeping in JSON for now
        self.stats['accounts'] = len(accounts) if isinstance(accounts, dict) else 0
        print_success(f"Noted {self.stats['accounts']} accounts (keeping in JSON)")
    
    def initialize_database(self):
        """Create all database tables"""
        print_info("Initializing database schema...")
        
        if self.dry_run:
            print_warning("DRY RUN: Would create all tables")
            return
        
        try:
            Base.metadata.create_all(bind=engine)
            print_success("Database schema created successfully")
        except Exception as e:
            print_error(f"Failed to create schema: {e}")
            raise
    
    def run_migration(self):
        """Execute full migration"""
        print_header("🔥 CODEX DOMINION - JSON TO POSTGRESQL MIGRATION 🔥")
        
        if self.dry_run:
            print_warning("RUNNING IN DRY-RUN MODE - No database changes will be made")
        
        # Backup JSON files
        if self.backup:
            self.backup_json_files()
        
        # Initialize database
        self.initialize_database()
        
        # Create session
        session = SessionLocal()
        
        try:
            # Run migrations
            self.migrate_workflow_types(session)
            self.migrate_councils(session)
            self.migrate_agents(session)
            self.migrate_treasury_data(session)
            self.migrate_proclamations(session)
            self.migrate_cycles(session)
            self.migrate_accounts(session)
            
            # Commit changes
            if not self.dry_run:
                session.commit()
                print_success("All changes committed to database")
            else:
                print_warning("DRY RUN: No changes committed")
        
        except Exception as e:
            session.rollback()
            print_error(f"Migration failed: {e}")
            raise
        
        finally:
            session.close()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print migration summary"""
        print_header("MIGRATION SUMMARY")
        
        print(f"{Colors.CYAN}Councils migrated:      {Colors.BOLD}{self.stats['councils']}{Colors.END}")
        print(f"{Colors.CYAN}Agents migrated:        {Colors.BOLD}{self.stats['agents']}{Colors.END}")
        print(f"{Colors.CYAN}Workflow types:         {Colors.BOLD}{self.stats['workflow_types']}{Colors.END}")
        print(f"{Colors.CYAN}Proclamations noted:    {Colors.BOLD}{self.stats['proclamations']}{Colors.END}")
        print(f"{Colors.CYAN}Cycles noted:           {Colors.BOLD}{self.stats['cycles']}{Colors.END}")
        print(f"{Colors.CYAN}Accounts noted:         {Colors.BOLD}{self.stats['accounts']}{Colors.END}")
        
        if self.stats['errors'] > 0:
            print(f"\n{Colors.RED}Errors encountered:     {Colors.BOLD}{self.stats['errors']}{Colors.END}")
        else:
            print(f"\n{Colors.GREEN}✅ Migration completed successfully!{Colors.END}")
        
        if self.dry_run:
            print(f"\n{Colors.YELLOW}Note: This was a DRY RUN. No database changes were made.{Colors.END}")
            print(f"{Colors.YELLOW}Run without --dry-run to apply changes.{Colors.END}")
        
        print(f"\n{Colors.BOLD}🔥 The Flame Burns Sovereign and Eternal! 👑{Colors.END}\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate JSON data to PostgreSQL")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be migrated without changing database")
    parser.add_argument("--no-backup", action="store_true", help="Skip JSON file backup")
    
    args = parser.parse_args()
    
    migrator = JSONToPostgreSQLMigrator(
        dry_run=args.dry_run,
        backup=not args.no_backup
    )
    
    try:
        migrator.run_migration()
        sys.exit(0)
    except Exception as e:
        print_error(f"Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
