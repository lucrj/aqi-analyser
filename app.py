import streamlit as st 
import requests 
import pandas as pd 
import os
st.title ("AQI analyser")


api_key = os.getenv("API_KEY")

cities_input = st.text_input("Enter city (comma separated):","Bangalore,Delhi,Mumbai")

def get_coordinates(city):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response = requests.get(geo_url).json()
    if response:
        return response [0]['lat'],response[0]['lon']
    return None,None

def aqi_status(aqi):
    if aqi == 1:
        return "Good","green"
    elif aqi == 2:
        return "fair","yellow"
    elif aqi == 3:
        return "moderate","orange"
    elif aqi == 4:
        return "poor","red"
    else : 
        return "very poor","purple"
    
def get_aqi(lat,lon):
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    return requests.get(aqi_url).json()

if st.button("GET AQI"):
    cities=[c.strip() for c in cities_input.split(",") ]
    
    results = []
    map_points = []

    for city in cities:
        lat,lon = get_coordinates(city)

        if lat is not None:
            data = get_aqi(lat,lon)
            aqi = data ['list'][0]['main']['aqi']

            status,color = aqi_status (aqi)
            
            
            results.append({
                    "City": city,
                    "AQI": aqi,
                    "Status": status
                })

            map_points.append({
                    "lat": lat,
                    "lon": lon
                })
        
    if results :
        df = pd.DataFrame(results)
        st.subheader("📊 AQI Comparison")
        st.dataframe(df)
        st.bar_chart(df.set_index("City")["AQI"])

        map_df = pd.DataFrame(map_points)
        st.subheader("📍 Cities Map")
        st.map(map_df)
    else:
        st.error("Cities not found")

