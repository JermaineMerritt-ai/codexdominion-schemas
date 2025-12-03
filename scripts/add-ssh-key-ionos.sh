#!/bin/bash
# Run these commands on your IONOS server to add the SSH key

echo "🔐 Setting up SSH key for automated deployment..."

# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh

# Add the public key
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAID+tF/X+Yf2jL8NLGLCSjyQFNqOC9wiGkbw1gsx6goWd github@codexdominion.app' >> ~/.ssh/authorized_keys

# Set correct permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Remove duplicates
sort -u ~/.ssh/authorized_keys -o ~/.ssh/authorized_keys

echo "✅ SSH key added successfully!"
echo ""
echo "🔍 Authorized keys:"
cat ~/.ssh/authorized_keys

echo ""
echo "✅ Setup complete! You can now disconnect and test passwordless SSH."
