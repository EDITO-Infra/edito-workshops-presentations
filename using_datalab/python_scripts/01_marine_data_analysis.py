# =============================================================================
# EDITO Datalab Tutorial: Marine Biodiversity Data Analysis with Jupyter
# =============================================================================
# This script demonstrates marine biodiversity data analysis using EDITO Datalab
# Perfect for marine researchers getting started with cloud computing

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 1. EXPLORING EDITO DATA CATALOG
# =============================================================================

print("🌊 Welcome to EDITO Datalab Jupyter Service!")
print("=" * 50)

# Connect to EDITO STAC API
stac_endpoint = "https://api.dive.edito.eu/data/"

# Get available collections
try:
    response = requests.get(f"{stac_endpoint}collections")
    collections = response.json()
    
    print(f"✅ Connected to EDITO STAC API")
    print(f"Found {len(collections['collections'])} data collections")
    
    # Show first few collections
    print("\nAvailable data collections:")
    for i, collection in enumerate(collections['collections'][:10]):
        print(f"{i+1:2d}. {collection['id']} - {collection.get('title', 'No title')}")
    
except Exception as e:
    print(f"❌ Error connecting to EDITO API: {e}")

# =============================================================================
# 2. ACCESSING MARINE DATA COLLECTIONS
# =============================================================================

print("\n" + "=" * 50)
print("🌊 ACCESSING MARINE DATA COLLECTIONS")
print("=" * 50)

# Search for different types of marine data
marine_data_types = {
    'biodiversity': 'eurobis-occurrence-data',
    'oceanographic': 'cmems',
    'satellite': 'sentinel',
    'bathymetry': 'bathymetry'
}

for data_type, keyword in marine_data_types.items():
    try:
        # Search for collections containing the keyword
        matching_collections = [col for col in collections['collections'] 
                              if keyword.lower() in col['id'].lower()]
        
        print(f"\n{data_type.title()} collections:")
        for i, col in enumerate(matching_collections[:3]):
            print(f"  {i+1}. {col['id']} - {col.get('title', 'No title')}")
            
    except Exception as e:
        print(f"❌ Error accessing {data_type} data: {e}")

# =============================================================================
# 3. WORKING WITH BIODIVERSITY DATA
# =============================================================================

print("\n" + "=" * 50)
print("🐟 BIODIVERSITY DATA ANALYSIS")
print("=" * 50)

# Create sample marine biodiversity data
np.random.seed(42)
n_records = 1000

biodiversity_data = pd.DataFrame({
    'scientificName': np.random.choice([
        'Gadus morhua', 'Melanogrammus aeglefinus', 'Scomber scombrus',
        'Clupea harengus', 'Pleuronectes platessa', 'Solea solea',
        'Mytilus edulis', 'Crassostrea gigas', 'Pecten maximus',
        'Fucus vesiculosus', 'Laminaria digitata', 'Ulva lactuca',
        'Cancer pagurus', 'Homarus gammarus', 'Carcinus maenas'
    ], n_records),
    'vernacularName': np.random.choice([
        'Atlantic Cod', 'Haddock', 'Atlantic Mackerel',
        'Atlantic Herring', 'European Plaice', 'Common Sole',
        'Blue Mussel', 'Pacific Oyster', 'Great Scallop',
        'Bladder Wrack', 'Oarweed', 'Sea Lettuce',
        'Brown Crab', 'European Lobster', 'Shore Crab'
    ], n_records),
    'decimalLatitude': np.random.uniform(50, 60, n_records),
    'decimalLongitude': np.random.uniform(0, 10, n_records),
    'eventDate': pd.date_range('2020-01-01', '2024-01-01', periods=n_records),
    'minimumDepthInMeters': np.random.uniform(5, 200, n_records),
    'individualCount': np.random.randint(1, 10, n_records)
})

print(f"✅ Created sample marine biodiversity dataset with {len(biodiversity_data)} records")

# Species analysis
species_counts = biodiversity_data['scientificName'].value_counts()
print(f"\nTop 5 marine species found:")
print(species_counts.head())

# =============================================================================
# 4. OCEANOGRAPHIC DATA ANALYSIS
# =============================================================================

print("\n" + "=" * 50)
print("🌊 OCEANOGRAPHIC DATA ANALYSIS")
print("=" * 50)

