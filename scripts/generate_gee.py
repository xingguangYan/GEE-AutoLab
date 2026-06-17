"""
GEE AutoLab — GEE Script Generator
Generates complete GEE Python scripts from parsed task parameters.
"""
import os
from datetime import datetime


def generate_gee_script(task_params: dict, project_id: str = None) -> str:
    """Generate a complete GEE Python script from parsed task parameters."""
    location = task_params.get("location", "study_area")
    start = task_params.get("start_date", "2023-01-01")
    end = task_params.get("end_date", "2023-12-31")
    tasks = task_params.get("tasks", ["index"])
    datasets = task_params.get("datasets", ["COPERNICUS/S2_SR_HARMONIZED"])
    params = task_params.get("params", {})
    scale = params.get("scale", 10)
    cloud = params.get("cloud_threshold", 20)
    classifier = params.get("classifier", "Random Forest")
    n_trees = params.get("n_trees", 100)
    crs = params.get("crs", "EPSG:4326")
    export_folder = params.get("export_folder", "GEE_Exports")
    
    script = f'''"""
GEE AutoLab — Generated Analysis Script
{location} | {start} ~ {end} | Tasks: {', '.join(tasks)}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
import ee
import geemap

{"ee.Initialize(project='" + project_id + "')" if project_id else "# Please set your project ID\n# ee.Initialize(project=\"your-project-id\")"}

# ============================================================
# STEP 1: Define ROI
# ============================================================
'''
    
    script += f"""# For Chinese admin boundaries:
# roi = ee.FeatureCollection("FAO/GAUL/2015/level2").filter(ee.Filter.eq("ADM2_NAME", "{location}"))
# roi = ee.FeatureCollection("projects/sat-io/open-datasets/CN/CHN_ADMIN_2022").filter(ee.Filter.eq("NAME", "{location}"))

# For coordinates: roi = ee.Geometry.Point([lng, lat]).buffer(5000)
# For vector file: roi = geemap.shp_to_ee("path/to/roi.shp")

# Placeholder — replace with actual ROI
roi = ee.Geometry.Point([114.3, 30.6]).buffer(10000)  # Wuhan example

# ============================================================
# STEP 2: Load & Preprocess Data
# ============================================================

"""
    
    for ds in datasets:
        ds_id = ds.split("/")[-1].replace("/", "_")
        script += f"""# Dataset: {ds}
collection_{ds_id} = (
    ee.ImageCollection("{ds}")
    .filterBounds(roi)
    .filterDate("{start}", "{end}")
)
"""
    
    script += f"""
# Cloud masking function
def mask_clouds(image):
    \"\"\"Cloud masking for Sentinel-2 / Landsat.\"\"\"
"""
    
    if any("S2" in ds for ds in datasets):
        script += """    qa = image.select("SCL")
    cloud_mask = qa.neq(3).And(qa.neq(8).And(qa.neq(9).And(qa.neq(10))))
    return image.updateMask(cloud_mask).divide(10000)
"""
    elif any("LC0" in ds for ds in datasets):
        script += """    qa = image.select("QA_PIXEL")
    cloud_mask = qa.bitwiseAnd(1 << 3).eq(0)  # Cloud bit
    return image.updateMask(cloud_mask)
"""
    else:
        script += """    return image  # No masking for this dataset
"""
    
    script += f"""
# Apply masking
masked = (
    collection_{ds_id}
    .map(mask_clouds)
    .median()
    .clip(roi)
)

print("Masked composite ready.")
print("Scale:", {scale}, "m | CRS: {crs}")

# ============================================================
# STEP 3: Analysis
# ============================================================

"""
    
    if "index" in tasks or "ndvi" in str(tasks).lower():
        script += """# Index Calculations
def compute_indices(image):
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    evi = image.expression(
        "2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))",
        {"NIR": image.select("B8"), "RED": image.select("B4"), "BLUE": image.select("B2")}
    ).rename("EVI")
    ndwi = image.normalizedDifference(["B3", "B8"]).rename("NDWI")
    mndwi = image.normalizedDifference(["B3", "B11"]).rename("MNDWI")
    ndbi = image.normalizedDifference(["B11", "B8"]).rename("NDBI")
    return image.addBands([ndvi, evi, ndwi, mndwi, ndbi])

result = compute_indices(masked)
print("Indices computed: NDVI, EVI, NDWI, MNDWI, NDBI")
"""
    elif "classification" in tasks:
        script += f"""# Land Cover Classification ({classifier}, n={n_trees})
label = "ESA/WorldCover/v200"
worldcover = ee.Image(label).clip(roi)
samples = result.addBands(worldcover.select("Map")).stratifiedSample(
    numPoints=1000, classBand="Map", region=roi, scale={scale}, geometries=True
)
training = samples.filter(ee.Filter.lte("Map", 10))
train_data = training.randomColumn()
train_set = train_data.filter(ee.Filter.lte("random", 0.7))
test_set = train_data.filter(ee.Filter.gt("random", 0.7))

trainer = ee.Classifier.smileRandomForest({n_trees}).train(
    features=train_set, classProperty="Map", inputProperties=result.bandNames()
)
classified = result.classify(trainer)

# Accuracy
test_result = test_set.classify(trainer)
confusion = test_result.errorMatrix("Map", "classification")
oa = confusion.accuracy()
kappa = confusion.kappa()
print(f"OA: {{oa.getInfo()}}, Kappa: {{kappa.getInfo()}}")

result = classified.rename("classification")
"""
    elif "change_detection" in tasks:
        script += f"""# Change Detection (Image Differencing)
# Year 1 composite
year1 = (
    collection_{ds_id}.filterDate("{start}", "{end.replace('-12-31', '-06-30')}")
    .map(mask_clouds).median().clip(roi)
)
# Year 2 composite
year2 = (
    collection_{ds_id}.filterDate("{end.replace('-12-31', '-07-01')}", "{end}")
    .map(mask_clouds).median().clip(roi)
)

ndvi1 = year1.normalizedDifference(["B8", "B4"]).rename("NDVI_1")
ndvi2 = year2.normalizedDifference(["B8", "B4"]).rename("NDVI_2")
diff = ndvi2.subtract(ndvi1).rename("NDVI_diff")

result = diff.addBands([ndvi1, ndvi2])
print("Change detection: NDVI difference computed")
"""
    else:
        script += """# Generic analysis
result = masked  # Use the composite as-is
print("Analysis complete.")
"""
    
    script += f"""
# ============================================================
# STEP 4: Visualization
# ============================================================

Map = geemap.Map()
Map.centerObject(roi, 10)
Map.addLayer(roi, {{}}, "ROI")
Map.addLayer(result, {{"min": -1, "max": 1, "palette": ["red", "yellow", "green"]}}, "Result")
Map

# ============================================================
# STEP 5: Export
# ============================================================

# Export GeoTIFF
task_img = ee.batch.Export.image.toDrive(
    image=result,
    description="{'_'.join(tasks)}_{location}",
    folder="{export_folder}",
    fileNamePrefix="{'_'.join(tasks)}_{location}_{start[:4]}",
    region=roi.geometry().bounds().getInfo(),
    scale={scale},
    crs="{crs}",
    maxPixels=1e13,
    fileDimensions=2560,
    skipEmptyTiles=True
)
task_img.start()
print("GeoTIFF export started:", task_img.id)

# Export CSV Stats
stats = result.reduceRegions(
    collection=roi,
    reducer=ee.Reducer.mean().combine(ee.Reducer.stdDev(), sharedInputs=True)
        .combine(ee.Reducer.minMax(), sharedInputs=True),
    scale={scale}
)
task_csv = ee.batch.Export.table.toDrive(
    collection=stats,
    description="stats_{'_'.join(tasks)}_{location}",
    folder="{export_folder}",
    fileNamePrefix="stats_{'_'.join(tasks)}_{location}_{start[:4]}",
    fileFormat="CSV"
)
task_csv.start()
print("CSV export started:", task_csv.id)
"""
    
    return script


