# GEE AutoLab — Complete GEE Dataset Reference

> Comprehensive catalog integrating **Google Earth Engine Official Catalog**,  
> **SAT-IO Community Datasets**, and **Awesome GEE Community Datasets**.  
> Sources:
> - [GEE Official Catalog](https://developers.google.com/earth-engine/datasetshl=zh-cn)
> - [SAT-IO Community Catalog](https://developers.google.com/earth-engine/datasets/community/sat-iohl=zh-cn)
> - [Awesome GEE Community Datasets](https://github.com/samapriya/awesome-gee-community-datasets)
> - [GEE Getting Started Guide](https://developers.google.com/earth-engine/guides/getstartedhl=zh-cn)

---

## 📖 How to Use These Datasets

All datasets are accessed via `ee.ImageCollection("dataset_id")` in Python API.

**Basic workflow:**
```python
import ee
ee.Initialize()

# Load a dataset
col = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
  .filterBounds(roi)
  .filterDate("2023-01-01", "2023-12-31")

# Apply mask
def mask(img):
    scl = img.select("SCL")
    return img.updateMask(scl.neq(3).And(scl.neq(8).And(scl.neq(9).And(scl.neq(10))))).divide(10000)

cleaned = col.map(mask).median().clip(roi)
```

For more details: [GEE Get Started](https://developers.google.com/earth-engine/guides/getstartedhl=zh-cn) | [Python API Guide](https://developers.google.com/earth-engine/guides/python_installhl=zh-cn)

---

## 🏆 Official GEE Datasets (Most Used)

### 🌿 Optical Satellites — High Resolution

| Dataset | GEE ID | Resolution | Bands | Revisit | Coverage |
|---------|--------|-----------|-------|---------|----------|
| **Sentinel-2 SR** | `COPERNICUS/S2_SR_HARMONIZED` | 10m / 20m | B1-B12, AOT, WVP, SCL | 5 days | Global (2017-) |
| **Sentinel-2 TOA** | `COPERNICUS/S2_HARMONIZED` | 10m / 20m | B1-B12, QA10, QA20, QA60 | 5 days | Global (2017-) |
| **Landsat 8/9 SR** | `LANDSAT/LC08/C02/T1_L2` | 30m (pan 15m) | SR_B1-B7, ST_B10, QA_PIXEL | 8 days | Global (2013-) |
| **Landsat 9 SR** | `LANDSAT/LC09/C02/T1_L2` | 30m (pan 15m) | SR_B1-B7, ST_B10, QA_PIXEL | 8 days | Global (2021-) |
| **Landsat 7 SR** | `LANDSAT/LE07/C02/T1_L2` | 30m (pan 15m) | SR_B1-B7, ST_B10, QA_PIXEL | 16 days | Global (1999-) |
| **Landsat 5 SR** | `LANDSAT/LT05/C02/T1_L2` | 30m | SR_B1-B7, QA_PIXEL | 16 days | Global (1984-2012) |
| **Landsat 4 SR** | `LANDSAT/LT04/C02/T1_L2` | 30m | SR_B1-B5, B7, QA_PIXEL | 16 days | Global (1982-1993) |
| **Landsat 8/9 TOA** | `LANDSAT/LC08/C02/T1_TOA` | 30m | B1-B11, BQA | 8 days | Global (2013-) |

### 🌿 Optical Satellites — Medium / Coarse Resolution

| Dataset | GEE ID | Resolution | Bands | Time Range |
|---------|--------|-----------|-------|-----------|
| **MODIS Terra NDVI** | `MODIS/061/MOD13Q1` | 250m | NDVI, EVI, pixel_reliability | 2000- |
| **MODIS Aqua NDVI** | `MODIS/061/MYD13Q1` | 250m | NDVI, EVI, pixel_reliability | 2002- |
| **MODIS Terra Reflectance** | `MODIS/061/MOD09GA` | 500m | B1-B7, solar_azimuth, state_1km | 2000- |
| **MODIS Vegetation Indices** | `MODIS/061/MOD13A2` | 1km | NDVI, EVI, VI_Quality | 2000- |
| **MODIS LAI/FPAR** | `MODIS/061/MCD15A3H` | 500m | LAI, FPAR | 2002- |
| **MODIS GPP/NPP** | `MODIS/061/MOD17A2H` | 500m | GPP, GPP_QC | 2000- |
| **MODIS NPP** | `MODIS/061/MOD17A3HGF` | 500m | NPP, NPP_QC | 2000- |
| **MODIS LST** | `MODIS/061/MOD11A2` | 1km | LST_Day, LST_Night | 2000- |
| **MODIS LST (Aqua)** | `MODIS/061/MYD11A2` | 1km | LST_Day, LST_Night | 2002- |
| **MODIS Fire** | `MODIS/061/MOD14A1` | 1km | FireMask, MaxFRP | 2000- |
| **VIIRS SDR** | `VIIRS/VNP02IMG` | 375m | I1-I5, M1-M11 | 2012- |
| **VIIRS Fire** | `VIIRS/VNP14A1` | 375m | FireMask, MaxFRP | 2012- |
| **VIIRS DNB Nightlight** | `NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG` | 500m | avg_rad, cf_cvg | 2014- |
| **DMSP-OLS Nightlight** | `NOAA/DMSP-OLS/NIGHTTIME_LIGHTS` | 30 arcsec | stable_lights, avg_lights | 1992-2013 |

### 📡 SAR (Synthetic Aperture Radar)

| Dataset | GEE ID | Resolution | Polarization | Time Range |
|---------|--------|-----------|-------------|-----------|
| **Sentinel-1 GRD** | `COPERNICUS/S1_GRD` | 10m | VV, VH, HH, HV | 2014- |
| **Sentinel-1 SLC** | `COPERNICUS/S1_SLC` | 2.7-22m | VV, VH | 2014- |
| **ALOS PALSAR** | `JAXA/ALOS/PALSAR/YEARLY/SAR` | 25m | HH, HV | 2006-2011 |
| **ALOS-2 PALSAR-2** | `JAXA/ALOS2/PALSAR2/LEVEL2_2/SCENE` | 10m | HH, HV, VV, VH | 2014- |
| **JERS-1 SAR** | `JERS-1/SAR` | 100m | HH | 1992-1998 |

### ⛰️ DEM & Terrain

| Dataset | GEE ID | Resolution | Description |
|---------|--------|-----------|-------------|
| **SRTM** | `USGS/SRTMGL1_003` | 30m | Global 30m DEM |
| **SRTM (90m)** | `USGS/SRTMGL1_003` | 90m | Resampled |
| **NASADEM** | `NASA/NASADEM_HGT/001` | 30m | Improved SRTM |
| **Copernicus DEM GLO30** | `COPERNICUS/DEM/GLO30` | 30m | EU high-accuracy DEM |
| **Copernicus DEM GLO90** | `COPERNICUS/DEM/GLO90` | 90m | Global DEM |
| **ALOS AW3D30** | `JAXA/ALOS/AW3D30/V3_2` | 30m | Japan high-accuracy DSM |
| **GMTED2010** | `USGS/GMTED2010` | 250m | Global multi-resolution DEM |
| **MERIT DEM** | `MERIT/DEM/v1` | 90m | Multi-error-removed DEM |
| **HydroSHEDS** | `WWF/HydroSHEDS/v1` | 90m | Hydro-conditioned DEM |

### 🌡️ Climate & Weather

| Dataset | GEE ID | Resolution | Variables | Time Range |
|---------|--------|-----------|-----------|-----------|
| **ERA5 Daily** | `ECMWF/ERA5/DAILY` | 0.25deg | T2m, Precip, Wind, Pressure | 1979- |
| **ERA5 Land** | `ECMWF/ERA5_LAND/DAILY` | 0.1deg | Soil moisture, T2m, Precip | 1981- |
| **CHIRPS Daily** | `UCSB-CHG/CHIRPS/DAILY` | 0.05deg | Precipitation | 1981- |
| **CHIRPS Pentad** | `UCSB-CHG/CHIRPS/PENTAD` | 0.05deg | Precipitation (5-day) | 1981- |
| **GPM IMERG** | `NASA/GPM_L3_IMERG_V06` | 0.1deg | Precipitation | 2000- |
| **GRIDMET** | `IDAHO_EPSCOR/GRIDMET` | 4km | Tmax, Tmin, Precip, VPD, PET | 1979- |
| **NLDAS-2** | `NASA/NLDAS/FORA0125_H002` | 0.125deg | Temperature, Humidity, Wind | 1979- |
| **Daymet** | `NASA/ORNL/DAYMET_V4` | 1km | Tmax, Tmin, Precip, Solar | 1980- |
| **MODIS LST** | `MODIS/061/MOD11A2` | 1km | LST Day/Night | 2000- |
| **OpenLandMap LST** | `projects/sat-io/open-datasets/LST` | 1km | Gap-filled LST | 2013- |

### 💧 Water & Hydrology

| Dataset | GEE ID | Resolution | Description |
|---------|--------|-----------|-------------|
| **JRC Global Surface Water** | `JRC/GSW1_4/GlobalSurfaceWater` | 30m | Occurrence, change, seasonality, transitions |
| **JRC Monthly Water** | `JRC/GSW1_4/MonthlyHistory` | 30m | Monthly water detection (1984-2021) |
| **JRC Monthly Recurrence** | `JRC/GSW1_4/MonthlyRecurrence` | 30m | Monthly water recurrence |
| **HydroSHEDS** | `WWF/HydroSHEDS/v1` | 90m | Flow accumulation, direction, river network |
| **Global Flood DB** | `GLOBAL_FLOOD_DB/MODIS_EV5/V1` | 250m | MODIS-based flood events |

### 🌲 Land Cover & Vegetation

| Dataset | GEE ID | Resolution | Classes | Year |
|---------|--------|-----------|---------|------|
| **ESA WorldCover** | `ESA/WorldCover/v200` | 10m | 11 classes | 2020-2021 |
| **MCD12Q1 (IGBP)** | `MODIS/061/MCD12Q1` | 500m | 17 classes | 2001- |
| **MCD12Q1 (UMD)** | `MODIS/061/MCD12Q1` | 500m | 14 classes | 2001- |
| **MCD12Q1 (LAI)** | `MODIS/061/MCD12Q1` | 500m | 8 classes | 2001- |
| **GlobeLand30** | `projects/sat-io/open-datasets/GlobeLand30` | 30m | 10 classes | 2000, 2010, 2020 |
| **Global Forest Change** | `UMD/hansen/global_forest_change_2023_v1_11` | 30m | Tree cover, loss, gain | 2000-2022 |
| **Global Mangrove Watch** | `projects/sat-io/open-datasets/GlobalMangroveWatch` | 25m | Mangrove extent | 1996-2020 |
| **Global Surface Water Dynamics** | `JRC/GSW1_4/GlobalSurfaceWater` | 30m | Water transitions | 1984-2021 |
| **CORINE Land Cover** | `COPERNICUS/CORINE/V20_100` | 100m | 44 classes | 2000-2018 |
| **Global Impervious Surface** | `GAIA/GAIA/v1` | 30m | Impervious percentage | 1985-2018 |

### 🔥 Fire & Thermal

| Dataset | GEE ID | Resolution | Description |
|---------|--------|-----------|-------------|
| **MODIS Thermal** | `MODIS/061/MOD11A2` | 1km | LST Day/Night |
| **MODIS Fire** | `MODIS/061/MOD14A1` | 1km | Fire mask + FRP |
| **MODIS Thermal (Aqua)** | `MODIS/061/MYD14A1` | 1km | Fire mask + FRP |
| **VIIRS Fire** | `VIIRS/VNP14A1` | 375m | Active fire |
| **VIIRS Thermal** | `VIIRS/VNP21A1D` | 375m | LST |
| **FIRMS** | `FIRMS` | 375m/1km | Fire information |
| **FireCCI** | `ESA/CCI/FireCCI/5_1` | 250m | Burned area |
| **Gap-filled LST** | `projects/sat-io/open-datasets/gap-filled-lst` | 1km | Gap-filled LST day/night |

### 🌍 Global & Thematic

| Dataset | GEE ID | Resolution | Description |
|---------|--------|-----------|-------------|
| **ESA WorldCover** | `ESA/WorldCover/v200` | 10m | 2020 global land cover |
| **Global Forest Change** | `UMD/hansen/global_forest_change_2023_v1_11` | 30m | Hansen forest |
| **JRC Water** | `JRC/GSW1_4/GlobalSurfaceWater` | 30m | Surface water |
| **Global Human Settlement** | `JRC/GHSL/P2023A/GHS_BUILT_S` | 100m | Built-up surface |
| **Global Human Settlement (Population)** | `JRC/GHSL/P2023A/GHS_POP` | 100m | Population grid |
| **WorldPop** | `WorldPop/GP/100m/pop` | 100m | Population count |
| **Global Mangrove Watch** | `projects/sat-io/open-datasets/GlobalMangroveWatch` | 25m | Mangrove |
| **Global Tidal Wetlands** | `projects/sat-io/open-datasets/GCW/v1` | 10m | Tidal wetlands |
| **Global Surface Water Change** | `JRC/GSW1_4/GlobalSurfaceWater` | 30m | Water change |
| **Global Shoreline** | `projects/sat-io/open-datasets/shoreline` | Vector | Global coastlines |
| **Global Habitat Types** | `projects/sat-io/open-datasets/IUCN_HABITAT` | 100m | IUCN habitat maps |

---

## 🇨🇳 China-Specific Datasets (SAT-IO Community)

| Dataset | GEE ID | Resolution | Description |
|---------|--------|-----------|-------------|
| **China Admin 2022** | `projects/sat-io/open-datasets/CN/CHN_ADMIN_2022` | Vector | Province-City-District boundaries |
| **China Land Cover (CLCD)** | `projects/sat-io/open-datasets/CN/LANDCOVER/CLCD` | 30m | Annual land cover (1985-2022) |
| **China GDP Grid** | `projects/sat-io/open-datasets/CN/GDP` | 1km | GDP spatial distribution |
| **China Population Grid** | `projects/sat-io/open-datasets/CN/POP` | 100m | Population density |
| **China Building Footprints** | `projects/sat-io/open-datasets/VIDA_COMBINED/CHN` | Vector | Google+Microsoft combined |
| **China Building Attribute** | `projects/sat-io/open-datasets/JRC/GHS-OBAT/GHS_OBAT_GPKG_CHN_E2020_R2024A_V1_0` | Vector | GHS building attributes |
| **China Soil Map** | `projects/sat-io/open-datasets/CN/Soil` | 250m | Soil properties |
| **China Urban Extent** | `projects/sat-io/open-datasets/CN/UrbanExtent` | 30m | Urban expansion |
| **China Cropland** | `projects/sat-io/open-datasets/CN/Cropland` | 30m | Cropland distribution |
| **China Forest Cover** | `projects/sat-io/open-datasets/CN/ForestCover` | 30m | Forest/non-forest |
| **FAO GAUL Admin (Global)** | `FAO/GAUL/2015/level0-2` | Vector | Country/province/district |
| **Global Administrative Boundaries** | `FAO/GAUL/2015/level0-2` | Vector | Global admin units |

---

## 🧠 SAT-IO Community Datasets by Category

### 🏙️ Urban & Infrastructure

| Dataset | GEE ID | Description |
|---------|--------|-------------|
| **Global Urban Footprint** | `projects/sat-io/open-datasets/GUF/GUF12` | 12m global urban extent |
| **Global Impervious Surface** | `projects/sat-io/open-datasets/GAIA` | 30m impervious (1985-2018) |
| **Global Building Footprints** | `projects/sat-io/open-datasets/VIDA_COMBINED` | Google+Microsoft combined |
| **GHS Built-up Surface** | `projects/sat-io/open-datasets/JRC/GHS-BUILT` | 100m global built-up |
| **Solar Energy US** | `projects/sat-io/open-datasets/GMSEUS` | Solar panel arrays |

### 🌿 Ecology & Biodiversity

| Dataset | GEE ID | Description |
|---------|--------|-------------|
| **IUCN Habitat Maps** | `projects/sat-io/open-datasets/IUCN_HABITAT` | Global habitat classification |
| **Global Tidal Wetlands** | `projects/sat-io/open-datasets/GCW` | 10m tidal wetland map |
| **Global Mangrove Watch** | `projects/sat-io/open-datasets/GlobalMangroveWatch` | Mangrove extent time series |
| **Geo-BON Ecosystem** | `projects/sat-io/open-datasets/GEOBON` | Ecosystem functional types |
| **Western Himalaya Canopy** | `projects/sat-io/open-datasets/WHICH_MAP` | Canopy height (Pakistan) |
| **Global Habitat Types** | `projects/sat-io/open-datasets/IUCN_HABITAT` | Level 1/2 v004 |

### 🌲 Forest & Carbon

| Dataset | GEE ID | Description |
|---------|--------|-------------|
| **GEDI Canopy Height** | `projects/sat-io/open-datasets/GLAD/GEDI_V27` | Global 30m canopy height |
| **GEDI Boreal** | `projects/sat-io/open-datasets/GLAD/GEDI_V25_Boreal` | Boreal forest height |
| **CA Forest Canopy** | `projects/sat-io/open-datasets/CA_FOREST` | California forest height |
| **Irrecoverable Carbon** | `projects/sat-io/open-datasets/irrecoverable_carbon` | Irrecoverable carbon stocks |
| **Vulnerable Carbon** | `projects/sat-io/open-datasets/vulnerable_carbon` | Vulnerable carbon biomass |
| **Manageable Carbon** | `projects/sat-io/open-datasets/manageable_carbon` | Manageable carbon stocks |

### 🌡️ Climate & LST

| Dataset | GEE ID | Description |
|---------|--------|-------------|
| **Gap-filled LST Day** | `projects/sat-io/open-datasets/gap-filled-lst/gf_day_1km` | 1km gap-filled daytime LST |
| **Gap-filled LST Night** | `projects/sat-io/open-datasets/gap-filled-lst/gf_night_1km` | 1km gap-filled nighttime LST |
| **ERA5 Agriculture** | `projects/climate-engine-pro/assets/ce-ag-era5-v2/daily` | ERA5 agri variables |
| **ERA5 Heat Stress** | `projects/climate-engine-pro/assets/ce-era5-heat` | ERA5 heat indices |
| **CHIRPS Prelim** | `projects/climate-engine-pro/assets/ce-chirps-prelim-pentad` | Preliminary CHIRPS |
| **CMORPH Precip** | `projects/climate-engine-pro/assets/noaa-cpc-cmorph/daily` | CMORPH precipitation |
| **Climate Engine** | `projects/climate-engine-pro/assets/*` | Various CE assets |

---

## 📚 GEE Documentation References

### Official Guides

| Topic | Link |
|-------|------|
| **Getting Started** | [developers.google.com/earth-engine/guides/getstarted](https://developers.google.com/earth-engine/guides/getstartedhl=zh-cn) |
| **Python Installation** | [developers.google.com/earth-engine/guides/python_install](https://developers.google.com/earth-engine/guides/python_installhl=zh-cn) |
| **Data Catalog** | [developers.google.com/earth-engine/datasets](https://developers.google.com/earth-engine/datasetshl=zh-cn) |
| **SAT-IO Community Catalog** | [developers.google.com/earth-engine/datasets/community/sat-io](https://developers.google.com/earth-engine/datasets/community/sat-iohl=zh-cn) |
| **Awesome GEE Community** | [github.com/samapriya/awesome-gee-community-datasets](https://github.com/samapriya/awesome-gee-community-datasets) |

### Key API References

| API | Description |
|-----|-------------|
| `ee.Image()` | Single image operations |
| `ee.ImageCollection()` | Collection filtering, compositing |
| `ee.FeatureCollection()` | Vector data handling |
| `ee.Reducer` | Statistics: mean, sum, minMax, linearFit |
| `ee.Classifier` | ML: RandomForest, CART, SVM |
| `ee.Filter` | Spatial/temporal filtering |
| `ee.Algorithms.LandTrendr` | Time-series segmentation |
| `ee.Algorithms.TemporalSegmentation.CCDC` | Continuous monitoring |
| `ee.batch.Export` | Export to Drive, Cloud Storage, or Asset |

### Cloud Masking Reference

**Sentinel-2 (SCL band):**
```
SCL values: 0=None, 1=Sat, 2=Dark, 3=Cloud_shadow, 4=Vegetation,
5=Soil, 6=Water, 7=Low_cloud, 8=Medium_cloud, 9=High_cloud, 10=Cirrus, 11=Snow
Mask: scl.neq(3).And(scl.neq(8).And(scl.neq(9).And(scl.neq(10))))
```

**Landsat (QA_PIXEL band):**
```
Bit 0: Fill, Bit 1: Dilated Cloud, Bit 2: Cirrus, Bit 3: Cloud,
Bit 4: Cloud Shadow, Bit 5: Snow, Bit 6: Clear, Bit 7: Water
Mask: qa.bitwiseAnd(1<<3).eq(0).And(qa.bitwiseAnd(1<<4).eq(0))
```

**MODIS (SummaryQA / pixel_reliability):**
```
0: Good, 1: Marginal, 2: Snow/Ice, 3: Cloudy
Mask: qa.lte(1)
```

---

## 🎯 Auto-Selection Rules (Implemented in task_parser.py)

The task parser uses these rules to auto-select datasets:

| User Task | Auto-selected Dataset | Scale |
|-----------|----------------------|-------|
| NDVI/EVI/LST | Sentinel-2 SR | 10m |
| Classification (fine) | Sentinel-2 SR | 10m |
| Classification (coarse) | Landsat 8/9 SR | 30m |
| Change Detection | Sentinel-2 + Landsat 8 | 10/30m |
| Time Series | MODIS NDVI | 250m |
| Fire | MODIS Fire + VIIRS | 1km |
| Water | Sentinel-2 / JRC | 10/30m |
| Urban | Sentinel-2 / VIIRS DNB | 10/500m |
| SAR | Sentinel-1 GRD | 10m |
| DEM | SRTM / Copernicus | 30m |
| Precipitation | GPM IMERG | 10km |
| Temperature | MODIS LST / ERA5 | 1km/0.25deg |

User-specified dataset always overrides auto-selection.

---

*Last updated: 2026-06-15 | For task-specific auto-selection rules, see SKILL.md | Sources: GEE Official, SAT-IO Community, Awesome GEE*