# Create sample oceanographic data
oceanographic_data = pd.DataFrame({
    'longitude': np.random.uniform(-10, 10, 500),
    'latitude': np.random.uniform(50, 60, 500),
    'sst': np.random.normal(12, 2, 500),  # Sea surface temperature
    'salinity': np.random.normal(35, 1, 500),  # Salinity
    'u_velocity': np.random.normal(0, 0.5, 500),  # Eastward velocity
    'v_velocity': np.random.normal(0, 0.5, 500),  # Northward velocity
    'depth': np.random.uniform(10, 200, 500),
    'month': np.random.randint(1, 13, 500)
})

# Calculate current speed
oceanographic_data['current_speed'] = np.sqrt(
    oceanographic_data['u_velocity']**2 + oceanographic_data['v_velocity']**2
)

print(f"✅ Created oceanographic dataset with {len(oceanographic_data)} records")
print(f"Temperature range: {oceanographic_data['sst'].min():.1f} - {oceanographic_data['sst'].max():.1f} °C")
print(f"Salinity range: {oceanographic_data['salinity'].min():.1f} - {oceanographic_data['salinity'].max():.1f} PSU")

# =============================================================================
# 5. SATELLITE DATA ANALYSIS
# =============================================================================

print("\n" + "=" * 50)
print("🛰️ SATELLITE DATA ANALYSIS")
print("=" * 50)

# Create sample satellite data (e.g., chlorophyll-a, sea surface temperature)
satellite_data = pd.DataFrame({
    'longitude': np.random.uniform(-10, 10, 300),
    'latitude': np.random.uniform(50, 60, 300),
    'chlorophyll_a': np.random.exponential(1, 300),  # Chlorophyll-a concentration
    'sst_satellite': np.random.normal(12, 1.5, 300),  # Satellite SST
    'turbidity': np.random.exponential(0.5, 300),  # Water turbidity
    'date': pd.date_range('2024-01-01', '2024-12-31', periods=300)
})

print(f"✅ Created satellite dataset with {len(satellite_data)} records")
print(f"Chlorophyll-a range: {satellite_data['chlorophyll_a'].min():.2f} - {satellite_data['chlorophyll_a'].max():.2f} mg/m³")

# =============================================================================
# 6. DATA VISUALIZATION
# =============================================================================

print("\n" + "=" * 50)
print("📊 DATA VISUALIZATION")
print("=" * 50)

# Create comprehensive visualizations
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Marine Data Analysis Dashboard', fontsize=16)

# 1. Marine biodiversity species distribution
species_counts.head().plot(kind='bar', ax=axes[0,0], color='skyblue')
axes[0,0].set_title('Marine Species Distribution')
axes[0,0].set_xlabel('Species')
axes[0,0].set_ylabel('Count')
axes[0,0].tick_params(axis='x', rotation=45)

# 2. Spatial distribution of marine biodiversity
scatter1 = axes[0,1].scatter(biodiversity_data['decimalLongitude'], 
                            biodiversity_data['decimalLatitude'], 
                            c=biodiversity_data['individualCount'], 
                            cmap='viridis', alpha=0.6)
axes[0,1].set_title('Marine Biodiversity Spatial Distribution')
axes[0,1].set_xlabel('Longitude')
axes[0,1].set_ylabel('Latitude')
plt.colorbar(scatter1, ax=axes[0,1], label='Individual Count')

# 3. Oceanographic variables correlation
ocean_vars = oceanographic_data[['sst', 'salinity', 'current_speed', 'depth']]
correlation_matrix = ocean_vars.corr()
im = axes[0,2].imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)
axes[0,2].set_title('Oceanographic Variables Correlation')
axes[0,2].set_xticks(range(len(correlation_matrix.columns)))
axes[0,2].set_yticks(range(len(correlation_matrix.columns)))
axes[0,2].set_xticklabels(correlation_matrix.columns, rotation=45)
axes[0,2].set_yticklabels(correlation_matrix.columns)
plt.colorbar(im, ax=axes[0,2])

# 4. Sea surface temperature distribution
axes[1,0].hist(oceanographic_data['sst'], bins=20, color='lightcoral', alpha=0.7)
axes[1,0].set_title('Sea Surface Temperature Distribution')
axes[1,0].set_xlabel('Temperature (°C)')
axes[1,0].set_ylabel('Frequency')