def save_script(script: str, output_dir: str = "outputs") -> str:
    """Save script to file."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"gee_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"Script saved: {filepath}")
    return filepath




def _band_info(dataset_id):
    d = dataset_id.lower()
    if "s2" in d or "sentinel" in d:
        return {"NIR":"B8","RED":"B4","GREEN":"B3","BLUE":"B2","SWIR1":"B11","RE1":"B5"}
    elif "landsat" in d or "l0" in d:
        return {"NIR":"SR_B5","RED":"SR_B4","GREEN":"SR_B3","BLUE":"SR_B2","SWIR1":"SR_B6"}
    return {"NIR":"NIR","RED":"RED","GREEN":"GREEN","BLUE":"BLUE","SWIR1":"SWIR1"}

def _mask_code(dataset_id, threshold=20):
    d = dataset_id.lower()
    if "s2" in d or "sentinel" in d:
        return "def mask(img):\n    scl=img.select(\"SCL\")\n    return img.updateMask(scl.neq(3).And(scl.neq(8).And(scl.neq(9).And(scl.neq(10))))).divide(10000)"
    elif "landsat" in d:
        return "def mask(img):\n    qa=img.select(\"QA_PIXEL\")\n    return img.updateMask(qa.bitwiseAnd(1<<3).eq(0).And(qa.bitwiseAnd(1<<4).eq(0)).And(qa.bitwiseAnd(1<<5).eq(0)))"
    return "def mask(img): return img"

def _roi_code(location):
    if not location:
        return "# roi = ee.Geometry.Point([114.3, 30.6]).buffer(10000)"
    cn = {"武汉":"projects/sat-io/open-datasets/CN/CHN_ADMIN_2022",
          "北京":"projects/sat-io/open-datasets/CN/CHN_ADMIN_2022",
          "上海":"projects/sat-io/open-datasets/CN/CHN_ADMIN_2022",
          "黑龙江":"projects/sat-io/open-datasets/CN/CHN_ADMIN_2022"}
    for k in cn:
        if k in location:
            return f'roi = ee.FeatureCollection("{cn[k]}")\
    .filter(ee.Filter.eq("NAME","{location}"))\
    .geometry()'
    return "# roi = ee.Geometry.Point([114.3, 30.6]).buffer(10000)"

def _classify_body(params, bands):
    loc = params.get("location", "study_area")
    start = params.get("start_date", "2023-01-01")
    end = params.get("end_date", "2023-12-31")
    dataset = params["datasets"][0] if params["datasets"] else "LANDSAT/LC08/C02/T1_L2"
    p = params["params"]
    scale = p["scale"]
    crs = p.get("crs", "EPSG:4326")
    folder = p.get("export_folder", "GEE_Exports")
    nt = p.get("n_trees", 100)
    nir, red, green, swir1 = bands["NIR"], bands["RED"], bands["GREEN"], bands["SWIR1"]

    return f"""# ===== 1. Study Area =====
{_roi_code(loc)}
print("Area km2:", roi.area().divide(1e6).getInfo())
# ===== 2. Data =====
{_mask_code(dataset, p["cloud_threshold"])}
composite = (ee.ImageCollection("{dataset}")
    .filterBounds(roi).filterDate("{start}", "{end}")
    .map(mask).median().clip(roi))
