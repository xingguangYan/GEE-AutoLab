# Change Detection Example

## Task Description

Detect forest change in Yunnan Province using LandTrendr and Landsat time series.

## Input
- Location: Yunnan Province
- Time: 2018 to 2023
- Task: Forest disturbance detection
- Method: LandTrendr

## Generated GEE Script

```javascript
// Forest Change Detection - Yunnan 2018-2023
var roi = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level1')
  .filter(ee.Filter.eq('ADM1_NAME', 'Yunnan'));

Map.centerObject(roi, 7);

// Landsat time series
var collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
  .filterBounds(roi)
  .filterDate('2018-01-01', '2023-12-31')
  .filter(ee.Filter.lte('CLOUD_COVER', 20));

function maskClouds(image) {
  var qa = image.select('QA_PIXEL');
  var cloudBitMask = 1 << 3;
  var cloudShadowBitMask = 1 << 4;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cloudShadowBitMask).eq(0));
  return image.updateMask(mask);
}

var masked = collection.map(maskClouds);

// Method 1: Bi-temporal change detection
var before = masked.filterDate('2018-01-01', '2018-12-31').median();
var after = masked.filterDate('2023-01-01', '2023-12-31').median();

var ndviBefore = before.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI_before');
var ndviAfter = after.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI_after');
var ndviDiff = ndviAfter.subtract(ndviBefore).rename('NDVI_diff');

// Forest loss detection (NDVI decrease > 0.2)
var forestLoss = ndviDiff.lt(-0.2).selfMask().rename('Forest_Loss');

Map.addLayer(ndviBefore, {min: 0, max: 1, palette: ['yellow', 'green']}, 'NDVI 2018');
Map.addLayer(ndviAfter, {min: 0, max: 1, palette: ['yellow', 'green']}, 'NDVI 2023');
Map.addLayer(ndviDiff, {min: -0.3, max: 0.3, palette: ['red', 'white', 'green']}, 'NDVI Change');
Map.addLayer(forestLoss, {palette: 'red'}, 'Forest Loss');

// Method 2: NBR-based burned area detection
var nbrBefore = before.normalizedDifference(['SR_B5', 'SR_B7']).rename('NBR_before');
var nbrAfter = after.normalizedDifference(['SR_B5', 'SR_B7']).rename('NBR_after');
var dNBR = nbrBefore.subtract(nbrAfter).rename('dNBR');

var burned = dNBR.gt(0.1).selfMask().rename('Burned_Area');

Map.addLayer(burned, {palette: 'orange'}, 'Burned Area');

// Statistics
var lossStats = ndviDiff.updateMask(forestLoss).reduceRegion({
  reducer: ee.Reducer.mean().combine({
    reducer2: ee.Reducer.count(),
    sharedInputs: true
  }),
  geometry: roi,
  scale: 30,
  maxPixels: 1e13
});

print('Forest Loss Statistics:', lossStats);

// Exports
Export.image.toDrive({
  image: ndviDiff,
  description: 'Yunnan_NDVI_Change_2018_2023',
  folder: 'GEE_Exports',
  scale: 30,
  crs: 'EPSG:4326',
  maxPixels: 1e13,
  region: roi.geometry()
});

Export.image.toDrive({
  image: forestLoss.addBands(burned),
  description: 'Yunnan_Forest_Loss_Burned_2018_2023',
  folder: 'GEE_Exports',
  scale: 30,
  crs: 'EPSG:4326',
  maxPixels: 1e13,
  region: roi.geometry()
});
```

## Expected Output
- NDVI difference map (GeoTIFF)
- Forest loss/burned area map (GeoTIFF)
- Change statistics (CSV)
- Area of change: ~X km2

## Methods
1. **Bi-temporal NDVI differencing**: Detects vegetation greenness change
2. **dNBR (differenced Normalized Burn Ratio)**: Detects burned areas
