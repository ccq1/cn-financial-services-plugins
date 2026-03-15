# 中国企业三表格式规范

## 通用格式规则

### 数值格式
- **货币单位**：人民币元（万元 / 百万元 / 亿元），根据公司规模选择
- **小数位**：金额保留 2 位小数，比率保留 2 位小数（如 12.34%）
- **千分位**：使用逗号分隔（如 1,234,567.89）
- **负数**：使用括号表示，如 (1,234)，而非 -1,234
- **空值**：用 "—" 表示，非零用 "0" 表示

### 时间列排布
- **年报**：从左到右按时间正序（如 2022A → 2023A → 2024E → 2025E → 2026E）
- **A = 实际（Actual）**，**E = 预测（Estimate）**，**Q = 季度**
- **季报分析**：Q1、H1（半年报）、Q1-Q3（前三季度）、FY（全年）
- 注意中国特色的报告期：一季报(4月)、半年报(8月)、三季报(10月)、年报(次年4月)

### 表头与标签
- 使用中文科目名称（利润表、资产负债表、现金流量表）
- 科目名称后可附英文缩写：如 营业收入 (Revenue)
- 年份标注：2023A / 2024E / 2025E

### 颜色规范（Excel/PPT 输出时）
- **历史数据**：黑色
- **预测数据**：蓝色
- **输入假设**：蓝色
- **公式计算**：黑色
- **链接引用**：绿色
- **合计行**：加粗 + 底部边框

## 利润表格式

```
                        2022A      2023A      2024E      2025E
营业收入                 X,XXX      X,XXX      X,XXX      X,XXX
  YoY 增速               XX.X%      XX.X%      XX.X%      XX.X%
营业成本                (X,XXX)    (X,XXX)    (X,XXX)    (X,XXX)
毛利润                   X,XXX      X,XXX      X,XXX      X,XXX
  毛利率                  XX.X%      XX.X%      XX.X%      XX.X%
─────────────────────────────────────────────────────────────────
销售费用                (X,XXX)    (X,XXX)    (X,XXX)    (X,XXX)
管理费用                (X,XXX)    (X,XXX)    (X,XXX)    (X,XXX)
研发费用                (X,XXX)    (X,XXX)    (X,XXX)    (X,XXX)
财务费用                  (XXX)      (XXX)      (XXX)      (XXX)
─────────────────────────────────────────────────────────────────
营业利润                 X,XXX      X,XXX      X,XXX      X,XXX
  营业利润率              XX.X%      XX.X%      XX.X%      XX.X%
加：营业外收入              XXX        XXX        XXX        XXX
减：营业外支出              (XX)       (XX)       (XX)       (XX)
─────────────────────────────────────────────────────────────────
利润总额                 X,XXX      X,XXX      X,XXX      X,XXX
减：所得税费用            (XXX)      (XXX)      (XXX)      (XXX)
  有效税率                XX.X%      XX.X%      XX.X%      XX.X%
净利润                   X,XXX      X,XXX      X,XXX      X,XXX
  归母净利润              X,XXX      X,XXX      X,XXX      X,XXX
  少数股东损益              XXX        XXX        XXX        XXX
═════════════════════════════════════════════════════════════════
EPS (元)                  X.XX       X.XX       X.XX       X.XX
```

## 资产负债表格式

```
                        2022A      2023A      2024E      2025E
流动资产
  货币资金               X,XXX      X,XXX      X,XXX      X,XXX
  交易性金融资产           XXX        XXX        XXX        XXX
  应收票据及应收账款      X,XXX      X,XXX      X,XXX      X,XXX
  预付款项                 XXX        XXX        XXX        XXX
  存货                   X,XXX      X,XXX      X,XXX      X,XXX
  其他流动资产             XXX        XXX        XXX        XXX
流动资产合计             X,XXX      X,XXX      X,XXX      X,XXX
─────────────────────────────────────────────────────────────────
非流动资产
  长期股权投资             XXX        XXX        XXX        XXX
  固定资产               X,XXX      X,XXX      X,XXX      X,XXX
  在建工程                 XXX        XXX        XXX        XXX
  无形资产                 XXX        XXX        XXX        XXX
  商誉                     XXX        XXX        XXX        XXX
  使用权资产               XXX        XXX        XXX        XXX
  其他非流动资产           XXX        XXX        XXX        XXX
非流动资产合计           X,XXX      X,XXX      X,XXX      X,XXX
═════════════════════════════════════════════════════════════════
资产总计                XX,XXX     XX,XXX     XX,XXX     XX,XXX
```

## 现金流量表格式

```
                        2022A      2023A      2024E      2025E
一、经营活动现金流量
  销售商品收到的现金      X,XXX      X,XXX      X,XXX      X,XXX
  购买商品支付的现金     (X,XXX)    (X,XXX)    (X,XXX)    (X,XXX)
  支付给职工的现金        (XXX)      (XXX)      (XXX)      (XXX)
  支付的各项税费          (XXX)      (XXX)      (XXX)      (XXX)
  其他                     XXX        XXX        XXX        XXX
经营活动现金流量净额      X,XXX      X,XXX      X,XXX      X,XXX
─────────────────────────────────────────────────────────────────
二、投资活动现金流量
  购建固定资产等         (X,XXX)    (X,XXX)    (X,XXX)    (X,XXX)
  投资支付的现金          (XXX)      (XXX)      (XXX)      (XXX)
  其他                     XXX        XXX        XXX        XXX
投资活动现金流量净额     (X,XXX)    (X,XXX)    (X,XXX)    (X,XXX)
─────────────────────────────────────────────────────────────────
三、筹资活动现金流量
  取得借款收到的现金      X,XXX      X,XXX      X,XXX      X,XXX
  偿还债务支付的现金     (X,XXX)    (X,XXX)    (X,XXX)    (X,XXX)
  分配股利支付的现金      (XXX)      (XXX)      (XXX)      (XXX)
  其他                    (XXX)      (XXX)      (XXX)      (XXX)
筹资活动现金流量净额       XXX        XXX        XXX        XXX
═════════════════════════════════════════════════════════════════
现金及等价物净增加额       XXX        XXX        XXX        XXX
期初现金及等价物余额     X,XXX      X,XXX      X,XXX      X,XXX
期末现金及等价物余额     X,XXX      X,XXX      X,XXX      X,XXX
```