ndvi = composite.normalizedDifference(["{nir}", "{red}"]).rename("NDVI")
features = composite.addBands(ndvi)
# ===== 3. Training =====
samples = features.addBands(ee.Image("ESA/WorldCover/v200").clip(roi).select("Map"))
samples = samples.stratifiedSample(numPoints=2000, classBand="Map", region=roi, scale={scale})
split = samples.randomColumn(42)
train = split.filter(ee.Filter.lte("random", 0.7))
test = split.filter(ee.Filter.gt("random", 0.3))
# ===== 4. Train RF =====
clf = ee.Classifier.smileRandomForest({nt}).train(train, "Map", features.bandNames())
classified = features.classify(clf).rename("classification")
# ===== 5. Accuracy =====
cm = test.classify(clf).errorMatrix("Map", "classification")
print("OA:", round(cm.accuracy().getInfo(), 4), "Kappa:", round(cm.kappa().getInfo(), 4))
# ===== 6. Export =====
ee.batch.Export.image.toDrive(image=classified.toByte(), scale={scale}, crs="{crs}",
    region=roi.bounds().getInfo() if hasattr(roi,"bounds") else roi,
    maxPixels=1e13, folder="{folder}", fileNamePrefix="classified_{loc}").start()
"""

def _change_body(params, bands):
    loc = params.get("location", "study_area")
    start = params.get("start_date", "2018-01-01")
    end = params.get("end_date", "2023-12-31")
    dataset = params["datasets"][0] if params["datasets"] else "LANDSAT/LC08/C02/T1_L2"
    p = params["params"]
    scale = p["scale"]
    crs = p.get("crs", "EPSG:4326")
    folder = p.get("export_folder", "GEE_Exports")
    nir, red = bands["NIR"], bands["RED"]
    mid = (int(start[:4]) + int(end[:4])) // 2
    return f"""# ===== 1. Study Area =====
{_roi_code(loc)}
# ===== 2. NDVI =====
{_mask_code(dataset, p["cloud_threshold"])}
def ndvi_comp(s, e):
    return (ee.ImageCollection("{dataset}").filterBounds(roi).filterDate(s, e).map(mask).median().clip(roi)
        .normalizedDifference(["{nir}", "{red}"]).rename("NDVI"))
