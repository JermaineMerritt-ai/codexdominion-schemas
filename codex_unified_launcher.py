#!/usr/bin/env python3
"""
Codex Treasury & Dawn Dispatch Unified Launcher
==============================================

A unified command-line interface for managing treasury operations
and dawn dispatches in the Codex Dominion system.

Usage:
  python codex_unified_launcher.py [command] [options]

Commands:
  treasury    - Treasury operations
  dawn        - Dawn dispatch operations  
  status      - Show system status
  report      - Generate comprehensive report
  setup       - Setup database (if PostgreSQL available)
"""

import argparse
import datetime
import json
import sys
from pathlib import Path

# Import Codex modules
try:
    from codex_treasury_database import CodexTreasury
    from dawn_dispatch_simple import dawn_dispatch, get_dawn_status
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Module import error: {e}")
    MODULES_AVAILABLE = False

class CodexUnifiedLauncher:
    """Unified launcher for Codex Treasury and Dawn Dispatch operations."""
    
    def __init__(self):
        """Initialize the launcher."""
        if MODULES_AVAILABLE:
            self.treasury = CodexTreasury()
        else:
            self.treasury = None
    
    def cmd_treasury(self, args):
        """Handle treasury operations."""
        if not self.treasury:
            print("❌ Treasury system not available")
            return False
        
        if args.action == "summary":
            return self._treasury_summary(args.days or 30)
        
        elif args.action == "ingest":
            return self._treasury_ingest(args)
        
        elif args.action == "list":
            return self._treasury_list(args.limit or 10)
        
        else:
            print("❌ Unknown treasury action. Use: summary, ingest, list")
            return False
    
    def _treasury_summary(self, days):
        """Show treasury summary."""
        try:
            print(f"📊 Treasury Summary (Last {days} days)")
            print("=" * 40)
            
            summary = self.treasury.get_treasury_summary(days)
            
            print(f"💰 Total Revenue: ${summary['total_revenue']:.2f}")
            print(f"📈 Transactions: {summary['total_transactions']}")
            print(f"🗄️  Data Source: {summary['source']}")
            
            if summary['revenue_streams']:
                print(f"\n📊 Revenue Streams:")
                for stream, data in summary['revenue_streams'].items():
                    print(f"   {stream.title()}: ${data['total_amount']:.2f} ({data['transaction_count']} txns)")
            
            return True
        except Exception as e:
            print(f"❌ Treasury summary failed: {e}")
            return False
    
    def _treasury_ingest(self, args):
        """Ingest a new treasury transaction."""
        try:
            if not all([args.stream, args.amount]):
                print("❌ Stream and amount required for ingestion")
                return False
            
            # Determine ingestion method based on stream
            if args.stream == "affiliate":
                if not args.order_id:
                    print("❌ Order ID required for affiliate transactions")
                    return False
                txn_id = self.treasury.ingest_affiliate(args.order_id, args.amount, args.currency or "USD")
            
            elif args.stream == "stock":
                if not args.symbol:
                    print("❌ Symbol required for stock transactions")
                    return False
                txn_id = self.treasury.ingest_stock(args.symbol, args.amount, args.currency or "USD")
            
            elif args.stream == "amm":
                if not args.pool_id:
                    print("❌ Pool ID required for AMM transactions")
                    return False
                txn_id = self.treasury.ingest_amm(args.pool_id, args.amount, args.currency or "USD")
            
            elif args.stream == "consulting":
                client_id = args.client_id or "default-client"
                hours = args.hours or (args.amount / 150.0)  # Default rate
                rate = args.amount / hours if hours > 0 else 150.0
                txn_id = self.treasury.ingest_consulting(client_id, hours, rate, args.currency or "USD")
            
            elif args.stream == "development":
                project_id = args.project_id or "default-project"
                txn_id = self.treasury.ingest_development(project_id, args.amount, args.currency or "USD")
            
            else:
                # Generic transaction
                txn_id = self.treasury.archive_transaction(
                    args.stream, args.amount, args.currency or "USD", 
                    args.source or "", args.status or "pending"
                )
            
            print(f"✅ Transaction ingested: {txn_id}")
            return True
            
        except Exception as e:
            print(f"❌ Treasury ingestion failed: {e}")
            return False
    
    def _treasury_list(self, limit):
        """List recent transactions."""
        try:
            ledger = self.treasury.load_ledger()
            transactions = ledger.get("transactions", [])
            
            if not transactions:
                print("📭 No transactions found")
                return True
            
            recent = transactions[-limit:]
            
            print(f"📋 Recent Transactions (Last {len(recent)}):")
            print("-" * 50)
            
            for txn in recent:
                created = txn['created_at'][:19]  # Remove timezone for display
                print(f"{txn['id']}: {txn['stream']} ${txn['amount']:.2f}")
                print(f"   {created} | {txn['status']} | {txn['source']}")
                print()
            
            return True
        except Exception as e:
            print(f"❌ Transaction listing failed: {e}")
            return False
    
    def cmd_dawn(self, args):
        """Handle dawn dispatch operations."""
        try:
            if args.action == "dispatch":
                print("🌅 Executing Dawn Dispatch...")
                result = dawn_dispatch(args.proclamation)
                if result.get("success"):
                    print(f"✅ Dawn Dispatch completed: {result['dispatch_id']}")
                    return True
                else:
                    print(f"❌ Dawn Dispatch failed: {result.get('error')}")
                    return False
            
            elif args.action == "status":
                print("📊 Dawn Dispatch Status:")
                status = get_dawn_status()
                print(f"   Date: {status['date']}")
                print(f"   Dispatched Today: {'Yes' if status['dispatched_today'] else 'No'}")
                print(f"   Total Dispatches: {status['total_dispatches']}")
                print(f"   Flame Status: {status['flame_status']}")
                return True
            
            else:
                print("❌ Unknown dawn action. Use: dispatch, status")
                return False
                
        except Exception as e:
            print(f"❌ Dawn dispatch operation failed: {e}")
            return False
    
    def cmd_serve(self, args):
        """Start web server for Cloud Run deployment."""
        try:
            from flask import Flask, jsonify, request
            import os
            
            # Create Flask app
            app = Flask(__name__)
            
            @app.route('/health')
            def health_check():
                """Health check endpoint for Cloud Run."""
                try:
                    # Test treasury system
                    treasury_status = "operational" if self.treasury else "json-only"
                    
                    # Test dawn dispatch
                    dawn_status = get_dawn_status() if MODULES_AVAILABLE else {"flame_status": "unknown"}
                    
                    return jsonify({
                        "status": "healthy",
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "treasury": treasury_status,
                        "dawn_flame": dawn_status.get("flame_status", "unknown"),
                        "version": "1.0.0"
                    }), 200
                    
                except Exception as e:
                    return jsonify({
                        "status": "unhealthy",
                        "error": str(e),
                        "timestamp": datetime.datetime.utcnow().isoformat()
                    }), 503
            
            @app.route('/api/treasury/summary')
            def treasury_summary():
                """API endpoint for treasury summary."""
                try:
                    days = int(request.args.get('days', 7))
                    if self.treasury:
                        summary = self.treasury.get_treasury_summary(days)
                        return jsonify(summary)
                    else:
                        return jsonify({"error": "Treasury system not available"}), 503
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            
            @app.route('/api/dawn/status')
            def dawn_status():
                """API endpoint for dawn dispatch status."""
                try:
                    if MODULES_AVAILABLE:
                        status = get_dawn_status()
                        return jsonify(status)
                    else:
                        return jsonify({"error": "Dawn dispatch not available"}), 503
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            
            @app.route('/api/dawn/dispatch', methods=['POST'])
            def dawn_dispatch_endpoint():
                """Cloud Scheduler endpoint for dawn dispatch."""
                try:
                    from codex_dawn_dispatch import dawn_dispatch
                    
                    # Execute dawn dispatch
                    result = dawn_dispatch()
                    
                    if result.get("success"):
                        return jsonify({
                            "success": True,
                            "message": "Dawn dispatch executed successfully",
                            "timestamp": result.get("timestamp"),
                            "archived": result.get("archived", False)
                        }), 200
                    else:
                        return jsonify({
                            "success": False,
                            "error": result.get("error"),
                            "timestamp": result.get("timestamp")
                        }), 500
                        
                except ImportError:
                    return jsonify({
                        "success": False,
                        "error": "Dawn dispatch module not available"
                    }), 503
                except Exception as e:
                    return jsonify({
                        "success": False,
                        "error": str(e),
                        "timestamp": datetime.datetime.utcnow().isoformat()
                    }), 500
            
            @app.route('/dawn', methods=['POST'])
            def dawn_dispatch_scheduler():
                """Simplified endpoint matching your gcloud command."""
                return dawn_dispatch_endpoint()
            
            @app.route('/signals/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
            def signals_proxy(path):
                """Proxy requests to FastAPI Signals service"""
                try:
                    import subprocess
                    import json as json_lib
                    
                    # Check if FastAPI signals service is available
                    signals_url = f"http://localhost:8000/signals/{path}"
                    
                    # For now, return a redirect response
                    return jsonify({
                        "message": "Codex Signals API Available",
                        "fastapi_url": f"http://localhost:8000/signals/{path}",
                        "documentation": "http://localhost:8000/docs",
                        "note": "Start FastAPI service with: uvicorn codex_signals.api:app --port 8000"
                    }), 200
                    
                except Exception as e:
                    return jsonify({
                        "error": "Signals service not available",
                        "details": str(e),
                        "setup": "pip install fastapi uvicorn"
                    }), 503
            
            @app.route('/docs')
            def api_docs():
                """Redirect to FastAPI documentation"""
                return jsonify({
                    "message": "Interactive API Documentation",
                    "fastapi_docs": "http://localhost:8000/docs",
                    "redoc": "http://localhost:8000/redoc",
                    "note": "Start FastAPI service: uvicorn codex_signals.api:app --port 8000"
                })
            
            @app.route('/')
            def index():
                """Main page with system overview."""
                return jsonify({
                    "message": "🔥 Codex Dominion Treasury & Dawn Dispatch System",
                    "status": "operational",
                    "endpoints": {
                        "health": "/health",
                        "treasury_summary": "/api/treasury/summary?days=7",
                        "dawn_status": "/api/dawn/status",
                        "dawn_dispatch": "/api/dawn/dispatch (POST)",
                        "scheduler_endpoint": "/dawn (POST)",
                        "signals_api": "/signals/* (Codex Signals Engine)",
                        "signals_docs": "/docs (Interactive API Documentation)"
                    },
                    "timestamp": datetime.datetime.utcnow().isoformat()
                })
            
            # Start server
            print(f"🚀 Starting Codex Dominion web server on {args.host}:{args.port}")
            print(f"🔥 Health check: http://{args.host}:{args.port}/health")
            print(f"📊 Treasury API: http://{args.host}:{args.port}/api/treasury/summary")
            print(f"🌅 Dawn API: http://{args.host}:{args.port}/api/dawn/status")
            print(f"⏰ Dawn Dispatch: http://{args.host}:{args.port}/dawn (POST)")
            print(f"🤖 Cloud Scheduler ready for automated dawn dispatches")
            
            # Use the PORT environment variable if set (Cloud Run requirement)
            port = int(os.environ.get('PORT', args.port))
            
            app.run(
                host=args.host,
                port=port,
                debug=args.debug,
                threaded=True
            )
            
            return True
            
        except ImportError:
            print("❌ Flask not available. Install with: pip install flask")
            return False
        except Exception as e:
            print(f"❌ Server start failed: {e}")
            return False
    
    def cmd_status(self, args):
        """Show overall system status."""
        try:
            print("🔍 Codex Dominion System Status")
            print("=" * 35)
            
            # Treasury status
            if self.treasury:
                summary = self.treasury.get_treasury_summary(7)  # Last 7 days
                print(f"💰 Treasury (7 days): ${summary['total_revenue']:.2f} ({summary['total_transactions']} txns)")
                print(f"🗄️  Data Source: {summary['source']}")
            else:
                print("💰 Treasury: Not Available")
            
            # Dawn dispatch status
            try:
                status = get_dawn_status()
                print(f"🌅 Dawn Status: {status['flame_status']} ({status['total_dispatches']} total)")
                print(f"   Today: {'Dispatched' if status['dispatched_today'] else 'Pending'}")
            except:
                print("🌅 Dawn Status: Not Available")
            
            # Ledger status
            try:
                ledger_path = Path("codex_ledger.json")
                if ledger_path.exists():
                    with open(ledger_path, 'r') as f:
                        ledger = json.load(f)
                    
                    cycles = len(ledger.get("cycles", []))
                    proclamations = len(ledger.get("proclamations", []))
                    print(f"📜 Ledger: {cycles} cycles, {proclamations} proclamations")
                    
                    if "meta" in ledger:
                        last_update = ledger["meta"].get("last_updated", "Unknown")[:19]
                        print(f"   Last Updated: {last_update}")
                else:
                    print("📜 Ledger: Not Found")
            except Exception as e:
                print(f"📜 Ledger: Error reading ({e})")
            
            # Database status
            if self.treasury and self.treasury.connection_pool:
                print("🗃️  Database: PostgreSQL Connected")
            else:
                print("🗃️  Database: JSON-Only Mode")
            
            return True
            
        except Exception as e:
            print(f"❌ Status check failed: {e}")
            return False
    
    def cmd_report(self, args):
        """Generate comprehensive system report."""
        try:
            print("📋 Codex Dominion Comprehensive Report")
            print("=" * 45)
            print(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Treasury report
            if self.treasury:
                print(f"\n💰 TREASURY REPORT")
                print("-" * 20)
                
                summary = self.treasury.get_treasury_summary(30)
                print(f"Total Revenue (30d): ${summary['total_revenue']:.2f}")
                print(f"Total Transactions: {summary['total_transactions']}")
                
                for stream, data in summary['revenue_streams'].items():
                    print(f"  {stream.title()}: ${data['total_amount']:.2f}")
            
            # Dawn dispatch report  
            try:
                print(f"\n🌅 DAWN DISPATCH REPORT")
                print("-" * 25)
                
                status = get_dawn_status()
                print(f"Total Dispatches: {status['total_dispatches']}")
                print(f"Today's Status: {'✅ Complete' if status['dispatched_today'] else '⏳ Pending'}")
                print(f"Flame Status: {status['flame_status']}")
            except:
                print(f"\n🌅 Dawn Dispatch: Not Available")
            
            # System health
            print(f"\n⚡ SYSTEM HEALTH")
            print("-" * 17)
            
            health_score = 0
            total_checks = 4
            
            # Check treasury
            if self.treasury:
                health_score += 1
                print("✅ Treasury System")
            else:
                print("❌ Treasury System")
            
            # Check dawn dispatch
            try:
                get_dawn_status()
                health_score += 1
                print("✅ Dawn Dispatch")
            except:
                print("❌ Dawn Dispatch")
            
            # Check ledger
            if Path("codex_ledger.json").exists():
                health_score += 1
                print("✅ Codex Ledger")
            else:
                print("❌ Codex Ledger")
            
            # Check database
            if self.treasury and self.treasury.connection_pool:
                health_score += 1
                print("✅ Database (PostgreSQL)")
            else:
                print("⚠️  Database (JSON-only)")
            
            health_percent = (health_score / total_checks) * 100
            print(f"\nOverall Health: {health_percent:.0f}% ({health_score}/{total_checks})")
            
            return True
            
        except Exception as e:
            print(f"❌ Report generation failed: {e}")
            return False
    
    def cmd_setup(self, args):
        """Setup database and configuration."""
        try:
            print("🔧 Codex System Setup")
            print("=" * 20)
            
            # Try to setup database
            try:
                from setup_treasury_database import CodexDatabaseSetup
                
                setup = CodexDatabaseSetup()
                
                print("Setting up PostgreSQL database...")
                if setup.create_database():
                    print("✅ Database created")
                    
                    if setup.create_tables():
                        print("✅ Tables created")
                        
                        if setup.insert_sample_data():
                            print("✅ Sample data inserted")
                        
                        if setup.test_connection():
                            print("✅ Connection verified")
                            print("🎉 PostgreSQL setup complete!")
                        else:
                            print("⚠️  Connection verification failed")
                    else:
                        print("❌ Table creation failed")
                else:
                    print("❌ Database creation failed")
                    
            except ImportError:
                print("⚠️  PostgreSQL setup not available (missing psycopg2)")
                print("   System will work in JSON-only mode")
            except Exception as e:
                print(f"❌ Database setup failed: {e}")
            
            # Verify JSON systems
            print(f"\nVerifying JSON systems...")
            if Path("codex_ledger.json").exists():
                print("✅ Codex ledger found")
            else:
                print("⚠️  Codex ledger will be created on first use")
            
            # Test treasury
            if self.treasury:
                print("✅ Treasury system ready")
            else:
                print("❌ Treasury system not available")
            
            return True
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Codex Treasury & Dawn Dispatch Unified Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Treasury operations
  python codex_unified_launcher.py treasury summary --days 30
  python codex_unified_launcher.py treasury ingest --stream affiliate --order-id A123 --amount 49.99
  python codex_unified_launcher.py treasury list --limit 10
  
  # Dawn dispatch operations
  python codex_unified_launcher.py dawn dispatch --proclamation "Custom message"
  python codex_unified_launcher.py dawn status
  
  # System operations
  python codex_unified_launcher.py status
  python codex_unified_launcher.py report
  python codex_unified_launcher.py setup
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Treasury subcommand
    treasury_parser = subparsers.add_parser('treasury', help='Treasury operations')
    treasury_parser.add_argument('action', choices=['summary', 'ingest', 'list'], help='Treasury action')
    treasury_parser.add_argument('--days', type=int, help='Days for summary')
    treasury_parser.add_argument('--stream', help='Revenue stream')
    treasury_parser.add_argument('--amount', type=float, help='Transaction amount')
    treasury_parser.add_argument('--currency', default='USD', help='Currency')
    treasury_parser.add_argument('--source', help='Transaction source')
    treasury_parser.add_argument('--status', help='Transaction status')
    treasury_parser.add_argument('--order-id', help='Order ID for affiliate')
    treasury_parser.add_argument('--symbol', help='Symbol for stock')
    treasury_parser.add_argument('--pool-id', help='Pool ID for AMM')
    treasury_parser.add_argument('--client-id', help='Client ID for consulting')
    treasury_parser.add_argument('--project-id', help='Project ID for development')
    treasury_parser.add_argument('--hours', type=float, help='Hours for consulting')
    treasury_parser.add_argument('--limit', type=int, help='Limit for list')
    
    # Dawn subcommand
    dawn_parser = subparsers.add_parser('dawn', help='Dawn dispatch operations')
    dawn_parser.add_argument('action', choices=['dispatch', 'status'], help='Dawn action')
    dawn_parser.add_argument('--proclamation', help='Custom proclamation')
    
    # Status subcommand
    subparsers.add_parser('status', help='Show system status')
    
    # Report subcommand
    subparsers.add_parser('report', help='Generate comprehensive report')
    
    # Setup subcommand
    subparsers.add_parser('setup', help='Setup database and configuration')
    
    # Serve subcommand (for Cloud Run)
    serve_parser = subparsers.add_parser('serve', help='Start web server for Cloud Run')
    serve_parser.add_argument('--host', default='0.0.0.0', help='Host address')
    serve_parser.add_argument('--port', type=int, default=8080, help='Port number')
    serve_parser.add_argument('--debug', action='store_true', help='Debug mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize launcher
    if not MODULES_AVAILABLE and args.command != 'serve':
        print("❌ Required modules not available")
        return
    
    launcher = CodexUnifiedLauncher()
    
    # Route command
    if args.command == 'treasury':
        success = launcher.cmd_treasury(args)
    elif args.command == 'dawn':
        success = launcher.cmd_dawn(args)
    elif args.command == 'status':
        success = launcher.cmd_status(args)
    elif args.command == 'report':
        success = launcher.cmd_report(args)
    elif args.command == 'setup':
        success = launcher.cmd_setup(args)
    elif args.command == 'serve':
        success = launcher.cmd_serve(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        success = False
    
    if success:
        print(f"\n🔥 Operation completed successfully")
    else:
        print(f"\n❌ Operation failed")

if __name__ == "__main__":
    main()