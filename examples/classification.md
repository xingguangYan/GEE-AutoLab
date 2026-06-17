# Land Cover Classification Example

## Task Description

Perform land cover classification for Heilongjiang Province using Sentinel-2 data.

## Input
- Location: Heilongjiang Province
- Time: 2022
- Task: Land cover classification
- Classifier: Random Forest (100 trees)
- Export: GeoTIFF + Accuracy table

## Generated GEE Script

```javascript
// Land Cover Classification - Heilongjiang 2022
var roi = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level1')
  .filter(ee.Filter.eq('ADM1_NAME', 'Heilongjiang'));

Map.centerObject(roi, 7);

var collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(roi)
  .filterDate('2022-01-01', '2022-12-31')
  .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', 20));

function maskS2clouds(image) {
  var qa = image.select('QA60');
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(mask).divide(10000);
}

var image = collection.map(maskS2clouds).median().clip(roi);

// Add spectral indices as features
var ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI');
var ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI');
var nbr = image.normalizedDifference(['B8', 'B12']).rename('NBR');

var imageWithIndices = image.addBands(ndvi).addBands(ndwi).addBands(nbr);

// Training data (generate sample points using existing land cover product)
var existingLC = ee.Image('ESA/WorldCover/v200').select('Map').clip(roi);
var samplePoints = existingLC.stratifiedSample({
  numPoints: 5000,
  classBand: 'Map',
  scale: 10,
  region: roi,
  geometries: true
});

var bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12', 'NDVI', 'NDWI', 'NBR'];

var training = imageWithIndices.select(bands).sampleRegions({
  collection: samplePoints,
  properties: ['Map'],
  scale: 10
});

var classifier = ee.Classifier.smileRandomForest(100).train({
  features: training,
  classProperty: 'Map',
  inputProperties: bands
});

// Validation
var validation = training.randomColumn();
var trainSet = validation.filter('random <= 0.7');
var testSet = validation.filter('random > 0.3');

var trained = ee.Classifier.smileRandomForest(100)
  .train(trainSet, 'Map', bands);

var testAccuracy = testSet.classify(trained);
var confusionMatrix = testAccuracy.errorMatrix('Map', 'classification');

print('Confusion Matrix:', confusionMatrix);
print('Overall Accuracy:', confusionMatrix.accuracy());
print('Kappa Coefficient:', confusionMatrix.kappa());

// Classify the image
var classified = imageWithIndices.select(bands).classify(classifier).clip(roi);

Map.addLayer(classified, {
  min: 10, max: 90,
  palette: ['006400', '002400', 'ABAB00', '686C00', '00FF00', 'FFBB22', 'FFFF4C', 'F096FF', 'FA0000', '0064FF', '00FFFF', 'AARR']
}, 'Classification');

// Export
Export.image.toDrive({
  image: classified,
  description: 'Heilongjiang_LC_2022',
  folder: 'GEE_Exports',
  scale: 10,
  crs: 'EPSG:4326',
  maxPixels: 1e13,
  region: roi.geometry()
});
```

## Expected Output
- Classified GeoTIFF
- Accuracy assessment table (Overall Accuracy, Kappa, Confusion Matrix)
- Class area statistics (CSV)

## Classification Scheme (ESA WorldCover Classes)
| Code | Class | Color |
|------|-------|-------|
| 10 | Tree cover | Green |
| 20 | Shrubland | Yellow |
| 30 | Grassland | Light green |
| 40 | Cropland | Brown |
| 50 | Built-up | Red |
| 60 | Bare/sparse vegetation | Gray |
| 70 | Snow/ice | White |
| 80 | Permanent water bodies | Blue |
| 90 | Herbaceous wetland | Cyan |
| 95 | Mangroves | Dark green |
| 100 | Moss and lichen | Purple |
