"""
Frontend Health Checker
Verifies all Next.js routes and API connections
"""

import requests
import json
from colorama import init, Fore, Style

init(autoreset=True)

FRONTEND_URL = "http://localhost:3000"

ROUTES = {
    "Dashboard": "/",
    "Login": "/login",
    "Register": "/register",
    "AI Chat": "/chat",
    "Mood Tracker": "/mood",
    "Journal": "/journal",
    "Meditation": "/meditation",
    "Insights": "/insights",
    "Settings": "/settings",
    "Wellness": "/wellness",
}

BACKEND_APIS = {
    "Auth": "http://localhost:8001/health",
    "Mood/Journal": "http://localhost:8008/health",
    "Doctor": "http://localhost:8006/health",
    "Chatbot": "http://localhost:8010/v1/greeting",
}

def check_route(name, path):
    """Check if a frontend route loads"""
    try:
        response = requests.get(f"{FRONTEND_URL}{path}", timeout=5)
        return {
            "status": "ok" if response.status_code == 200 else "error",
            "code": response.status_code
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}

def check_api(name, url):
    """Check backend API"""
    try:
        response = requests.get(url, timeout=3)
        return {
            "status": "ok" if response.status_code in [200, 404] else "error",
            "response_time": f"{response.elapsed.total_seconds()*1000:.0f}ms"
        }
    except Exception as e:
        return {"status": "offline", "error": "Not running"}

print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
print(f"🎨 FRONTEND HEALTH CHECK")
print(f"{'='*70}\n")

print(f"{Fore.YELLOW}📱 Checking Frontend Routes...")
print()

for name, path in ROUTES.items():
    result = check_route(name, path)
    if result["status"] == "ok":
        print(f"{Fore.GREEN}✅ {name:<20} {Fore.CYAN}{path:<25} {Fore.GREEN}OK")
    else:
        print(f"{Fore.RED}❌ {name:<20} {Fore.CYAN}{path:<25} {Fore.RED}FAILED")

print(f"\n{Fore.YELLOW}🔌 Checking Backend API Connections...")
print()

for name, url in BACKEND_APIS.items():
    result = check_api(name, url)
    if result["status"] == "ok":
        time = result.get("response_time", "N/A")
        print(f"{Fore.GREEN}✅ {name:<20} {Fore.WHITE}{time:<15} {Fore.GREEN}CONNECTED")
    else:
        print(f"{Fore.RED}🔴 {name:<20} {Fore.RED}OFFLINE")

print(f"\n{Fore.CYAN}{'='*70}\n")
print(f"{Fore.WHITE}💡 Tip: Make sure both frontend (npm run dev) and backend services are running")
print()
