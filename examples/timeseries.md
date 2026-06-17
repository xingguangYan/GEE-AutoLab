# Time Series Analysis Example

## Task Description

Analyze NDVI time series trends in the Yangtze River Basin from 2000 to 2023.

## Input
- Location: Yangtze River Basin
- Time: 2000 to 2023
- Task: NDVI time series trend analysis
- Data: MODIS MOD13Q1 (250m, 16-day)

## Generated GEE Script

```javascript
// NDVI Time Series Analysis - Yangtze River Basin
var roi = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level0')
  .filter(ee.Filter.eq('ADM0_NAME', 'China'));

// Simple Yangtze basin approximation (bounding box)
var yangtze = ee.Geometry.Rectangle([97, 24, 122, 35]);
Map.centerObject(yangtze, 5);

var collection = ee.ImageCollection('MODIS/061/MOD13Q1')
  .filterBounds(yangtze)
  .filterDate('2000-01-01', '2023-12-31')
  .select('NDVI');

// Scale NDVI (MODIS NDVI is scaled by 0.0001)
function scaleNDVI(image) {
  return image.multiply(0.0001).copyProperties(image, ['system:time_start', 'system:index']);
}

var ndvi = collection.map(scaleNDVI);

// Create annual composites
var years = ee.List.sequence(2000, 2023);
var annualNDVI = ee.ImageCollection.fromImages(years.map(function(year) {
  var start = ee.Date.fromYMD(year, 1, 1);
  var end = ee.Date.fromYMD(year, 12, 31);
  var annual = ndvi.filterDate(start, end).mean().clip(yangtze);
  return annual.set('year', year).set('system:time_start', start);
}));

// Calculate trend (Theil-Sen / median slope)
var trend = annualNDVI.select('NDVI').reduce(ee.Reducer.linearFit())
  .rename(['slope', 'offset', 'r2']);

var slopeVis = {
  min: -0.01, max: 0.01,
  palette: ['red', 'white', 'green']
};

Map.addLayer(trend.select('slope'), slopeVis, 'NDVI Trend Slope');

// Greenness trend direction
var greening = trend.select('slope').gt(0).selfMask().rename('Greening');
var browning = trend.select('slope').lt(0).selfMask().rename('Browning');

Map.addLayer(greening, {palette: 'green'}, 'Greening');
Map.addLayer(browning, {palette: 'red'}, 'Browning');

// Extract time series for a point
var samplePoint = ee.Geometry.Point([110, 30]);
var ts = ndvi.filterBounds(samplePoint).map(function(img) {
  var value = img.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: samplePoint,
    scale: 250
  });
  return ee.Feature(null, {
    'date': img.date().format('YYYY-MM-dd'),
    'NDVI': value.get('NDVI')
  });
});

print('Time series at sample point:', ts);

// Exports
Export.image.toDrive({
  image: trend.select('slope'),
  description: 'Yangtze_NDVI_Trend_2000_2023',
  folder: 'GEE_Exports',
  scale: 250,
  crs: 'EPSG:4326',
  maxPixels: 1e13,
  region: yangtze
});

Export.table.toDrive({
  collection: ts,
  description: 'Yangtze_NDVI_TimeSeries_Point',
  folder: 'GEE_Exports',
  fileFormat: 'CSV'
});
```

## Expected Output
- NDVI trend slope map (GeoTIFF)
- Greening/browning classification
- Time series data for sample points (CSV)
- Trend analysis statistics

## Trend Interpretation
- **Positive slope (green)**: Vegetation greening/increasing
- **Negative slope (red)**: Vegetation browning/decreasing
- **Near-zero**: Stable vegetation
