#!/usr/bin/env python3
"""
🔒 COSMIC DOMINION - SSL CERTIFICATE MANAGER 🔒
Python-based SSL certificate management and monitoring
"""

import subprocess
import sys
import json
import datetime
from pathlib import Path

class CosmicSSLManager:
    """SSL Certificate Manager for Cosmic Dominion"""
    
    def __init__(self, domain="aistorelab.com"):
        self.domain = domain
        self.www_domain = f"www.{domain}"
        self.email = f"admin@{domain}"
    
    def check_certbot_installed(self):
        """Check if Certbot is installed"""
        try:
            result = subprocess.run(['certbot', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Certbot installed: {result.stdout.strip()}")
                return True
            else:
                print("❌ Certbot not found")
                return False
        except FileNotFoundError:
            print("❌ Certbot not installed")
            return False
    
    def install_certbot(self):
        """Install Certbot on Ubuntu/Debian systems"""
        print("📦 Installing Certbot...")
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', 
                          'certbot', 'python3-certbot-nginx'], check=True)
            print("✅ Certbot installation completed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Certbot installation failed: {e}")
            return False
    
    def check_existing_certificates(self):
        """Check for existing certificates"""
        try:
            result = subprocess.run(['sudo', 'certbot', 'certificates'], 
                                  capture_output=True, text=True)
            
            if self.domain in result.stdout:
                print(f"📋 Existing certificates found for {self.domain}")
                return True
            else:
                print(f"🆕 No existing certificates for {self.domain}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error checking certificates: {e}")
            return False
    
    def obtain_certificates(self, interactive=True):
        """Obtain SSL certificates"""
        print(f"🔒 Obtaining SSL certificates for {self.domain} and {self.www_domain}...")
        
        cmd = [
            'sudo', 'certbot', '--nginx',
            '-d', self.domain,
            '-d', self.www_domain,
            '--email', self.email,
            '--agree-tos',
            '--redirect'
        ]
        
        if not interactive:
            cmd.extend(['--non-interactive', '--no-eff-email'])
        
        try:
            result = subprocess.run(cmd, check=True)
            print("✅ SSL certificates obtained successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to obtain SSL certificates: {e}")
            return False
    
    def setup_auto_renewal(self):
        """Set up automatic certificate renewal"""
        print("🔄 Setting up automatic certificate renewal...")
        
        try:
            # Enable certbot timer
            subprocess.run(['sudo', 'systemctl', 'enable', 'certbot.timer'], check=True)
            subprocess.run(['sudo', 'systemctl', 'start', 'certbot.timer'], check=True)
            
            print("✅ Certbot timer enabled and started")
            
            # Test renewal
            print("🧪 Testing renewal process...")
            subprocess.run(['sudo', 'certbot', 'renew', '--dry-run'], check=True)
            print("✅ Renewal test passed")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to setup auto-renewal: {e}")
            return False
    
    def create_renewal_hook(self):
        """Create post-renewal hook to reload Nginx"""
        print("🔧 Creating Nginx reload hook...")
        
        hook_dir = Path("/etc/letsencrypt/renewal-hooks/post")
        hook_script = hook_dir / "nginx-reload.sh"
        
        try:
            # Create directory
            subprocess.run(['sudo', 'mkdir', '-p', str(hook_dir)], check=True)
            
            # Create hook script
            hook_content = """#!/bin/bash
# Reload Nginx after certificate renewal
systemctl reload nginx
echo "🔒 Nginx reloaded after SSL certificate renewal - $(date)"
"""
            
            # Write hook script
            with open('temp_hook.sh', 'w') as f:
                f.write(hook_content)
            
            subprocess.run(['sudo', 'cp', 'temp_hook.sh', str(hook_script)], check=True)
            subprocess.run(['sudo', 'chmod', '+x', str(hook_script)], check=True)
            Path('temp_hook.sh').unlink()  # Clean up temp file
            
            print("✅ Nginx reload hook created")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create renewal hook: {e}")
            return False
    
    def get_certificate_info(self):
        """Get detailed certificate information"""
        try:
            result = subprocess.run(['sudo', 'certbot', 'certificates'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("📋 Certificate Information:")
                print(result.stdout)
                return result.stdout
            else:
                print("❌ Failed to get certificate information")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error getting certificate info: {e}")
            return None
    
    def check_ssl_status(self):
        """Check SSL status and connectivity"""
        print("🔍 Testing SSL connectivity...")
        
        urls = [f"https://{self.domain}", f"https://{self.www_domain}"]
        
        for url in urls:
            try:
                result = subprocess.run(['curl', '-s', '-I', url], 
                                      capture_output=True, text=True, timeout=10)
                
                if "HTTP" in result.stdout and "200" in result.stdout:
                    print(f"✅ SSL working: {url}")
                else:
                    print(f"⚠️ SSL test failed: {url}")
                    
            except Exception as e:
                print(f"❌ SSL test error for {url}: {e}")
    
    def check_timer_status(self):
        """Check certbot timer status"""
        try:
            result = subprocess.run(['systemctl', 'is-active', 'certbot.timer'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0 and 'active' in result.stdout:
                print("✅ Certbot timer: ACTIVE")
                
                # Get next run time
                timer_result = subprocess.run(['systemctl', 'list-timers', 'certbot.timer'], 
                                            capture_output=True, text=True)
                print(f"📅 Next renewal check: {timer_result.stdout.split('\n')[1] if timer_result.stdout else 'Unknown'}")
                return True
            else:
                print("❌ Certbot timer: INACTIVE")
                return False
                
        except Exception as e:
            print(f"❌ Error checking timer status: {e}")
            return False
    
    def full_setup(self):
        """Complete SSL setup process"""
        print("🔒 COSMIC DOMINION SSL SETUP 🔒")
        print("=" * 40)
        
        # Check if certbot is installed
        if not self.check_certbot_installed():
            if not self.install_certbot():
                return False
        
        # Check existing certificates
        has_existing = self.check_existing_certificates()
        
        if not has_existing:
            # Obtain new certificates
            if not self.obtain_certificates():
                return False
        
        # Set up auto-renewal
        if not self.setup_auto_renewal():
            return False
        
        # Create renewal hook
        if not self.create_renewal_hook():
            print("⚠️ Hook creation failed, but continuing...")
        
        # Final status check
        print("\n🌟 SSL Setup Complete!")
        print("=" * 25)
        
        self.get_certificate_info()
        self.check_ssl_status()
        self.check_timer_status()
        
        print(f"\n🔒 Your domain is now secured:")
        print(f"   https://{self.domain}")
        print(f"   https://{self.www_domain}")
        
        return True

def main():
    """Main SSL setup function"""
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = "aistorelab.com"
    
    ssl_manager = CosmicSSLManager(domain)
    
    if ssl_manager.full_setup():
        print("\n🔥 DIGITAL SOVEREIGNTY IS NOW ENCRYPTED! 🔥")
        sys.exit(0)
    else:
        print("\n❌ SSL setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()