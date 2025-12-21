#!/usr/bin/env python3
"""
Script to start both frontend and backend services for the Mental Health App
"""
import os
import subprocess
import sys
import time
import signal
import threading

class AppManager:
    def __init__(self):
        self.processes = []
        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    def start_backend_services(self):
        """Start all backend services"""
        print("Starting Mental Health App Backend Services...")
        print("=" * 50)
        
        # Change to the project directory
        os.chdir(self.project_dir)
        
        # Define the services and their ports
        services = [
            {"name": "Auth Service", "port": 8001, "path": "backend/auth_service/main.py"},
            {"name": "Text Analysis", "port": 8002, "path": "backend/text_service/main.py"},
            {"name": "Voice Analysis", "port": 8003, "path": "backend/voice_service/main.py"},
            {"name": "Face Analysis", "port": 8004, "path": "backend/face_service/main.py"},
            {"name": "Fusion Service", "port": 8005, "path": "backend/fusion_service/main.py"},
            {"name": "Doctor Service", "port": 8006, "path": "backend/doctor_service/main.py"},
            {"name": "Notification Service", "port": 8007, "path": "backend/notification_service/main.py"},
            {"name": "Report Service", "port": 8008, "path": "backend/report_service/main.py"},
            {"name": "Assistant Service", "port": 8009, "path": "backend/assistant_service/main.py"},
        ]
        
        # Start all services
        for service in services:
            try:
                # Set the PYTHONPATH to include the backend directory
                env = os.environ.copy()
                env['PYTHONPATH'] = os.path.join(self.project_dir, 'backend')
                
                # Start the service
                process = subprocess.Popen([
                    sys.executable, service['path']
                ], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                self.processes.append(process)
                print(f"Started {service['name']} on port {service['port']} (PID: {process.pid})")
                time.sleep(0.5)  # Small delay between starting services
            except Exception as e:
                print(f"Failed to start {service['name']}: {e}")
        
        print("\nBackend services started successfully!")
        
    def start_frontend_service(self):
        """Start the frontend service"""
        print("\nStarting Frontend Service...")
        print("=" * 30)
        
        frontend_dir = os.path.join(self.project_dir, 'frontend')
        os.chdir(frontend_dir)
        
        try:
            # Start the Next.js frontend
            process = subprocess.Popen([
                'npm', 'run', 'dev'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes.append(process)
            print(f"Frontend service started (PID: {process.pid})")
            print("Frontend will be available at http://localhost:3000")
        except Exception as e:
            print(f"Failed to start frontend service: {e}")
            
        # Change back to project directory
        os.chdir(self.project_dir)
        
    def stop_all_services(self):
        """Stop all running services"""
        print("\nStopping all services...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        print("All services stopped.")
        
    def signal_handler(self, sig, frame):
        """Handle interrupt signals"""
        print('\nReceived interrupt signal. Shutting down...')
        self.stop_all_services()
        sys.exit(0)
        
    def run(self):
        """Main run method"""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Start backend services
            self.start_backend_services()
            
            # Start frontend service
            self.start_frontend_service()
            
            print("\n" + "=" * 60)
            print("MENTAL HEALTH APP IS NOW RUNNING!")
            print("=" * 60)
            print("Backend services:")
            print("  - Auth Service:     http://localhost:8001")
            print("  - Text Analysis:    http://localhost:8002")
            print("  - Voice Analysis:   http://localhost:8003")
            print("  - Face Analysis:    http://localhost:8004")
            print("  - Fusion Service:   http://localhost:8005")
            print("  - Doctor Service:   http://localhost:8006")
            print("  - Notification:     http://localhost:8007")
            print("  - Report Service:   http://localhost:8008")
            print("  - Assistant Service: http://localhost:8009")
            print("")
            print("Frontend service:")
            print("  - Web Application:  http://localhost:3000")
            print("=" * 60)
            print("Press Ctrl+C to stop all services")
            print("=" * 60)
            
            # Keep the main thread alive
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.stop_all_services()

if __name__ == "__main__":
    manager = AppManager()
    manager.run()