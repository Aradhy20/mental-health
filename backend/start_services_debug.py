"""
Enhanced Service Startup Script with Debugging
Launches all backend services with health monitoring
"""

import subprocess
import sys
import os
import time
from pathlib import Path
import requests

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(msg):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"{msg}")
    print(f"{'='*60}{Colors.ENDC}\n")

def print_success(msg):
    print(f"{Colors.OKGREEN}[✓]{Colors.ENDC} {msg}")

def print_info(msg):
    print(f"{Colors.OKCYAN}[i]{Colors.ENDC} {msg}")

def print_warning(msg):
    print(f"{Colors.WARNING}[!]{Colors.ENDC} {msg}")

def print_error(msg):
    print(f"{Colors.FAIL}[✗]{Colors.ENDC} {msg}")

def check_port(port):
    """Check if a port is already in use"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def wait_for_service(port, timeout=10):
    """Wait for a service to become available"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=1)
            if response.status_code in [200, 404]:  # 404 for services without /health
                return True
        except:
            pass
        time.sleep(0.5)
    return False

def start_service(name, port, script="main.py"):
    """Start a single service with enhanced monitoring"""
    service_dir = Path(f"{name}_service")
    
    if not service_dir.exists():
        print_error(f"{name.title()} Service directory not found at {service_dir}")
        return None
    
    script_path = service_dir / script
    if not script_path.exists():
        print_warning(f"{name.title()} Service script not found: {script}")
        return None
    
    # Check if port is already in use
    if check_port(port):
        print_warning(f"{name.title()} Service already running on port {port}")
        return "already_running"
    
    print_info(f"Starting {name.title()} Service on port {port}...")
    
    try:
        # Start service in background with output capture
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            cwd=service_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for service to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print_error(f"{name.title()} Service failed to start")
            if stderr:
                print_error(f"Error: {stderr[:200]}")
            return None
        
        # Wait for service to respond
        if wait_for_service(port, timeout=5):
            print_success(f"{name.title()} Service running on http://localhost:{port}")
            return process
        else:
            print_warning(f"{name.title()} Service started but not responding on port {port}")
            return process
    
    except Exception as e:
        print_error(f"Failed to start {name} service: {e}")
        return None

def main():
    print_header("🚀 MENTAL HEALTH APP - SERVICE LAUNCHER")
    print_info("Enhanced version with health monitoring and debugging")
    
    services = [
        ("auth", 8001),
        ("text", 8002),
        ("voice", 8003),
        ("face", 8004),
        ("fusion", 8005),
        ("doctor", 8006),
        ("notification", 8007),
        ("mood_journal", 8008),
        ("report", 8009),
        ("chatbot", 8010),
    ]
    
    processes = []
    successful = 0
    already_running = 0
    failed = 0
    
    print_header("Starting Services")
    
    for name, port in services:
        result = start_service(name, port)
        if result == "already_running":
            already_running += 1
        elif result:
            processes.append((name, result, port))
            successful += 1
        else:
            failed += 1
        time.sleep(0.5)  # Small delay between starts
    
    # Summary
    print_header("Service Status Summary")
    print_success(f"Successfully started: {successful} services")
    if already_running > 0:
        print_info(f"Already running: {already_running} services")
    if failed > 0:
        print_error(f"Failed to start: {failed} services")
    
    total_active = successful + already_running
    print(f"\n{Colors.BOLD}Total Active Services: {total_active}/{len(services)}{Colors.ENDC}\n")
    
    if total_active > 0:
        print_header("Service Endpoints")
        for name, port in services:
            if check_port(port):
                print_success(f"{name.title():15} → http://localhost:{port}")
        
        print_info("\n💡 Run 'python debug_services.py' to check service health")
        print_info("💡 Press Ctrl+C to stop all services\n")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print_header("Shutting Down Services")
            for name, process, port in processes:
                print_info(f"Stopping {name} service...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except:
                    process.kill()
            print_success("\nAll services stopped")
    else:
        print_error("No services are running. Check for errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