# 5. Chlorophyll-a vs SST
scatter2 = axes[1,1].scatter(satellite_data['sst_satellite'], 
                            satellite_data['chlorophyll_a'], 
                            c=satellite_data['turbidity'], 
                            cmap='plasma', alpha=0.6)
axes[1,1].set_title('Chlorophyll-a vs SST')
axes[1,1].set_xlabel('Sea Surface Temperature (°C)')
axes[1,1].set_ylabel('Chlorophyll-a (mg/m³)')
plt.colorbar(scatter2, ax=axes[1,1], label='Turbidity')

# 6. Temporal trends
monthly_sst = oceanographic_data.groupby('month')['sst'].mean()
monthly_sst.plot(kind='line', ax=axes[1,2], marker='o', color='green')
axes[1,2].set_title('Seasonal SST Trends')
axes[1,2].set_xlabel('Month')
axes[1,2].set_ylabel('Mean SST (°C)')
axes[1,2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# =============================================================================
# 7. MACHINE LEARNING FOR MARINE DATA
# =============================================================================

print("\n" + "=" * 50)
print("🤖 MACHINE LEARNING FOR MARINE DATA")
print("=" * 50)

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Example: Predict chlorophyll-a from environmental variables
# Merge satellite and oceanographic data
merged_data = pd.merge(
    satellite_data[['longitude', 'latitude', 'chlorophyll_a', 'sst_satellite']],
    oceanographic_data[['longitude', 'latitude', 'sst', 'salinity', 'depth']],
    on=['longitude', 'latitude'],
    how='inner'
)

if len(merged_data) > 50:  # Ensure we have enough data
    # Prepare features and target
    features = ['sst', 'salinity', 'depth', 'sst_satellite']
    X = merged_data[features]
    y = merged_data['chlorophyll_a']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Chlorophyll-a Prediction Model:")
    print(f"R² Score: {r2:.3f}")
    print(f"RMSE: {np.sqrt(mse):.3f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nFeature Importance:")
    print(feature_importance)
    
    # Visualize predictions vs actual
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Chlorophyll-a')
    plt.ylabel('Predicted Chlorophyll-a')
    plt.title('Model Predictions vs Actual Values')
    plt.show()

# =============================================================================
# 8. DATA EXPORT AND SAVING
# =============================================================================

print("\n" + "=" * 50)
print("💾 SAVING YOUR WORK")
print("=" * 50)

# Save all datasets
biodiversity_data.to_csv('biodiversity_analysis.csv', index=False)
oceanographic_data.to_csv('oceanographic_analysis.csv', index=False)
satellite_data.to_csv('satellite_analysis.csv', index=False)

print("✅ Data saved:")
print("- marine_biodiversity_analysis.csv")
print("- oceanographic_analysis.csv")
print("- satellite_analysis.csv")

# Save as Parquet (more efficient)
biodiversity_data.to_parquet('marine_biodiversity_analysis.parquet', index=False)
oceanographic_data.to_parquet('oceanographic_analysis.parquet', index=False)
satellite_data.to_parquet('satellite_analysis.parquet', index=False)

print("✅ Data saved as Parquet:")
print("- marine_biodiversity_analysis.parquet")
print("- oceanographic_analysis.parquet")
print("- satellite_analysis.parquet")

# =============================================================================
# 9. NEXT STEPS
# =============================================================================

print("\n" + "=" * 50)
print("🚀 NEXT STEPS")
print("=" * 50)

print("1. 📊 Try the RStudio service for R-based analysis")
print("2. 🔧 Use VSCode for larger projects")
print("3. 🌊 Access real environmental data from EDITO")
print("4. 🤝 Learn about data sharing and collaboration")
print("5. 📚 Check out the R Markdown tutorial")

print("\n🔗 RESOURCES")
print("=" * 50)
print("• EDITO Datalab: https://datalab.dive.edito.eu/")
print("• Personal Storage: https://datalab.dive.edito.eu/account/storage")
print("• EDITO Tutorials: https://dive.edito.eu/training")
print("• Data API Docs: https://pub.pages.mercator-ocean.fr/edito-infra/edito-tutorials-content/#/interactWithTheDataAPI")

print("\n✅ Marine biodiversity data analysis tutorial completed!")
print("Ready to explore more EDITO features! 🌊")
