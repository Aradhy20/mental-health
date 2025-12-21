import math
from typing import Tuple

class GeoLocationService:
    def __init__(self):
        pass
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the distance between two points using the haversine formula
        Returns distance in kilometers
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r
    
    def find_nearby_doctors(self, doctors: list, user_lat: float, user_lon: float, max_distance: float = 50.0) -> list:
        """
        Find doctors within a certain distance of the user
        """
        nearby_doctors = []
        
        for doctor in doctors:
            distance = self.calculate_distance(
                user_lat, user_lon, 
                doctor.latitude, doctor.longitude
            )
            
            # Only include doctors within max_distance
            if distance <= max_distance:
                doctor_with_distance = doctor.copy()
                doctor_with_distance["distance"] = round(distance, 2)
                nearby_doctors.append(doctor_with_distance)
        
        # Sort by distance
        nearby_doctors.sort(key=lambda x: x["distance"])
        
        return nearby_doctors
    
    def is_within_radius(self, lat1: float, lon1: float, lat2: float, lon2: float, radius: float) -> bool:
        """
        Check if a point is within a certain radius of another point
        """
        distance = self.calculate_distance(lat1, lon1, lat2, lon2)
        return distance <= radius

# Global instance
geo_service = GeoLocationService()