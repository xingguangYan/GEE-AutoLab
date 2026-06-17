#!/usr/bin/env python3
"""
GEE AutoLab — Report Generator
Generates structured experiment reports in Markdown and HTML.
"""
import os, json
from datetime import datetime


def _report_markdown(params: dict, results: dict) -> str:
    """Generate the Markdown report body."""
    loc = params.get("location", "N/A")
    start = params.get("start_date", "N/A")
    end = params.get("end_date", "N/A")
    tasks = ", ".join(params.get("tasks", ["N/A"]))
    datasets = params.get("datasets", [])
    p = params.get("params", {})
    scale = p.get("scale", "N/A")
    cloud = p.get("cloud_threshold", "N/A")
    clf = p.get("classifier", "N/A")
    ntrees = p.get("n_trees", "N/A")
    crs = p.get("crs", "EPSG:4326")
    folder = p.get("export_folder", "GEE_Exports")

    return f"""# GEE AutoLab Experiment Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Query**: {params.get("raw_input", "N/A")}

---

## 1. Study Area

| Field | Value |
|-------|-------|
| **Location** | {loc} |
| **Time Range** | {start} ~ {end} |

## 2. Data Sources

| Dataset | Scale |
|---------|-------|
""" + "\n".join([f"| `{d}` | {scale}m |" for d in datasets]) + f"""

## 3. Methodology

| Step | Description |
|------|-------------|
| **Preprocessing** | Cloud masking ({cloud}% threshold), temporal/spatial filter, median composite, ROI clip |
| **Analysis Tasks** | {tasks} |
| **Classifier** | {clf} (n={ntrees}), CRS: {crs} |
| **Exports** | GeoTIFF (Drive), CSV (Drive), Visualization (geemap) |

## 4. Parameters

| Parameter | Value |
|-----------|-------|
| Spatial Resolution | {scale}m |
| Cloud Threshold | {cloud}% |
| Classifier | {clf} |
| RF Trees | {ntrees} |
| Export CRS | {crs} |
| Export Folder | {folder} |

## 5. Results & Statistics

{f"| Statistic | Value |\\n|-----------|-------|\\n" + chr(10).join([f"| {k} | {v} |" for k, v in results.get("stats", {}).items()]) if results.get("stats") else "*(Results pending — GEE export tasks have been submitted. Run `earthengine task list` to check status.)*"}

### Classification Accuracy
{_classification_table(results) if results.get("classification") else "*(N/A — not a classification task)*"}

## 6. Visualizations

- `figures/study_area.png` — Study area overview
- `figures/result_map.png` — Analysis result visualization
- `figures/time_series.png` — Temporal trend (if applicable)

## 7. Export Files

| File | Description |
|------|-------------|
| `{tasks.replace(", ", "_")}_{loc.replace(' ', '_')}.tif` | Analysis result GeoTIFF |
| `stats_{tasks.replace(", ", "_")}_{loc.replace(' ', '_')}.csv` | Zonal statistics table |
| `gee_script_{tasks.replace(", ", "_")}.py` | Generated GEE Python script |

## 8. Limitations & Suggestions

- **Cloud coverage**: {cloud}% threshold may reduce temporal density in cloudy regions
- **Resolution**: {scale}m limits detection of fine-scale features
- **Temporal coverage**: {start} to {end} may not capture long-term (>10yr) trends
- **Validation**: Results should be validated with field data or higher-resolution imagery
- **Suggestion**: For large ROIs, consider splitting into tiles or using coarser resolution

## References

1. Google Earth Engine. https://earthengine.google.com/
2. Gorelick, N., et al. (2017). Google Earth Engine. *Remote Sensing of Environment*, 202, 18–27.
3. GEE AutoLab. https://github.com/xingguangYan/GEE-AutoLab
"""


def _classification_table(results: dict) -> str:
    """Generate classification accuracy table."""
    clf = results.get("classification", {})
    rows = [
        ("Overall Accuracy", clf.get("oa", "Pending")),
        ("Kappa", clf.get("kappa", "Pending")),
        ("Precision", clf.get("precision", "Pending")),
        ("Recall", clf.get("recall", "Pending")),
        ("F1 Score", clf.get("f1", "Pending")),
    ]
    table = "| Metric | Value |\n|--------|-------|\n"
    table += "\n".join([f"| {k} | {v} |" for k, v in rows])
    return table


def _report_html(params: dict, results: dict) -> str:
    """Generate HTML report."""
    loc = params.get("location", "N/A")
    start = params.get("start_date", "N/A")
    end = params.get("end_date", "N/A")
    tasks = ", ".join(params.get("tasks", ["N/A"]))
    md = _report_markdown(params, results)

    # Simple HTML conversion
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>GEE AutoLab Report — {loc}</title>
<style>
body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; line-height: 1.8; color: #333; }}
h1 {{ color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }}
h2 {{ color: #2c3e50; margin-top: 30px; }}
table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
th {{ background: #f5f5f5; font-weight: 600; }}
tr:nth-child(even) {{ background: #fafafa; }}
code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
.footer {{ margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 0.85em; color: #888; }}
</style>
</head>
<body>
<h1>GEE AutoLab Experiment Report</h1>
<p><strong>Location</strong>: {loc} | <strong>Period</strong>: {start} ~ {end}<br>
<strong>Tasks</strong>: {tasks}<br>
<strong>Generated</strong>: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

<div class="md-content">
{md}
</div>

<div class="footer">
<p>Generated by <a href="https://github.com/xingguangYan/GEE-AutoLab">GEE AutoLab</a></p>
</div>
</body>
</html>"""
    return html


def generate_report(params: dict, results: dict, output_dir: str = "outputs",
                    formats: list = None) -> list:
    """Generate experiment reports in specified formats."""
    if formats is None:
        formats = ["md", "html"]

    os.makedirs(output_dir, exist_ok=True)
    loc = params.get("location", "study_area").replace(" ", "_")
    task = "_".join(params.get("tasks", ["analysis"])).replace(" ", "_")
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"report_{task}_{loc}_{date}"

    paths = []

    if "md" in formats:
        md = _report_markdown(params, results)
        path = os.path.join(output_dir, f"{base}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"  Report (Markdown): {path}")
        paths.append(path)

    if "html" in formats:
        html = _report_html(params, results)
        path = os.path.join(output_dir, f"{base}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Report (HTML): {path}")
        paths.append(path)

    return paths


if __name__ == "__main__":
    demo_params = {
        "raw_input": "在武汉市，2023年Sentinel-2 NDVI计算",
        "location": "武汉市",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "tasks": ["index", "ndvi"],
        "datasets": ["COPERNICUS/S2_SR_HARMONIZED"],
        "params": {"scale": 10, "cloud_threshold": 20, "classifier": "Random Forest", "n_trees": 100,
                   "crs": "EPSG:4326", "export_folder": "GEE_Exports", "composite_method": "median"},
        "export_formats": ["GeoTIFF", "CSV"],
        "report": True,
    }
    demo_results = {
        "stats": {"mean_ndvi": 0.45, "std_ndvi": 0.12, "max_ndvi": 0.89, "min_ndvi": -0.05}
    }
    generate_report(demo_params, demo_results)
