"""
SQLite to MongoDB Migration Script
Migrates data from SQLite databases to MongoDB
"""

import asyncio
import sqlite3
from datetime import datetime
import sys
import os

# Add shared to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared'))

from shared.mongodb import (
    text_collection, voice_collection, mood_collection,
    check_connection, create_indexes, logger
)


async def migrate_text_analysis():
    """Migrate text analysis data from SQLite to MongoDB"""
    logger.info("Starting text analysis migration...")
    
    try:
        # Connect to SQLite database
        sqlite_path = os.path.join(os.path.dirname(__file__), 'test.db')
        if not os.path.exists(sqlite_path):
            logger.warning(f"SQLite database not found at {sqlite_path}")
            return 0
        
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='text_analysis'")
        if not cursor.fetchone():
            logger.warning("text_analysis table not found in SQLite")
            conn.close()
            return 0
        
        # Fetch all text analysis records
        cursor.execute("""
            SELECT user_id, input_text, emotion_label, emotion_score, confidence, created_at
            FROM text_analysis
        """)
        
        records = cursor.fetchall()
        migrated_count = 0
        
        for record in records:
            user_id, input_text, emotion_label, emotion_score, confidence, created_at = record
            
            # Check if already migrated
            existing = await text_collection.find_one({
                "user_id": str(user_id),
                "input_text": input_text,
                "created_at": created_at
            })
            
            if existing:
                continue
            
            # Insert into MongoDB
            doc = {
                "user_id": str(user_id),
                "input_text": input_text,
                "emotion_label": emotion_label,
                "emotion_score": float(emotion_score),
                "confidence": float(confidence),
                "created_at": datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at
            }
            
            await text_collection.insert_one(doc)
            migrated_count += 1
        
        conn.close()
        logger.info(f"Migrated {migrated_count} text analysis records")
        return migrated_count
        
    except Exception as e:
        logger.error(f"Error migrating text analysis: {e}")
        return 0


async def migrate_voice_analysis():
    """Migrate voice analysis data from SQLite to MongoDB"""
    logger.info("Starting voice analysis migration...")
    
    try:
        sqlite_path = os.path.join(os.path.dirname(__file__), 'test.db')
        if not os.path.exists(sqlite_path):
            logger.warning(f"SQLite database not found at {sqlite_path}")
            return 0
        
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='voice_analysis'")
        if not cursor.fetchone():
            logger.warning("voice_analysis table not found in SQLite")
            conn.close()
            return 0
        
        cursor.execute("""
            SELECT user_id, stress_level, intensity, created_at
            FROM voice_analysis
        """)
        
        records = cursor.fetchall()
        migrated_count = 0
        
        for record in records:
            user_id, stress_level, intensity, created_at = record
            
            # Check if already migrated
            existing = await voice_collection.find_one({
                "user_id": str(user_id),
                "created_at": created_at
            })
            
            if existing:
                continue
            
            doc = {
                "user_id": str(user_id),
                "stress_level": stress_level,
                "intensity": float(intensity),
                "confidence": 0.85,  # Default confidence
                "created_at": datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at
            }
            
            await voice_collection.insert_one(doc)
            migrated_count += 1
        
        conn.close()
        logger.info(f"Migrated {migrated_count} voice analysis records")
        return migrated_count
        
    except Exception as e:
        logger.error(f"Error migrating voice analysis: {e}")
        return 0


async def main():
    """Main migration function"""
    logger.info("=" * 60)
    logger.info("Starting SQLite to MongoDB Migration")
    logger.info("=" * 60)
    
    # Check MongoDB connection
    if not await check_connection():
        logger.error("Cannot connect to MongoDB. Please ensure MongoDB is running.")
        return
    
    # Create indexes
    await create_indexes()
    
    # Run migrations
    text_count = await migrate_text_analysis()
    voice_count = await migrate_voice_analysis()
    
    logger.info("=" * 60)
    logger.info("Migration Summary")
    logger.info("=" * 60)
    logger.info(f"Text Analysis Records: {text_count}")
    logger.info(f"Voice Analysis Records: {voice_count}")
    logger.info(f"Total Records Migrated: {text_count + voice_count}")
    logger.info("=" * 60)
    logger.info("Migration completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
