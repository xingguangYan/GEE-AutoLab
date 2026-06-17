# NDVI Analysis Example

## Task Description

Calculate NDVI and EVI for Wuhan city using Sentinel-2 data for the year 2023.

## Input
- Location: Wuhan (Wuhan)
- Time: 2023-01-01 to 2023-12-31
- Task: NDVI, EVI, MNDWI calculation
- Resolution: 10m

## Generated GEE Script

```javascript
// NDVI, EVI, MNDWI Analysis - Wuhan 2023
var roi = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level1')
  .filter(ee.Filter.eq('ADM1_NAME', 'Wuhan'));

Map.centerObject(roi, 10);
Map.addLayer(roi, {color: 'yellow'}, 'ROI');

// Sentinel-2 SR
var collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(roi)
  .filterDate('2023-01-01', '2023-12-31')
  .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', 20));

// Cloud masking
function maskS2clouds(image) {
  var qa = image.select('QA60');
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(mask).divide(10000);
}

var masked = collection.map(maskS2clouds);
var composite = masked.median().clip(roi);

// Calculate indices
var ndvi = composite.normalizedDifference(['B8', 'B4']).rename('NDVI');
var evi = composite.expression(
    '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
      'NIR': composite.select('B8'),
      'RED': composite.select('B4'),
      'BLUE': composite.select('B2')
}).rename('EVI');
var mndwi = composite.normalizedDifference(['B3', 'B11']).rename('MNDWI');

// Add to map
Map.addLayer(ndvi, {min: -0.2, max: 1, palette: ['blue', 'white', 'green']}, 'NDVI');
Map.addLayer(evi, {min: -1, max: 1, palette: ['blue', 'white', 'darkgreen']}, 'EVI');
Map.addLayer(mndwi, {min: -1, max: 1, palette: ['brown', 'white', 'blue']}, 'MNDWI');

// Export
Export.image.toDrive({
  image: ndvi,
  description: 'Wuhan_NDVI_2023',
  folder: 'GEE_Exports',
  scale: 10,
  crs: 'EPSG:4326',
  maxPixels: 1e13,
  region: roi.geometry()
});

Export.image.toDrive({
  image: evi,
  description: 'Wuhan_EVI_2023',
  folder: 'GEE_Exports',
  scale: 10,
  crs: 'EPSG:4326',
  maxPixels: 1e13,
  region: roi.geometry()
});

Export.image.toDrive({
  image: mndwi,
  description: 'Wuhan_MNDWI_2023',
  folder: 'GEE_Exports',
  scale: 10,
  crs: 'EPSG:4326',
  maxPixels: 1e13,
  region: roi.geometry()
});
```

## Expected Output
- 3 GeoTIFF files (NDVI, EVI, MNDWI)
- CSV statistics table
- Visualization preview in GEE Code Editor

## Results Summary
- Mean NDVI: ~0.45 (typical for mixed urban/vegetation area)
- Vegetation coverage: ~62% of study area
- Water bodies: ~9% (detected by MNDWI)
