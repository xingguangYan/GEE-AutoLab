# GEE AutoLab - 全自动遥感科研助手

> **GEE AutoLab** 是一个基于 Google Earth Engine 的全自动遥感分析Agent
> 用户只需输入时间地点任务三要素，即可自动完成数据检索 -> GEE 脚本生成 -> 指数分类变化检测分析 -> GeoTIFF/CSV 导出 -> 实验报告生成的全流程

---

## 触发关键词

```
trigger_terms:
  - GEE 自动化
  - 遥感分析自动
  - 一键遥感
  - GEE 实验
  - Earth Engine 分析
  - gee auto
  - auto gee
  - auto gee lab
```

---

## 支持的任务类型 (12)

1. **植被指数分析** - NDVI, EVI, NDWI, MNDWI, NDBI, NDMI, SAVI, GCI, RECI, NBR
2. **水体与湿地分析** - 水体提取面积统计湿地分类
3. **土地覆盖分类** - Random Forest, CART, SVM, Gradient Boosted Trees
4. **变化检测** - LandTrendr, CCDC, 双期差分检测
5. **时间序列分析** - 年度月度合成趋势分析物候参数
6. **城市与夜光分析** - 城市扩张不透水面NPP-VIIRS夜光
7. **森林与碳汇分析** - 森林覆盖生物量估算碳储量
8. **灾害监测** - MODIS/VIIRS 火点洪水旱情
9. **地形与DEM分析** - 高程坡度流域划分
10. **气象与气候分析** - 降水气温蒸散量旱旱指数
11. **SAR 分析** - Sentinel-1 GRD 水体检测船只检测
12. **综合统计** - 面积统计Zonal Statistics图表

---

## 默认参数

| 参数 | 默认值 |
|---:|---:|
| 空间分辨率 | 10m / 30m |
| 云量阈值 | 20% |
| 合成方法 | 中值合成 |
| 分类器 | Random Forest |
| RF 树数量 | 100 |
| 导出CRS | EPSG:4326 |
| 导出文件夹 | GEE_Exports |

---

## License

MIT 许可证
