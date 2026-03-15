# PPT XML 参考（Office Open XML）

## 概述

当需要以编程方式生成 PowerPoint 文件时，可使用 Office Open XML (OOXML) 格式。
Python 中推荐使用 `python-pptx` 库。

## python-pptx 基础结构

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Cm, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.chart import XL_CHART_TYPE

# 创建演示文稿
prs = Presentation()
prs.slide_width = Cm(33.87)   # 16:9 宽屏
prs.slide_height = Cm(19.05)
```

## 常用操作

### 添加幻灯片
```python
# 使用空白版式
blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)
```

### 添加文本框
```python
from pptx.util import Inches, Pt

txBox = slide.shapes.add_textbox(
    left=Cm(1.5),
    top=Cm(1.0),
    width=Cm(30),
    height=Cm(2.0)
)
tf = txBox.text_frame
tf.word_wrap = True

# 标题段落
p = tf.paragraphs[0]
p.text = "标题文本"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
p.font.name = "微软雅黑"
p.alignment = PP_ALIGN.LEFT
```

### 添加表格
```python
rows, cols = 6, 5
table_shape = slide.shapes.add_table(
    rows, cols,
    left=Cm(1.5),
    top=Cm(4.0),
    width=Cm(30),
    height=Cm(10)
)
table = table_shape.table

# 设置表头
headers = ["指标", "2022A", "2023A", "2024A", "2025E"]
for i, header in enumerate(headers):
    cell = table.cell(0, i)
    cell.text = header
    # 表头格式
    for paragraph in cell.text_frame.paragraphs:
        paragraph.font.size = Pt(11)
        paragraph.font.bold = True
        paragraph.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    # 表头背景色
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(0x00, 0x33, 0x66)

# 填充数据
data = [
    ["营业收入(亿)", "100.0", "120.0", "145.0", "170.0"],
    ["净利润(亿)", "30.0", "38.0", "46.0", "55.0"],
    ["毛利率", "45.0%", "46.2%", "47.1%", "48.0%"],
    ["ROE", "18.5%", "19.2%", "20.1%", "21.0%"],
    ["PE(x)", "25.0", "22.0", "18.5", "15.2"],
]
for row_idx, row_data in enumerate(data):
    for col_idx, value in enumerate(row_data):
        cell = table.cell(row_idx + 1, col_idx)
        cell.text = value
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(10)
            paragraph.font.name = "Arial"
            # 预测数据用蓝色
            if col_idx == 4:
                paragraph.font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
```

### 添加图表
```python
from pptx.chart.data import CategoryChartData

# 柱状图
chart_data = CategoryChartData()
chart_data.categories = ['2022A', '2023A', '2024A', '2025E', '2026E']
chart_data.add_series('营业收入', (100, 120, 145, 170, 195))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    left=Cm(1.5),
    top=Cm(4.0),
    width=Cm(15),
    height=Cm(10),
    chart_data=chart_data
).chart

# 设置颜色
plot = chart.plots[0]
series = plot.series[0]
series.format.fill.solid()
series.format.fill.fore_color.rgb = RGBColor(0x00, 0x33, 0x66)

# 添加数据标签
series.has_data_labels = True
series.data_labels.font.size = Pt(9)
series.data_labels.number_format = '#,##0'
```

### 添加形状和线条
```python
from pptx.enum.shapes import MSO_SHAPE

# 矩形
shape = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    left=Cm(2), top=Cm(5),
    width=Cm(8), height=Cm(3)
)
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0xE8, 0xF0, 0xFE)
shape.line.fill.background()  # 无边框

# 箭头连接线
connector = slide.shapes.add_connector(
    1,  # 直线连接器
    Cm(10), Cm(6.5),  # 起点
    Cm(15), Cm(6.5)   # 终点
)
connector.line.color.rgb = RGBColor(0x00, 0x33, 0x66)
connector.line.width = Pt(1.5)
```

## 颜色常量定义

```python
# 投行路演常用颜色
class IBColors:
    DARK_BLUE = RGBColor(0x00, 0x33, 0x66)
    MID_BLUE = RGBColor(0x00, 0x66, 0xCC)
    LIGHT_BLUE = RGBColor(0x66, 0xAA, 0xDD)
    RED = RGBColor(0xCC, 0x00, 0x00)
    GREEN = RGBColor(0x00, 0x66, 0x33)
    GRAY = RGBColor(0x66, 0x66, 0x66)
    LIGHT_GRAY = RGBColor(0xE5, 0xE7, 0xEB)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    BLACK = RGBColor(0x00, 0x00, 0x00)
    GOLD = RGBColor(0xDA, 0xA5, 0x20)
```

## 完整页面生成示例

```python
def create_financial_summary_slide(prs, company_name, financial_data):
    """创建财务概览页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 标题
    title_box = slide.shapes.add_textbox(Cm(1.5), Cm(0.8), Cm(30), Cm(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"{company_name}：盈利能力持续提升，ROE 达到行业领先水平"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = IBColors.DARK_BLUE

    # 分隔线
    line = slide.shapes.add_connector(
        1, Cm(1.5), Cm(2.5), Cm(32), Cm(2.5)
    )
    line.line.color.rgb = IBColors.MID_BLUE
    line.line.width = Pt(1)

    # 财务数据表格
    # ... (添加表格代码)

    # 来源标注
    source_box = slide.shapes.add_textbox(Cm(1.5), Cm(17.5), Cm(20), Cm(1))
    tf = source_box.text_frame
    p = tf.paragraphs[0]
    p.text = "来源：公司公告, cn-financial-mcp"
    p.font.size = Pt(8)
    p.font.color.rgb = IBColors.GRAY

    # 页码
    page_box = slide.shapes.add_textbox(Cm(30), Cm(17.5), Cm(3), Cm(1))
    tf = page_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"P.{len(prs.slides)}"
    p.font.size = Pt(8)
    p.font.color.rgb = IBColors.GRAY
    p.alignment = PP_ALIGN.RIGHT

    return slide
```

## 导出与保存

```python
# 保存文件
prs.save('路演材料_公司名称_YYYYMM.pptx')
```

## 依赖

```
pip install python-pptx
```
