"""
Database Inspector & Debugger
Inspect database contents and verify data integrity
"""

import sqlite3
import os
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

DB_PATH = "backend/mental_health.db"

def print_header(title):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
    print(f"{title}")
    print(f"{'='*70}\n")

def get_table_stats(cursor, table_name):
    """Get statistics for a table"""
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    return count

def inspect_database():
    """Inspect the SQLite database"""
    if not os.path.exists(DB_PATH):
        print(f"{Fore.RED}❌ Database not found at {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print_header("📊 DATABASE INSPECTOR")
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"{Fore.YELLOW}📋 Database Tables ({len(tables)} total):\n")
    
    table_stats = {}
    for table in tables:
        count = get_table_stats(cursor, table)
        table_stats[table] = count
        
        if count > 0:
            icon = Fore.GREEN + "✅"
        else:
            icon = Fore.YELLOW + "⚠️"
        
        print(f"{icon} {Fore.WHITE}{table:<30} {Fore.CYAN}{count} records")
    
    # Detailed inspection of key tables
    print_header("🔍 DETAILED DATA INSPECTION")
    
    # Users
    if table_stats.get('users', 0) > 0:
        print(f"{Fore.YELLOW}👥 Users Table:")
        cursor.execute("SELECT user_id, username, email, name FROM users LIMIT 5")
        for row in cursor.fetchall():
            print(f"  {Fore.WHITE}ID:{row[0]:<5} {Fore.CYAN}@{row[1]:<15} {Fore.WHITE}{row[3] or 'No name'}")
        print()
    
    # Mood Tracking
    if table_stats.get('mood_tracking', 0) > 0:
        print(f"{Fore.YELLOW}😊 Recent Mood Entries:")
        cursor.execute("SELECT user_id, mood_label, score, timestamp FROM mood_tracking ORDER BY timestamp DESC LIMIT 5")
        for row in cursor.fetchall():
            print(f"  {Fore.CYAN}User {row[0]}: {Fore.WHITE}{row[1]} (score: {row[2]}) - {row[3]}")
        print()
    
    # Journal Entries
    if table_stats.get('journal_entries', 0) > 0:
        print(f"{Fore.YELLOW}📔 Recent Journal Entries:")
        cursor.execute("SELECT user_id, title, created_at FROM journal_entries ORDER BY created_at DESC LIMIT 5")
        for row in cursor.fetchall():
            print(f"  {Fore.CYAN}User {row[0]}: {Fore.WHITE}\"{row[1]}\" - {row[2]}")
        print()
    
    # Doctors
    if table_stats.get('doctors', 0) > 0:
        print(f"{Fore.YELLOW}🏥 Registered Doctors:")
        cursor.execute("SELECT doctor_id, name, specialization, rating FROM doctors")
        for row in cursor.fetchall():
            stars = "⭐" * int(float(row[3] or 0))
            print(f"  {Fore.WHITE}Dr. {row[1]:<25} {Fore.CYAN}{row[2]:<25} {Fore.YELLOW}{stars}")
        print()
    
    # Database file info
    print_header("💾 DATABASE FILE INFO")
    db_size = os.path.getsize(DB_PATH)
    size_mb = db_size / (1024 * 1024)
    modified = datetime.fromtimestamp(os.path.getmtime(DB_PATH))
    
    print(f"{Fore.WHITE}📂 Path: {Fore.CYAN}{DB_PATH}")
    print(f"{Fore.WHITE}💿 Size: {Fore.CYAN}{size_mb:.2f} MB ({db_size:,} bytes)")
    print(f"{Fore.WHITE}🕐 Last Modified: {Fore.CYAN}{modified.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    conn.close()

if __name__ == "__main__":
    inspect_database()
