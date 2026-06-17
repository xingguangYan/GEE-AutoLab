import re, json
from datetime import datetime

DEFAULT_PARAMS = {"scale": None, "cloud_threshold": 20, "classifier": "Random Forest", "n_trees": 100, "crs": "EPSG:4326", "export_folder": "GEE_Exports", "composite_method": "median"}

TASK_KEYWORDS = {
    "index": ["ndvi","evi","ndwi","mndwi","ndbi","ndmi","savi","gci","reci"],
    "classification": ["classification","land cover","lulc","random forest","cart"],
    "change_detection": ["landtrendr","ccdc","change detection","bfast"],
    "timeseries": ["time series","trend","temporal"],
    "fire": ["burned area","fire","modis fire","nbr"],
    "water": ["water","flood","inundation"],
    "urban": ["urban","nightlight"],
    "lst": ["lst","land surface temperature"],
    "dem": ["dem","srtm","slope"],
    "sar": ["sar","sentinel-1","radar","vv","vh"],
    "precipitation": ["precipitation","gpm","imerg"],
    "export": ["geotiff","csv","export"],
}

DATASET_KEYWORDS = {
    "COPERNICUS/S2_SR_HARMONIZED": ["sentinel-2","sentinel2","s2 ","sentinel 2"],
    "LANDSAT/LC08/C02/T1_L2": ["landsat 8","landsat8","l8","landsat 9","landsat9","l9"],
    "LANDSAT/LE07/C02/T1_L2": ["landsat 7","landsat7","l7","etm"],
    "LANDSAT/LT05/C02/T1_L2": ["landsat 5","landsat5","l5","tm"],
    "MODIS/061/MOD13Q1": ["modis ndvi","mod13q1"],
    "MODIS/061/MOD14A1": ["modis fire","mod14a1"],
    "COPERNICUS/S1_GRD": ["sentinel-1","sentinel1","s1 ","sar"],
}

def _extract_time(text, result):
    m = re.search(r"(\d{4})\s*[-_\u2013\u2014\u81f3\u5230]\s*(\d{4})", text)
    if m: result["start_date"]=f"{m.group(1)}-01-01"; result["end_date"]=f"{m.group(2)}-12-31"; return result
    m = re.search(r"(\d{4}-\d{2}-\d{2})\s*(?:\u81f3|\u5230|to|~)\s*(\d{4}-\d{2}-\d{2})", text)
    if m: result["start_date"]=m.group(1); result["end_date"]=m.group(2); return result
    m = re.search(r"(\d{4})\s*\u5e74", text)
    if m: y=m.group(1); result["start_date"]=f"{y}-01-01"; result["end_date"]=f"{y}-12-31"; return result
    # Standalone 4-digit year in text
    m = re.search(r"(?<!\d)(\d{4})(?!\d)", text)
    if m: y=m.group(1); result["start_date"]=f"{y}-01-01"; result["end_date"]=f"{y}-12-31"; return result
    y = datetime.now().year - 1
    result["start_date"]=f"{y}-01-01"; result["end_date"]=f"{y}-12-31"
    return result

def _extract_location(text, result):
    m = re.search(r"(?:\u5730\u70b9[\uff1a:]\s*)([^\u2502;|\n]{2,30})", text)
    if m: result["location"]=m.group(1).strip(); return result
    m = re.search(r"(?:\u5728|\u4e8e|\u9488\u5bf9)(.{2,8}(?:\u7701|\u5e02|\u533a|\u53bf))", text)
    if m: result["location"]=m.group(1).strip()
    return result

def _extract_scale(text, result):
    m = re.search(r"(\d+)\s*m[^a-zA-Z]", text)
    if m: result["params"]["scale"]=int(m.group(1)); return result
    m = re.search(r"(?:resolution|\u5206\u8fa8\u7387)\D{0,10}(\d+)", text.lower())
    if m: result["params"]["scale"]=int(m.group(1))
    return result

def _auto_determine_scale(datasets):
    s = " ".join(datasets).lower()
    if "s2" in s or "sentinel" in s: return 10
    if "landsat" in s: return 30
    if "modis" in s: return 250
    return 30

def _auto_select_dataset(result):
    tasks = result["tasks"]
    sc = result["params"]["scale"] or 30
    has_land = any(t in tasks for t in ["index","classification","urban"])
    if has_land: result["datasets"].append("COPERNICUS/S2_SR_HARMONIZED" if sc <= 10 else "LANDSAT/LC08/C02/T1_L2")
    if "timeseries" in tasks or "change_detection" in tasks:
        if "LANDSAT/LC08/C02/T1_L2" not in result["datasets"]: result["datasets"].append("LANDSAT/LC08/C02/T1_L2")
    if "fire" in tasks: result["datasets"].append("MODIS/061/MOD14A1")
    if "lst" in tasks: result["datasets"].append("LANDSAT/LC08/C02/T1_L2")
    if not result["datasets"]: result["datasets"].append("COPERNICUS/S2_SR_HARMONIZED")
    return result

def _detect_user_dataset(text, result):
    tl = text.lower()
    for ds_id, kws in DATASET_KEYWORDS.items():
        for kw in kws:
            if kw in tl:
                if ds_id not in result["datasets"]: result["datasets"].append(ds_id)
                break
    return result

def parse_task(user_input):
    r = {"raw_input":user_input,"location":None,"start_date":None,"end_date":None,"tasks":[],"params":DEFAULT_PARAMS.copy(),"datasets":[],"export_formats":["GeoTIFF","CSV"],"report":True}
    ul = user_input.lower()
    CN_KWS = {'classification':['分类','耕地','土地覆盖'],'index':['指数','ndvi','evi','ndwi'],'change_detection':['变化检测','变化'],'fire':['火点','火灾']}
    for tt, kws in CN_KWS.items():
        for kw in kws:
            if kw in user_input and tt not in r['tasks']: r['tasks'].append(tt); break
    for tt, kws in TASK_KEYWORDS.items():
        for kw in kws:
            if kw in ul and tt not in r["tasks"]: r["tasks"].append(tt); break
    cm = re.search(r"(?:cloud|\u4e91\u91cf)\s*<?\s*(\d+)", ul)
    if cm: r["params"]["cloud_threshold"] = int(cm.group(1))
    for c in ["Random Forest","CART","SVM","Gradient Boosted Trees"]:
        if c.lower() in ul: r["params"]["classifier"] = c; break
    r = _extract_time(user_input, r)
    r = _extract_location(user_input, r)
    r = _extract_scale(user_input, r)
    r = _detect_user_dataset(user_input, r)
    if not r["datasets"]: r = _auto_select_dataset(r)
    if r["params"]["scale"] is None: r["params"]["scale"] = _auto_determine_scale(r["datasets"])
    return r

def print_parsed(r):
    print("="*55)
    print("  GEE AutoLab - Task Parse Result")
    print("="*55)
    print(f'  Location      : {r["location"] or "Auto-detect needed"}')
    print(f'  Time Range    : {r["start_date"]} ~ {r["end_date"]}')
    ts = ", ".join(r["tasks"]) or "Auto-detect needed"
    print(f'  Tasks         : {ts}')
    print(f'  Datasets      : {", ".join(r["datasets"])}')
    print(f'  Scale         : {r["params"]["scale"]}m')
    print(f'  Cloud Threshold: {r["params"]["cloud_threshold"]}%')
    print(f'  Classifier    : {r["params"]["classifier"]}')
    print(f'  Export Formats: {", ".join(r["export_formats"])}')
    print("="*55)

if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Wuhan, 2023, NDVI"
    print_parsed(parse_task(q))
