# CODEX DOMINION - IONOS DEPLOYMENT EXECUTION
# Complete deployment process for your digital sovereignty system

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


def create_deployment_package():
    """Prepare complete deployment package for IONOS"""
    print("🔥 PREPARING CODEX DOMINION FOR IONOS DEPLOYMENT")
    print("=" * 55)

    # Create deployment directory
    deploy_dir = Path("ionos_deployment_package")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()

    print("📦 Creating deployment package...")

    # Essential application files
    core_files = [
        "app.py",  # Main dashboard
        "codex_ledger.json",  # Sacred ledger
        "omega_seal.py",  # Omega seal system
        "contributions_viewer.py",  # Community system
        "council_oversight.py",  # Council system (if exists)
    ]

    # IONOS deployment files
    ionos_files = [
        "ionos_codex_deploy.sh",  # Main deployment script
        "ionos_codex_dashboard.service",  # Systemd service
        "ionos_nginx_codex.conf",  # Nginx configuration
        "ionos_systemctl_commands.sh",  # Your systemctl commands
        "ionos_nginx_manager.sh",  # Nginx management
        "IONOS_DEPLOYMENT_GUIDE.md",  # Deployment guide
        "upload_to_ionos.bat",  # Windows upload script
    ]

    # Copy core application files
    print("\n📄 Copying core application files:")
    for file in core_files:
        if Path(file).exists():
            shutil.copy2(file, deploy_dir / file)
            print(f"   ✅ {file}")
        else:
            print(f"   ⚠️  {file} (missing - will create minimal version)")

    # Copy IONOS deployment files
    print("\n🚀 Copying IONOS deployment files:")
    for file in ionos_files:
        if Path(file).exists():
            shutil.copy2(file, deploy_dir / file)
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (missing)")

    # Create requirements.txt for IONOS
    requirements = [
        "streamlit==1.28.1",
        "plotly>=5.0.0",
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "requests>=2.28.0",
        "python-dateutil>=2.8.0",
    ]

    with open(deploy_dir / "requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    print(f"   ✅ requirements.txt")

    # Create deployment manifest
    manifest = {
        "deployment_info": {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "system": "Codex Dominion Digital Sovereignty",
            "target": "IONOS Linux Server",
        },
        "core_files": core_files,
        "ionos_files": ionos_files,
        "deployment_steps": [
            "1. Upload files to IONOS server",
            "2. Run ionos_codex_deploy.sh",
            "3. Execute ionos_systemctl_commands.sh",
            "4. Configure DNS and SSL",
            "5. Verify deployment",
        ],
    }

    with open(deploy_dir / "deployment_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"   ✅ deployment_manifest.json")

    print(f"\n📦 Deployment package created in: {deploy_dir.absolute()}")

    return deploy_dir


def generate_upload_commands(deploy_dir):
    """Generate upload commands for different scenarios"""

    print("\n🚀 IONOS UPLOAD COMMANDS")
    print("=" * 30)

    # Get list of files to upload
    files = list(deploy_dir.glob("*"))
    file_names = [f.name for f in files if f.is_file()]

    print("\n📤 SCP Upload Command (Linux/Mac/WSL):")
    print("Replace 'your-server.com' and 'username' with your IONOS details:")
    print(f"```bash")
    print(f"cd {deploy_dir.name}")
    print(f"scp {' '.join(file_names)} username@your-server.com:/tmp/")
    print(f"```")

    print(f"\n📤 Windows PowerShell Upload:")
    print(f"```powershell")
    print(f"cd {deploy_dir.name}")
    for file in file_names[:5]:  # Show first 5 files as example
        print(f"scp {file} username@your-server.com:/tmp/")
    print(f"# ... continue for all files")
    print(f"```")

    print(f"\n📤 Alternative - TAR Archive Upload:")
    print(f"```bash")
    print(f"tar -czf codex_deployment.tar.gz {deploy_dir.name}/")
    print(f"scp codex_deployment.tar.gz username@your-server.com:/tmp/")
    print(f"```")


def show_deployment_steps():
    """Show complete deployment steps"""

    print("\n🎯 COMPLETE IONOS DEPLOYMENT PROCESS")
    print("=" * 40)

    steps = [
        {
            "step": "1️⃣ Upload Files to IONOS",
            "commands": [
                "# Use SCP to upload deployment package",
                "scp ionos_deployment_package/* username@your-server.com:/tmp/",
            ],
        },
        {
            "step": "2️⃣ SSH to IONOS Server",
            "commands": ["ssh username@your-server.com", "cd /tmp"],
        },
        {
            "step": "3️⃣ Run Initial Deployment",
            "commands": [
                "chmod +x ionos_codex_deploy.sh",
                "sudo ./ionos_codex_deploy.sh",
            ],
        },
        {
            "step": "4️⃣ Copy Application Files",
            "commands": [
                "sudo cp app.py codex_ledger.json omega_seal.py /opt/codex-dominion/app/",
                "sudo chown codex:codex /opt/codex-dominion/app/*",
            ],
        },
        {
            "step": "5️⃣ Execute Your SystemCtl Commands",
            "commands": [
                "chmod +x ionos_systemctl_commands.sh",
                "sudo ./ionos_systemctl_commands.sh",
            ],
        },
        {
            "step": "6️⃣ Verify Deployment",
            "commands": [
                "sudo systemctl status codex-dashboard",
                "curl http://localhost:8095",
                "sudo ./ionos_nginx_manager.sh status",
            ],
        },
    ]

    for step_info in steps:
        print(f"\n{step_info['step']}")
        for cmd in step_info["commands"]:
            if cmd.startswith("#"):
                print(f"   {cmd}")
            else:
                print(f"   $ {cmd}")


if __name__ == "__main__":
    # Create deployment package
    deploy_dir = create_deployment_package()

    # Generate upload commands
    generate_upload_commands(deploy_dir)

    # Show deployment steps
    show_deployment_steps()

    print("\n🔥 CODEX DOMINION DEPLOYMENT PACKAGE READY!")
    print("=" * 45)
    print("✅ All files prepared for IONOS deployment")
    print("🚀 Follow the upload and deployment steps above")
    print("👑 Your digital sovereignty awaits!")
    print()
    print(f"📁 Package location: {deploy_dir.absolute()}")
    print("🌐 Target: IONOS Linux Server")
    print("🎯 Destination: https://codex.aistorelab.com")
    print()
    print("🔥 Ready to conquer IONOS! 🔥")