ndvi1 = ndvi_comp("{start}", "{mid-1}-12-31")
ndvi2 = ndvi_comp("{mid}-01-01", "{end}")
diff = ndvi2.subtract(ndvi1).rename("diff")
change = diff.expression("b(0)>0.15?1:b(0)<-0.15?3:2").rename("change")
area = change.multiply(ee.Image.pixelArea()).reduceRegion(
    reducer=ee.Reducer.sum().group(1), geometry=roi, scale={scale}, maxPixels=1e10)
print("Areas:", area.getInfo())
# ===== 3. Export =====
ee.batch.Export.image.toDrive(image=ndvi1.addBands([ndvi2, diff, change]).toFloat(),
    scale={scale}, crs="{crs}", region=roi.bounds().getInfo() if hasattr(roi,"bounds") else roi,
    maxPixels=1e13, folder="{folder}", fileNamePrefix="change_{loc}").start()
"""

def _timeseries_body(params, bands):
    loc = params.get("location", "study_area")
    start = params.get("start_date", "2000-01-01")
    end = params.get("end_date", "2023-12-31")
    p = params["params"]
    folder = p.get("export_folder", "GEE_Exports")
    scale = 250
    return f"""# ===== 1. Study Area =====
{_roi_code(loc)}
# ===== 2. MODIS NDVI =====
col = (ee.ImageCollection("MODIS/061/MOD13Q1")
    .filterBounds(roi).filterDate("{start}", "{end}").select(["NDVI","EVI","SummaryQA"]))
clean = col.map(lambda img: img.updateMask(img.select("SummaryQA").lte(1)).multiply(0.0001))
# ===== 3. Annual =====
years = ee.List.sequence(int("{start}"[:4]), int("{end}"[:4]))
def annual(y):
    ann = clean.filterDate(ee.Date.fromYMD(y,1,1), ee.Date.fromYMD(y,1,1).advance(1,"year")).mean()
    return ann.set("year", y).set("system:time_start", ee.Date.fromYMD(y,6,1))
annual_col = ee.ImageCollection.fromImages(years.map(annual))
# ===== 4. Trend =====
slope = annual_col.select("NDVI").reduce(ee.Reducer.linearFit()).select("scale").multiply(10).rename("trend")
# ===== 5. Export =====
ee.batch.Export.image.toDrive(image=slope.toFloat(), scale={scale},
    region=roi.bounds().getInfo() if hasattr(roi,"bounds") else roi,
    maxPixels=1e13, folder="{folder}", fileNamePrefix="trend_{loc}").start()
"""

def generate_gee_script_v2(params, project_id=None):
    """Multi-task aware GEE script generator."""
    tasks = params.get("tasks", ["index"])
    dataset = params.get("datasets", ["COPERNICUS/S2_SR_HARMONIZED"])[0]
    bands = _band_info(dataset)
    loc = params.get("location", "study_area")
    start = params.get("start_date", "2023-01-01")
    end = params.get("end_date", "2023-12-31")
    scale = params["params"]["scale"]
    ts = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    hdr = f"""
GEE AutoLab - {", ".join(tasks)}
Location : {loc}
Time     : {start} ~ {end}
Dataset  : {dataset}
Scale    : {scale}m
Generated: {ts}
"""

    if "classification" in tasks:
        body = _classify_body(params, bands)
    elif "change_detection" in tasks:
        body = _change_body(params, bands)
    elif "timeseries" in tasks or "time_series" in tasks:
        body = _timeseries_body(params, bands)
    else:
        body = generate_gee_script(params, project_id)
    return hdr + "\n" + body
