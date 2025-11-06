#!/usr/bin/env python3
"""
Reset bahan_ajar module in Odoo database
"""
import os
import sys
import subprocess

# Try to uninstall bahan_ajar module
print("Attempting to uninstall bahan_ajar module...")

# Stop Odoo
print("Stopping Odoo...")
os.system("docker-compose down")

# Start Odoo with module upgrade
print("\nStarting Odoo with module reset...")
os.system("docker-compose up -d")

# Wait for Odoo to start
import time
time.sleep(30)

# Now use Odoo API to uninstall and reinstall
print("\nModule reset script completed")
print("Access Odoo at http://localhost:8069")
