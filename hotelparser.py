import csv
import requests
from io import StringIO

experience_scores = {
    "Excellent": 5,
    "Very good": 4,
    "Average": 3,
    "Poor": 2,
    "Terrible": 1,
    "Bad": 0
}

def selection_sort(data):
    for i in range(len(data)):
        minpos = i
        for j in range(i+1, len(data)):
            
            if data[j]['hotel_price'] < data[minpos]['hotel_price']:
                minpos = j
            
            elif data[j]['hotel_price'] == data[minpos]['hotel_price'] and experience_scores[data[j]['hotel_experience']] < experience_scores[data[minpos]['hotel_experience']]:
                minpos = j
                
        data[minpos], data[i] = data[i], data[minpos]


def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1

        while j >= 0 and key['hotel_price'] < data[j]['hotel_price']:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key

        for k in range(1, len(data)):
            key = data[k]
            j = k - 1
            while j >= 0 and data[j]['hotel_price'] == key['hotel_price'] and experience_scores[data[j]['hotel_experience']] < experience_scores[key['hotel_experience']]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key


def load_and_process_data(url):
    hotels = []
    response = requests.get(url)
    response_text = StringIO(response.text)
    reader = csv.DictReader(response_text)
    for row in reader:
        amenities = eval(row['amenities']) if row['amenities'] else []
        has_wifi = 'Free High Speed Internet (WiFi)' in amenities 
        hotel_price = float(row['price']) if row['price'] else 300
        hotel_rating = float(row['hotel_rating']) if 'hotel_rating' in row and row['hotel_rating'] else 0
        hotel_experience = row['hotel_experience'] if row['hotel_experience'] in experience_scores else 'Bad'
        hotels.append({
            'hotel_name': row['hotel_name'],
            'hotel_experience': hotel_experience,
            'hotel_price': hotel_price,
            'has_wifi': has_wifi,
            'hotel_rating': hotel_rating   
        })
    return hotels



file_path = "https://raw.githubusercontent.com/sachinnpraburaj/Intelligent-Travel-Recommendation-System/master/tripadvisor_hotel_output/hotel_info_dedup.csv"
hotels1 = load_and_process_data(file_path)
hotels2 = hotels1.copy()
