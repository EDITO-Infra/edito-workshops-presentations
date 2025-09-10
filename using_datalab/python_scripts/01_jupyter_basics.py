# =============================================================================
# EDITO Datalab Tutorial: Jupyter Service Basics
# =============================================================================
# This script demonstrates basic usage of Jupyter service on EDITO Datalab
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
# 2. ACCESSING BIODIVERSITY DATA (Perfect for Fish Research!)
# =============================================================================

print("\n" + "=" * 50)
print("🐟 ACCESSING FISH AND BIODIVERSITY DATA")
print("=" * 50)

# Search for biodiversity data
try:
    # Get EUROBIS occurrence data collection
    biodiversity_url = f"{stac_endpoint}collections/eurobis-occurrence-data"
    response = requests.get(biodiversity_url)
    collection_info = response.json()
    
    print(f"✅ Found biodiversity collection: {collection_info['title']}")
    print(f"Description: {collection_info.get('description', 'No description')}")
    
    # Get some items from the collection
    items_url = f"{biodiversity_url}/items?limit=5"
    response = requests.get(items_url)
    items = response.json()
    
    print(f"\nFound {items['context']['returned']} sample items")
    
except Exception as e:
    print(f"❌ Error accessing biodiversity data: {e}")

# =============================================================================
# 3. READING ARCO DATA (Analysis Ready Cloud Optimized)
# =============================================================================

print("\n" + "=" * 50)
print("📊 READING ARCO DATA (Parquet Format)")
print("=" * 50)

# Example: Read EUROBIS occurrence data in Parquet format
parquet_url = "https://s3.waw3-1.cloudferro.com/emodnet/biology/eurobis_occurrence_data/eurobis_occurrences_geoparquet_2024-10-01.parquet"

try:
    # Read a sample of the data using pandas
    # Note: This is a large dataset, so we'll read just a sample
    print("📥 Reading sample data from EDITO data lake...")
    
    # For demonstration, we'll create sample data that mimics the structure
    # In practice, you would use: df = pd.read_parquet(parquet_url)
    
    # Create sample fish occurrence data
    np.random.seed(42)
    n_records = 1000
    
    sample_data = pd.DataFrame({
        'scientificName': np.random.choice([
            'Gadus morhua', 'Melanogrammus aeglefinus', 'Scomber scombrus',
            'Clupea harengus', 'Pleuronectes platessa', 'Solea solea'
        ], n_records),
        'vernacularName': np.random.choice([
            'Atlantic Cod', 'Haddock', 'Atlantic Mackerel',
            'Atlantic Herring', 'European Plaice', 'Common Sole'
        ], n_records),
        'decimalLatitude': np.random.uniform(50, 60, n_records),
        'decimalLongitude': np.random.uniform(0, 10, n_records),
        'eventDate': pd.date_range('2020-01-01', '2024-01-01', periods=n_records),
        'minimumDepthInMeters': np.random.uniform(5, 200, n_records),
        'individualCount': np.random.randint(1, 10, n_records)
    })
    
    print(f"✅ Created sample dataset with {len(sample_data)} records")
    print("\nData structure:")
    print(sample_data.info())
    
    print("\nFirst few records:")
    print(sample_data.head())
    
except Exception as e:
    print(f"❌ Error reading data: {e}")

# =============================================================================
# 4. FISH TRACKING ANALYSIS
# =============================================================================

print("\n" + "=" * 50)
print("🐟 FISH TRACKING ANALYSIS")
print("=" * 50)

# Filter for fish species
fish_data = sample_data[sample_data['scientificName'].str.contains('Gadus|Melanogrammus|Scomber|Clupea|Pleuronectes|Solea', case=False, na=False)]

print(f"Found {len(fish_data)} fish occurrence records")

if len(fish_data) > 0:
    # Species summary
    species_counts = fish_data['scientificName'].value_counts()
    print("\nFish species found:")
    print(species_counts)
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Fish Occurrence Analysis', fontsize=16)
    
    # 1. Species distribution
    species_counts.plot(kind='bar', ax=axes[0,0], color='skyblue')
    axes[0,0].set_title('Species Distribution')
    axes[0,0].set_xlabel('Species')
    axes[0,0].set_ylabel('Count')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 2. Spatial distribution
    axes[0,1].scatter(fish_data['decimalLongitude'], fish_data['decimalLatitude'], 
                     c=fish_data['individualCount'], cmap='viridis', alpha=0.6)
    axes[0,1].set_title('Spatial Distribution')
    axes[0,1].set_xlabel('Longitude')
    axes[0,1].set_ylabel('Latitude')
    
    # 3. Depth distribution
    axes[1,0].hist(fish_data['minimumDepthInMeters'], bins=20, color='lightcoral', alpha=0.7)
    axes[1,0].set_title('Depth Distribution')
    axes[1,0].set_xlabel('Depth (meters)')
    axes[1,0].set_ylabel('Frequency')
    
    # 4. Temporal distribution
    fish_data['year'] = fish_data['eventDate'].dt.year
    yearly_counts = fish_data['year'].value_counts().sort_index()
    yearly_counts.plot(kind='line', ax=axes[1,1], marker='o', color='green')
    axes[1,1].set_title('Temporal Distribution')
    axes[1,1].set_xlabel('Year')
    axes[1,1].set_ylabel('Count')
    
    plt.tight_layout()
    plt.show()
    
    # Summary statistics
    print(f"\nSummary Statistics:")
    print(f"Average depth: {fish_data['minimumDepthInMeters'].mean():.1f} meters")
    print(f"Depth range: {fish_data['minimumDepthInMeters'].min():.1f} - {fish_data['minimumDepthInMeters'].max():.1f} meters")
    print(f"Latitude range: {fish_data['decimalLatitude'].min():.2f} - {fish_data['decimalLatitude'].max():.2f}")
    print(f"Longitude range: {fish_data['decimalLongitude'].min():.2f} - {fish_data['decimalLongitude'].max():.2f}")

