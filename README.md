# | GEE AutoLab - Automated Remote Sensing Research Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GEE](https://img.shields.io/badge/Earth%20Engine-API-green.svg)](https://earthengine.google.com/)

> **GEE AutoLab** is a fully automated remote sensing analysis agent built on Google Earth Engine. It transforms a simple natural language query (time + location + task) into a complete scientific workflow: data retrieval | GEE script generation | index/classification/change detection analysis | GeoTIFF/CSV export | experiment report generation.

---

##  Features

### | Zero-Code Operation
- **Natural Language Input**: Describe your analysis in plain Chinese or English
- **Auto Parameter Filling**: Missing parameters are automatically filled with intelligent defaults
- **One-Click Execution**: From query to full scientific report in one command

###  Comprehensive Data Source Support
- **Official GEE Datasets**: Full support for 50+ public datasets including Sentinel, Landsat, MODIS, VIIRS, GPM, SRTM, ERA5, etc.
- **SAT-IO Community Catalog**: Extended support for community-contributed datasets
- **Intelligent Auto-Selection**: Automatically selects the optimal dataset based on task type and resolution requirements
- **Custom Dataset Support**: Users can specify any GEE dataset by ID

### | 12 Analysis Task Categories
1. **Vegetation Indices** - NDVI, EVI, NDWI, MNDWI, NDBI, NDMI, SAVI, GCI, RECI, NBR, PSRI, SIPI, ARVI, GNDVI, NDRE, MSAVI (16+ indices)
2. **Water & Wetland Analysis** - Water extraction, area statistics, wetland classification, shoreline change
3. **Land Cover Classification** - Random Forest, CART, SVM, Gradient Boosted Trees with accuracy assessment
4. **Change Detection** - LandTrendr, CCDC, bi-temporal differencing, spectral angle, PCA change detection
5. **Time Series Analysis** - Annual/monthly composites, trend analysis, anomaly detection, phenology parameters
6. **Urban & Nightlight** - Urban expansion, impervious surface, NPP-VIIRS analysis, urban heat island
7. **Forest & Carbon** - Forest cover, disturbance detection, biomass estimation, carbon stock calculation
8. **Disaster Monitoring** - Fire detection, burn area, flood mapping, drought monitoring, landslide detection
9. **Terrain & DEM** - Elevation, slope/aspect, watershed delineation, topographic indices
10. **Meteorology & Climate** - Precipitation, temperature, evapotranspiration, drought indices
11. **SAR Analysis** - Sentinel-1 GRD, flood detection, ship detection, soil moisture
12. **Statistics & Export** - Area statistics, zonal statistics, CSV export, chart generation

### | Automatic Export
- **GeoTIFF** - Cloud-optimized raster export
- **CSV** - Statistical tables and time series data
- **Shapefile/GeoJSON** - Vector analysis results
- **PNG/JPG** - Visualization thumbnails
- **Cloud Optimized GeoTIFF** - For efficient web delivery

### | Scientific Report Generation
- Research area overview
- Data source documentation
- Methodology description
- Parameter configuration record
- Result statistics and analysis
- Accuracy assessment (for classification tasks)
- Charts and visualizations
- Limitations and improvement suggestions

