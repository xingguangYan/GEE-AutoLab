# GEE AutoLab - 全自动遥感科研助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GEE](https://img.shields.io/badge/Earth%20Engine-API-green.svg)](https://earthengine.google.com/)

> **GEE AutoLab** 是一个基于Google Earth Engine的全自动遥感分析 Agent。

用户只需输入自然语言描述（时间+地点+任务），
即可自动完成数据检索、GEE脚本生成、
指数/分类/变化检测分析、GeoTIFF/CSV导出
以及实验报告生成的全流程。

---

## 核心功能

### 零代码操作
- **自然语言输入**: 用中文或英文描述分析需求
- **自动参数补全**: 缺失参数自动使用智能默认值
- **一键执行**: 从查询到完整科学报告一条命令

### 全面数据源支持
- **Official GEE Datasets**: 完整支持50+个公开数据集（Sentinel,Landsat,MODIS,VIIRS,GPM,SRTM,ERA5等）
- **SAT-IO Community Catalog**: 扩展支持社区贡献的数据集
- **智能自动选择**: 根据任务类型和分辨率自动匹配
- **自定义数据集**: 用户可指定任意GEE数据集ID

### 12 大分析任务
1. **植被指数** - NDVI, EVI, NDWI, MNDWI, NDBI, NDMI, SAVI, GCI, RECI, NBR, PSRI, SIPI, ARVI, GNDVI, NDRE, MSAVI
2. **水体与湿地** - 水体提取、面积统计、湿地分类
3. **土地覆盖分类** - Random Forest, CART, SVM
4. **变化检测** - LandTrendr, CCDC, 差分
5. **时间序列** - 合成、趋势、物候
6. **城市与夜光** - 城市扩张、NPP-VIIRS
7. **森林与碳汇** - 森林覆盖、生物量
8. **灾害监测** - MODIS/VIIRS 火点、洪水、旱情
9. **地形与DEM** - 高程、坡度、流域
10. **气象与气候** - 降水、气温、蒸散
11. **SAR 分析** - Sentinel-1 GRD, 水域检测
12. **综合统计** - 面积统计、Zonal Statistics

---

## 快速开始

### 安装
```bash
git clone https://github.com/xingguangYAN/GEE-AutoLab.git
cd GEE-AutoLab
pip install -r requirements.txt
earthengine authenticate
python scripts/check_gee.py
```

### 使用示例

**示例1**
```bash
python scripts/run_pipeline.py "在武汉市2023年计算NDVI和EVI" --output result_wuhan
```

**示例2**
```bash
python scripts/run_pipeline.py "黑龙江2022土地覆盖分类Random Forest" --output result_heilongjiang
```

**示例3**
```bash
python scripts/run_pipeline.py "云南省2018-2023森林变化检测" --output result_yunnan_forest
```

---

## 项目结构

```
GEE-AutoLab/
+-- SKILL.md
+-- README.md / README_CN.md
+-- LICENSE / CITATION.cff / requirements.txt
+-- scripts/ (5 files)
+-- templates/ (1 file)
+-- references/ (1 file)
+-- examples/ (4 files)
```

---

## License

MIT License

## Citation

```bibtex
@software{gee_autolab,
  author = {{GEE AutoLab Contributors}},
  title = {GEE AutoLab: Automated Remote Sensing Research Assistant},
  year = {2025},
  url = {https://github.com/xingguangYAN/GEE-AutoLab}
}
```
