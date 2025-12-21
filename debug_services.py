"""
Service Health Checker & Debugger
Real-time monitoring tool for all microservices
"""

import requests
import json
from datetime import datetime
from colorama import init, Fore, Style
import time

init(autoreset=True)

SERVICES = {
    "Auth Service": "http://localhost:8001/health",
    "Text Service": "http://localhost:8002/health",
    "Voice Service": "http://localhost:8003/health",
    "Face Service": "http://localhost:8004/health",
    "Fusion Service": "http://localhost:8005/health",
    "Doctor Service": "http://localhost:8006/health",
    "Notification Service": "http://localhost:8007/health",
    "Mood Journal Service": "http://localhost:8008/health",
    "Report Service": "http://localhost:8009/health",
    "Chatbot Service": "http://localhost:8010/v1/greeting",
}

def check_service(name, url):
    """Check if a service is running and healthy"""
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return {
                "status": "healthy",
                "response_time": response.elapsed.total_seconds(),
                "data": response.json() if response.headers.get('content-type') == 'application/json' else None
            }
        else:
            return {
                "status": "unhealthy",
                "error": f"Status code: {response.status_code}"
            }
    except requests.exceptions.ConnectionError:
        return {
            "status": "offline",
            "error": "Connection refused - Service not running"
        }
    except requests.exceptions.Timeout:
        return {
            "status": "timeout",
            "error": "Request timeout - Service too slow"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def print_header():
    """Print colorful header"""
    print("\n" + "="*70)
    print(Fore.CYAN + Style.BRIGHT + "🏥 MENTAL HEALTH APP - SERVICE HEALTH MONITOR")
    print(Fore.YELLOW + f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")

def print_service_status(name, port, result):
    """Print formatted service status"""
    status = result["status"]
    
    if status == "healthy":
        icon = Fore.GREEN + "✅"
        status_text = Fore.GREEN + "HEALTHY"
        details = f"Response: {result['response_time']*1000:.0f}ms"
    elif status == "offline":
        icon = Fore.RED + "🔴"
        status_text = Fore.RED + "OFFLINE"
        details = result["error"]
    elif status == "timeout":
        icon = Fore.YELLOW + "⏱️"
        status_text = Fore.YELLOW + "TIMEOUT"
        details = result["error"]
    else:
        icon = Fore.RED + "❌"
        status_text = Fore.RED + "ERROR"
        details = result["error"]
    
    print(f"{icon} {Fore.WHITE}{Style.BRIGHT}{name:<25} {status_text:<15} {Fore.CYAN}{details}")

def run_health_check():
    """Run health check on all services"""
    print_header()
    
    healthy_count = 0
    total_count = len(SERVICES)
    
    results = {}
    
    for name, url in SERVICES.items():
        port = url.split(":")[2].split("/")[0]
        result = check_service(name, url)
        results[name] = result
        
        if result["status"] == "healthy":
            healthy_count += 1
        
        print_service_status(name, port, result)
    
    # Summary
    print("\n" + "="*70)
    health_percentage = (healthy_count / total_count) * 100
    
    if health_percentage == 100:
        color = Fore.GREEN
        emoji = "🎉"
    elif health_percentage >= 70:
        color = Fore.YELLOW
        emoji = "⚠️"
    else:
        color = Fore.RED
        emoji = "🚨"
    
    print(f"{emoji} {color}{Style.BRIGHT}System Health: {healthy_count}/{total_count} services ({health_percentage:.0f}%)")
    print("="*70 + "\n")
    
    # Recommendations
    offline_services = [name for name, result in results.items() if result["status"] == "offline"]
    if offline_services:
        print(Fore.YELLOW + "⚡ RECOMMENDATIONS:")
        print(Fore.WHITE + f"   • {len(offline_services)} service(s) are offline")
        print(Fore.WHITE + "   • Run: " + Fore.CYAN + "python backend/start_services.py")
        print()
    
    return results

def continuous_monitor(interval=10):
    """Continuously monitor services"""
    print(Fore.CYAN + "Starting continuous monitoring (Ctrl+C to stop)...\n")
    try:
        while True:
            run_health_check()
            time.sleep(interval)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⏹️  Monitoring stopped by user")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "watch":
        continuous_monitor()
    else:
        run_health_check()
        print(Fore.CYAN + "💡 Tip: Run " + Fore.WHITE + "'python debug_services.py watch'" + Fore.CYAN + " for continuous monitoring\n")