### | GEE Official Docs Integration
GEE AutoLab is built with reference to the complete GEE documentation ecosystem:
- [GEE Quick Start Guide](https://developers.google.com/earth-engine/guides/getstarted|?hl=zh-cn)
- [GEE Datasets Catalog](https://developers.google.com/earth-engine/datasets|?hl=zh-cn)
- [GEE Community Datasets (SAT-IO)](https://developers.google.com/earth-engine/datasets/community/sat-io|?hl=zh-cn)
- [GEE Classification Guide](https://developers.google.com/earth-engine/guides/classification|?hl=zh-cn)
- [GEE Change Detection Guide](https://developers.google.com/earth-engine/guides/changedetection|?hl=zh-cn)
- [GEE Time Series Analysis](https://developers.google.com/earth-engine/guides/arrays_time_series|?hl=zh-cn)
- [GEE Export Guide](https://developers.google.com/earth-engine/guides/exporting|?hl=zh-cn)
- [GEE Best Practices](https://developers.google.com/earth-engine/guides/best_practices|?hl=zh-cn)

---

## | Quick Start

### Prerequisites
- Python 3.9+
- Google Earth Engine account ([sign up](https://signup.earthengine.google.com/))
- Internet connection

### Installation

`ash
# Clone the repository
git clone https://github.com/xingguangYan/GEE-AutoLab.git
cd GEE-AutoLab

# Install dependencies
pip install -r requirements.txt

# Authenticate with GEE
earthengine authenticate

# Verify installation
python scripts/check_gee.py
`

### Usage Examples

**Example 1: Vegetation Index Calculation**
`ash
python scripts/run_pipeline.py "在武汉市，2023年，计算NDVI和EVI" --output result_wuhan
`

**Example 2: Land Cover Classification**
`ash
python scripts/run_pipeline.py "地点：黑龙江省 时间：2022 任务：土地覆盖分类 分类器：Random Forest" --output result_heilongjiang
`

**Example 3: Change Detection**
`ash
python scripts/run_pipeline.py "云南省，2018-2023年，森林变化检测" --output result_yunnan_forest
`

**Example 4: Time Series Analysis**
`ash
python scripts/run_pipeline.py "长江流域，2000-2023年，NDVI时间序列趋势分析" --output result_yangtze_timeseries
`

### Quick Modes

`ash
# Quiet mode - suppress detailed progress
python scripts/run_pipeline.py "||" --output output_dir -q

# Generate GEE code only (no execution)
python scripts/run_pipeline.py "||" --output output_dir --code-only

# Generate report only from existing results
python scripts/run_pipeline.py "||" --output output_dir --report-only
`

---

##  Architecture

`
User Input (Natural Language)
        |
        |
||||||||||
|   task_parser    |  Parses location, time, task, parameters
||||||||||
         |
         |
||||||||||
|  generate_gee    |  Generates GEE JavaScript/Python code
|                  |   Indices analysis
|                  |   Classification
|  + data_sources  |   Change detection
|                  |   Time series
||||||||||
         |
         |
||||||||||
|  run_pipeline    |  Orchestrates full pipeline execution
||||||||||
         |
          GEE Code (.js)
          Task Execution (optional)
         |
         |
||||||||||
| generate_report  |  Generates MD/HTML report
||||||||||
         |
         |
   Final Output:
   | GeoTIFF files
   | CSV statistics
   | Accuracy assessment
   | Charts/Visualizations
   | Experiment report (MD/HTML)
`

---

## | Project Structure

`
GEE-AutoLab/
| SKILL.md                       # Skill definition (Codex)
| README.md                      # English documentation
| README_CN.md                   # Chinese documentation
| LICENSE                        # MIT License
| CITATION.cff                   # Citation information
| requirements.txt               # Python dependencies
| scripts/
|   | run_pipeline.py            # Main entry point
|   | task_parser.py             # Natural language parser
|   | generate_gee.py            # GEE code generator
|   | generate_report.py         # Report generator
|   | check_gee.py               # Environment checker
| templates/
|   | report.md                  # Report template
| references/
|   | data_sources.md            # Dataset reference (50+ datasets)
| examples/
    | ndvi_analysis.md           # NDVI analysis example
    | classification.md          # Land cover classification example
    | change_detection.md        # Change detection example
    | timeseries.md             # Time series analysis example
`

---

## | Supported Data Sources

### Optical Data
| Dataset | ID | Resolution |
|---------|-----|------------|
| Sentinel-2 MSI SR | COPERNICUS/S2_SR | 10m |
| Sentinel-2 MSI TOA | COPERNICUS/S2 | 10m |
| Sentinel-2 MSI SR (Harmonized) | COPERNICUS/S2_SR_HARMONIZED | 10m |
| Landsat 8-9 OLI/TIRS SR | LANDSAT/LC08/C02/T1_L2 | 30m |
| Landsat 7 ETM+ SR | LANDSAT/LE07/C02/T1_L2 | 30m |
| Landsat 4-5 TM SR | LANDSAT/LT05/C02/T1_L2 | 30m |
| Landsat Collection 1 SR | LANDSAT/LC08/C01/T1_SR | 30m |
| MODIS MOD09GA | MODIS/006/MOD09GA | 500m |
| MODIS MOD09Q1 | MODIS/006/MOD09Q1 | 250m |
| MODIS MOD13Q1 | MODIS/006/MOD13Q1 | 250m |

### SAR Data
| Dataset | ID | Resolution |
|---------|-----|------------|
| Sentinel-1 GRD | COPERNICUS/S1_GRD | 10m |
| ALOS PALSAR | JAXA/ALOS/PALSAR/YEARLY/SAR | 25m |

### Climate & Weather
| Dataset | ID | Resolution |
|---------|-----|------------|
| GPM IMERG | NASA/GPM_L3_IMERG_V06 | 10km |
| ERA5 Monthly | ECMWF/ERA5_LAND/MONTHLY | 11km |
| CHIRPS Daily | UCSB-CHG/CHIRPS/DAILY | 5km |
| MODIS LST | MODIS/006/MOD11A2 | 1km |
| GRIDMET | IDAHO_EPSCOR/GRIDMET | 4km |

### Land Cover
| Dataset | ID | Resolution |
|---------|-----|------------|
| ESA WorldCover | ESA/WorldCover/v200 | 10m |
| Hansen Global Forest | UMD/hansen/global_forest_change_v1_11 | 30m |
| JRC Global Surface Water | JRC/GSW1_4/GlobalSurfaceWater | 30m |
| MODIS Land Cover | MODIS/006/MCD12Q1 | 500m |
| Copernicus CORINE | COPERNICUS/CORINE/V20_100 | 100m |

### Terrain
| Dataset | ID | Resolution |
|---------|-----|------------|
| SRTM Digital Elevation | USGS/SRTMGL1_003 | 30m |
| Copernicus DEM | COPERNICUS/DEM/GLO30 | 30m |
| NASADEM | NASA/NASADEM_HGT/001 | 30m |

### Fire & Thermal
| Dataset | ID | Resolution |
|---------|-----|------------|
| MODIS Fire/Months | MODIS/006/MOD14A2 | 1km |
| VIIRS S-NPP Fire | VIIRS/VNP14IMG | 375m |
| MODIS Thermal | MODIS/006/MOD11A2 | 1km |

### Nightlight
| Dataset | ID | Resolution |
|---------|-----|------------|
| NPP-VIIRS VNP46A4 | VIIRS/VNP46A4 | 500m |
| DMSP-OLS | NOAA/DMSP-OLS/NIGHTTIME_LIGHTS | 1km |

---

## | Example Output

### NDVI Analysis Report
- **Location**: Wuhan, China
- **Data**: Sentinel-2 SR (10m resolution)
- **Period**: 2023-01-01 to 2023-12-31
- **Indices**: NDVI, EVI, MNDWI
- **Results**:
  - Mean NDVI: 0.45 (range: -0.12 to 0.89)
  - Vegetation coverage: 62.3% of study area
  - Water area: 8.7% (derived from MNDWI)
- **Exports**: GeoTIFF x 3, CSV x 1

### Land Cover Classification (Random Forest)
- **Overall Accuracy**: 92.4%
- **Kappa Coefficient**: 0.89
- **Classes**: 6 land cover types
- **Exports**: Classified GeoTIFF + Accuracy table (CSV)

---

## | Customization

### Adding Custom Datasets
Edit 
eferences/data_sources.md to add dataset entries:
`yaml
- name: My Custom Dataset
  id: PATH/TO/DATASET
  resolution: 30
  type: optical
  tasks: [classification, indices]
`

### Creating Custom Templates
Edit 	emplates/report.md to customize report format and content.

---

## | Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

---

## | License

Distributed under the MIT License. See LICENSE for more information.

## | Citation

`ibtex
@software{gee_autolab,
  author = {{GEE AutoLab Contributors}},
  title = {GEE AutoLab: Automated Remote Sensing Research Assistant},
  year = {2025},
  url = {https://github.com/xingguangYan/GEE-AutoLab}
}
`

## | Acknowledgments

- Google Earth Engine for providing the powerful cloud computing platform
- SAT-IO community for the extended dataset catalog
- ESA, NASA, USGS, JAXA for open Earth observation data
- [CSDN Blog Reference](https://blog.csdn.net/qq_31988139)