# =============================================================================
# 5. ENVIRONMENTAL DATA INTEGRATION
# =============================================================================

print("\n" + "=" * 50)
print("🌊 ENVIRONMENTAL DATA INTEGRATION")
print("=" * 50)

# Search for oceanographic data that could be used for fish habitat modeling
try:
    # Look for CMEMS (Copernicus Marine) data
    cmems_collections = [col for col in collections['collections'] 
                        if 'cmems' in col['id'].lower() or 'ocean' in col['id'].lower()]
    
    print(f"Found {len(cmems_collections)} oceanographic data collections:")
    for i, col in enumerate(cmems_collections[:5]):
        print(f"{i+1}. {col['id']} - {col.get('title', 'No title')}")
    
    print("\nThese collections contain environmental data like:")
    print("- Sea surface temperature")
    print("- Salinity")
    print("- Currents")
    print("- Sea level")
    print("- Perfect for fish habitat modeling!")
    
except Exception as e:
    print(f"❌ Error accessing environmental data: {e}")

# =============================================================================
# 6. MACHINE LEARNING EXAMPLE
# =============================================================================

print("\n" + "=" * 50)
print("🤖 MACHINE LEARNING FOR FISH HABITAT MODELING")
print("=" * 50)

# Simple example of using environmental data for fish habitat modeling
if len(fish_data) > 0:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
    
    # Create features for habitat modeling
    # In practice, you would use real environmental data
    np.random.seed(42)
    
    # Simulate environmental variables
    fish_data['temperature'] = np.random.normal(10, 3, len(fish_data))
    fish_data['salinity'] = np.random.normal(35, 1, len(fish_data))
    fish_data['current_speed'] = np.random.exponential(0.5, len(fish_data))
    
    # Create habitat suitability classes (simplified)
    fish_data['habitat_suitability'] = (
        (fish_data['temperature'] > 8) & 
        (fish_data['temperature'] < 15) &
        (fish_data['salinity'] > 34) &
        (fish_data['salinity'] < 36) &
        (fish_data['minimumDepthInMeters'] > 20) &
        (fish_data['minimumDepthInMeters'] < 150)
    ).astype(int)
    
    # Prepare features for modeling
    features = ['decimalLatitude', 'decimalLongitude', 'minimumDepthInMeters', 
                'temperature', 'salinity', 'current_speed']
    X = fish_data[features]
    y = fish_data['habitat_suitability']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate model
    print("Habitat Suitability Model Results:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    # Visualize feature importance
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_importance, x='importance', y='feature')
    plt.title('Feature Importance for Fish Habitat Suitability')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.show()

# =============================================================================
# 7. SAVING RESULTS
# =============================================================================

print("\n" + "=" * 50)
print("💾 SAVING YOUR WORK")
print("=" * 50)

# Save results to files
if len(fish_data) > 0:
    # Save as CSV
    fish_data.to_csv('fish_analysis_results.csv', index=False)
    print("✅ Results saved to fish_analysis_results.csv")
    
    # Save as Parquet (more efficient)
    fish_data.to_parquet('fish_analysis_results.parquet', index=False)
    print("✅ Results saved to fish_analysis_results.parquet")
    
    # Save summary statistics
    summary_stats = {
        'total_records': len(fish_data),
        'species_count': fish_data['scientificName'].nunique(),
        'avg_depth': fish_data['minimumDepthInMeters'].mean(),
        'depth_range': [fish_data['minimumDepthInMeters'].min(), 
                       fish_data['minimumDepthInMeters'].max()],
        'lat_range': [fish_data['decimalLatitude'].min(), 
                     fish_data['decimalLatitude'].max()],
        'lon_range': [fish_data['decimalLongitude'].min(), 
                     fish_data['decimalLongitude'].max()]
    }
    
    with open('analysis_summary.json', 'w') as f:
        json.dump(summary_stats, f, indent=2, default=str)
    
    print("✅ Summary statistics saved to analysis_summary.json")

# =============================================================================
# 8. NEXT STEPS
# =============================================================================

print("\n" + "=" * 50)
print("🚀 NEXT STEPS")
print("=" * 50)

print("1. 📊 Try the personal storage tutorial")
print("2. 🐍 Explore more Python libraries for fish tracking")
print("3. 🔧 Use VSCode for larger projects")
print("4. 🌊 Access real environmental data from EDITO")
print("5. 🤝 Share your work with collaborators")

print("\n✅ Jupyter basics tutorial completed!")
print("Ready to explore more EDITO features!")
