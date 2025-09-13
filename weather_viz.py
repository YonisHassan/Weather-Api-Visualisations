import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# Weather API setup - using Berlin coordinates by default
API_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 52.52
LONGITUDE = 13.41

def get_weather_data(lat=LATITUDE, lon=LONGITUDE):
    """Fetch temperature data from Open-Meteo API"""
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'temperature_2m',
        'models': 'jma_seamless'
    }
    
    response = requests.get(API_URL, params=params)
    return response.json()

def process_data(data):
    """Convert API response to DataFrame"""
    time_data = data['hourly']['time']
    temp_data = data['hourly']['temperature_2m']
    
    df = pd.DataFrame({
        'time': pd.to_datetime(time_data),
        'temperature': temp_data
    })
    
    df['day'] = df['time'].dt.day
    df['hour'] = df['time'].dt.hour
    return df

def plot_temperature_line(df):
    """Basic line plot of temperature over time"""
    plt.figure(figsize=(12, 6))
    plt.plot(df['time'], df['temperature'], linewidth=2)
    plt.title('Temperature Forecast')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_3d_surface(df):
    """3D surface plot showing temperature patterns"""
    # Create pivot table for surface plot
    pivot = df.pivot(index='hour', columns='day', values='temperature')
    pivot = pivot.fillna(method='ffill').fillna(method='bfill')
    
    X, Y = np.meshgrid(pivot.columns, pivot.index)
    Z = pivot.values
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.8)
    ax.set_xlabel('Day')
    ax.set_ylabel('Hour')
    ax.set_zlabel('Temperature (°C)')
    ax.set_title('Temperature Surface')
    
    fig.colorbar(surf)
    plt.show()

def analyze_temperature_gradients(df):
    """Calculate and visualize temperature gradients"""
    pivot = df.pivot(index='hour', columns='day', values='temperature')
    pivot = pivot.fillna(method='ffill').fillna(method='bfill')
    
    X, Y = np.meshgrid(pivot.columns, pivot.index)
    Z = pivot.values
    
    # Calculate gradients
    grad_y, grad_x = np.gradient(Z)
    grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    
    print("Temperature Gradient Stats:")
    print(f"Daily change - Min: {grad_x.min():.2f}, Max: {grad_x.max():.2f} °C/day")
    print(f"Hourly change - Min: {grad_y.min():.2f}, Max: {grad_y.max():.2f} °C/hour")
    
    # Plot gradients
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Temperature surface
    im1 = axes[0,0].contourf(X, Y, Z, levels=15, cmap='coolwarm')
    axes[0,0].set_title('Temperature')
    plt.colorbar(im1, ax=axes[0,0])
    
    # Daily gradient
    im2 = axes[0,1].contourf(X, Y, grad_x, levels=15, cmap='RdBu_r')
    axes[0,1].set_title('Daily Change')
    plt.colorbar(im2, ax=axes[0,1])
    
    # Hourly gradient  
    im3 = axes[1,0].contourf(X, Y, grad_y, levels=15, cmap='RdBu_r')
    axes[1,0].set_title('Hourly Change')
    plt.colorbar(im3, ax=axes[1,0])
    
    # Gradient magnitude
    im4 = axes[1,1].contourf(X, Y, grad_magnitude, levels=15, cmap='plasma')
    axes[1,1].set_title('Change Magnitude')
    plt.colorbar(im4, ax=axes[1,1])
    
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == "__main__":
    print("Fetching weather data...")
    data = get_weather_data()
    df = process_data(data)
    
    print(f"Got {len(df)} hours of temperature data")
    
    # Create visualizations
    plot_temperature_line(df)
    plot_3d_surface(df) 
    analyze_temperature_gradients(df)