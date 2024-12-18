import pandas as pd
import requests
import time
from tqdm import tqdm

API_KEY = 'AIzaSyBTvrWCaYZLZjdTYzjaT7Z2-wrTqxNKlyk'

def reverse_geocode(lng, lat):
    """Find the first restaurant within 10m radius"""
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=10&type=restaurant&key={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json().get('results', [])
        
        if results:
            place = results[0]  # Get first restaurant
            return {
                'name': place.get('name', ''),
                'category': ', '.join(place.get('types', [])),
                'rating': str(place.get('rating', '')),
                'address': place.get('vicinity', ''),
                'latitude': lat,
                'longitude': lng
            }
    except Exception as e:
        print(f"Error for coordinates {lat},{lng}: {str(e)}")
    
    return {
        'name': '',
        'category': '',
        'rating': '',
        'address': '',
        'latitude': lat,
        'longitude': lng
    }

def main():
    # Read input CSV
    df = pd.read_csv('mapdata.csv')
    
    # Initialize list to store restaurant data
    restaurant_data = []
    count = 0
    for _, row in tqdm(df.iterrows(), total=len(df)):
        restaurant_info = reverse_geocode(row['ycoord'], row['xcoord'])
        restaurant_data.append(restaurant_info)
        time.sleep(0.1)  # Rate limiting
        count += 1
        if count == 15:
            break
        
    
    result_df = pd.DataFrame(restaurant_data)
    
    # Save to new CSV
    result_df.to_csv('restaurants.csv', index=False)
    print("Restaurant data saved to restaurants.csv")

if __name__ == "__main__":
    main()








