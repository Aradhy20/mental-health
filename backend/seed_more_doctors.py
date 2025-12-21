"""
Seed More Doctors Script
Adds comprehensive doctor data for testing nearby search
"""

import os
import sys
import random

# Add parent directory to path to allow importing from shared
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from shared.database import engine

def seed_more_doctors():
    """Seed database with more doctors"""
    print("🚀 Seeding more doctors...")
    
    doctors_data = [
        # Sukhli (User requested location - using dummy coords near a city for now, or 0,0 if unknown)
        # Assuming Sukhli might be in India (common name structure). I'll place it near Nagpur/Central India just in case, or arbitrary.
        # Let's put it near a generic "User Home" location if we had one.
        ('Dr. Priya Sharma', 'Psychiatrist', 'priya.s@example.com', '999-001-0001', '12 Sukhli Main Road, Sukhli', 21.1458, 79.0882, 4.9, 8),
        
        # Major Hubs
        ('Dr. Alan Grant', 'Therapist', 'alan.g@example.com', '555-0201', '101 Market St, San Francisco, CA', 37.7749, -122.4194, 4.8, 15),
        ('Dr. Ellie Sattler', 'Clinical Psychologist', 'ellie.s@example.com', '555-0202', '202 Broadway, Seattle, WA', 47.6062, -122.3321, 4.9, 12),
        ('Dr. Ian Malcolm', 'Psychiatrist', 'ian.m@example.com', '555-0203', '303 Oxford St, London, UK', 51.5074, -0.1278, 4.7, 25),
        
        # India (Student/Corporate hubs)
        ('Dr. Rajesh Koothrappali', 'Psychiatrist', 'raj.k@example.com', '91-999-001', 'Electronic City, Bangalore', 12.9716, 77.5946, 4.5, 6),
        ('Dr. Anjali Gupta', 'Counselor', 'anjali.g@example.com', '91-999-002', 'Hitech City, Hyderabad', 17.3850, 78.4867, 4.8, 9),
        ('Dr. Vikram Singh', 'Therapist', 'vikram.s@example.com', '91-999-003', 'Connaught Place, New Delhi', 28.6139, 77.2090, 4.6, 11),
        
        # New York
        ('Dr. Frasier Crane', 'Psychiatrist', 'frasier.c@example.com', '555-0301', '1900 Broadway, New York, NY', 40.7812, -73.9814, 4.4, 30),
        ('Dr. Niles Crane', 'Psychiatrist', 'niles.c@example.com', '555-0302', 'The Montana, New York, NY', 40.7820, -73.9800, 4.9, 28)
    ]
    
    # Generate 40 random doctors around a central point (e.g., NY) for testing density
    base_lat, base_lng = 40.7128, -74.0060
    
    with engine.connect() as conn:
        # Insert specific doctors
        for doc in doctors_data:
            conn.execute(text("""
                INSERT INTO doctors (name, specialization, email, phone, address, latitude, longitude, rating, years_experience)
                VALUES (:name, :spec, :email, :phone, :addr, :lat, :lng, :rating, :exp)
            """), {
                "name": doc[0], "spec": doc[1], "email": doc[2], "phone": doc[3], 
                "addr": doc[4], "lat": doc[5], "lng": doc[6], "rating": doc[7], "exp": doc[8]
            })
            
        print("✅ Specific doctors added.")

        # Insert random doctors
        import random
        specializations = ['Psychiatrist', 'Therapist', 'Counselor', 'Clinical Psychologist']
        
        for i in range(40):
            # Random offset
            lat_offset = (random.random() - 0.5) * 0.5 # +/- 0.25 degrees
            lng_offset = (random.random() - 0.5) * 0.5
            
            conn.execute(text("""
                INSERT INTO doctors (name, specialization, email, phone, address, latitude, longitude, rating, years_experience)
                VALUES (:name, :spec, :email, :phone, :addr, :lat, :lng, :rating, :exp)
            """), {
                "name": f"Dr. Random {i}", 
                "spec": random.choice(specializations), 
                "email": f"random.{i}@example.com", 
                "phone": "555-0000", 
                "addr": f"Random Loc {i}, NY", 
                "lat": base_lat + lat_offset, 
                "lng": base_lng + lng_offset, 
                "rating": round(3.5 + random.random() * 1.5, 1), 
                "exp": random.randint(1, 40)
            })
            
        conn.commit()
        print("✅ Random doctors added.")
        print("\n✅ Seeding complete!")

if __name__ == "__main__":
    try:
        seed_more_doctors()
    except Exception as e:
        print(f"❌ Error: {e}")
