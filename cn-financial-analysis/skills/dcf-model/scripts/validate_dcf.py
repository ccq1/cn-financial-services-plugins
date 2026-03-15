#!/usr/bin/env python3
"""
A股 DCF 模型验证脚本

验证 DCF 模型的关键参数和逻辑一致性。
用于在生成 DCF 分析后进行快速质量检查。

用法:
    python validate_dcf.py <dcf_yaml_file>

示例:
    python validate_dcf.py kweichow_moutai_dcf.yaml
"""

import sys
import yaml
from pathlib import Path


def validate_wacc(params: dict) -> list:
    """验证 WACC 参数合理性"""
    errors = []
    warnings = []

    rf = params.get("risk_free_rate", 0)
    erp = params.get("equity_risk_premium", 0)
    beta = params.get("beta", 0)
    kd = params.get("cost_of_debt", 0)
    tax_rate = params.get("tax_rate", 0)
    debt_ratio = params.get("debt_to_total_capital", 0)
    wacc = params.get("wacc", 0)

    # 无风险利率检查
    if rf < 0.01 or rf > 0.05:
        warnings.append(
            f"⚠️ 无风险利率 {rf:.2%} 超出典型范围 (1.0%-5.0%)，"
            "请确认是否使用10年期国债收益率"
        )

    # ERP 检查
    if erp < 0.04 or erp > 0.10:
        warnings.append(
            f"⚠️ 股权风险溢价 {erp:.2%} 超出A股典型范围 (4.0%-10.0%)"
        )

    # Beta 检查
    if beta < 0.3 or beta > 2.0:
        warnings.append(f"⚠️ Beta {beta:.2f} 超出典型范围 (0.3-2.0)")

    # 税率检查
    if tax_rate not in [0.15, 0.25]:
        warnings.append(
            f"⚠️ 税率 {tax_rate:.0%}，A股企业通常为 25%（一般）或 15%（高新技术）"
        )

    # WACC 合理性
    ke = rf + beta * erp
    expected_wacc = ke * (1 - debt_ratio) + kd * (1 - tax_rate) * debt_ratio

    if wacc > 0 and abs(wacc - expected_wacc) > 0.005:
        errors.append(
            f"❌ WACC 不一致: 声明值 {wacc:.2%}, 计算值 {expected_wacc:.2%}, "
            f"差异 {abs(wacc - expected_wacc):.2%}"
        )

    if wacc < 0.05 or wacc > 0.15:
        warnings.append(f"⚠️ WACC {wacc:.2%} 超出典型范围 (5.0%-15.0%)")

    return errors, warnings


def validate_terminal_value(params: dict, wacc: float) -> list:
    """验证终值参数"""
    errors = []
    warnings = []

    method = params.get("method", "perpetuity_growth")
    g = params.get("perpetuity_growth_rate", 0)
    tv_pct = params.get("tv_as_pct_of_ev", 0)
    exit_multiple = params.get("exit_multiple", 0)

    if method == "perpetuity_growth" or g > 0:
        # 永续增长率 < WACC
        if g >= wacc:
            errors.append(
                f"❌ 永续增长率 ({g:.2%}) ≥ WACC ({wacc:.2%})，"
                "模型无效"
            )
        # 永续增长率不应超过GDP长期增速
        if g > 0.04:
            warnings.append(
                f"⚠️ 永续增长率 {g:.2%} 偏高，不应超过中国GDP长期增速预期 (3-4%)"
            )
        if g < 0:
            warnings.append(f"⚠️ 永续增长率为负 ({g:.2%})，请确认合理性")

    if method == "exit_multiple" or exit_multiple > 0:
        if exit_multiple > 25:
            warnings.append(
                f"⚠️ 退出倍数 {exit_multiple:.1f}x 偏高，请确认行业可比水平"
            )

    # 终值占比
    if tv_pct > 0.80:
        warnings.append(
            f"⚠️ 终值占企业价值比例 {tv_pct:.0%} > 80%，"
            "近期预测可能过于保守或终值假设过于激进"
        )

    return errors, warnings


def validate_projections(projections: list) -> list:
    """验证预测数据一致性"""
    errors = []
    warnings = []

    if not projections:
        errors.append("❌ 未找到预测数据")
        return errors, warnings

    for i, year_data in enumerate(projections):
        year = year_data.get("year", f"第{i+1}年")
        revenue = year_data.get("revenue", 0)
        ebit = year_data.get("ebit", 0)
        fcff = year_data.get("fcff", 0)
        capex = year_data.get("capex", 0)
        da = year_data.get("depreciation_amortization", 0)

        # 基本合理性
        if revenue <= 0:
            errors.append(f"❌ {year}: 营收 ≤ 0")

        if ebit != 0 and revenue != 0:
            ebit_margin = ebit / revenue
            if ebit_margin > 0.60:
                warnings.append(
                    f"⚠️ {year}: EBIT 利润率 {ebit_margin:.0%} 异常高"
                )

        # CAPEX 应为负数或其绝对值 < 营收
        if abs(capex) > revenue and revenue > 0:
            warnings.append(
                f"⚠️ {year}: CAPEX ({capex:,.0f}) > 营收 ({revenue:,.0f})，请确认"
            )

    # 检查最后一年增速是否趋于稳态
    if len(projections) >= 2:
        last_rev = projections[-1].get("revenue", 0)
        prev_rev = projections[-2].get("revenue", 0)
        if prev_rev > 0:
            last_growth = (last_rev - prev_rev) / prev_rev
            if last_growth > 0.20:
                warnings.append(
                    f"⚠️ 预测末年营收增速仍为 {last_growth:.0%}，"
                    "尚未趋于稳态，可能需要延长预测期"
                )

    return errors, warnings


def validate_balance_sheet_check(bs: dict) -> list:
    """验证三表勾稽"""
    errors = []

    total_assets = bs.get("total_assets", 0)
    total_liabilities = bs.get("total_liabilities", 0)
    total_equity = bs.get("total_equity", 0)

    if total_assets > 0:
        diff = abs(total_assets - total_liabilities - total_equity)
        if diff > 1:  # 允许1元四舍五入误差
            errors.append(
                f"❌ 资产负债表不平: 资产 {total_assets:,.0f} ≠ "
                f"负债 {total_liabilities:,.0f} + 权益 {total_equity:,.0f}，"
                f"差异 {diff:,.0f}"
            )

    return errors


def validate_dcf(file_path: str) -> bool:
    """主验证函数"""
    path = Path(file_path)

    if not path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"❌ YAML 解析错误: {e}")
        return False

    if not data:
        print("❌ 文件为空")
        return False

    all_errors = []
    all_warnings = []

    company = data.get("company", "未知公司")
    print(f"\n📊 验证 DCF 模型: {company}")
    print("=" * 60)

    # 1. WACC 验证
    wacc_params = data.get("wacc_parameters", {})
    if wacc_params:
        errors, warnings = validate_wacc(wacc_params)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
    else:
        all_errors.append("❌ 未找到 WACC 参数")

    # 2. 终值验证
    tv_params = data.get("terminal_value", {})
    wacc = wacc_params.get("wacc", 0.10)
    if tv_params:
        errors, warnings = validate_terminal_value(tv_params, wacc)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    # 3. 预测数据验证
    projections = data.get("projections", [])
    errors, warnings = validate_projections(projections)
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    # 4. 资产负债表勾稽
    bs = data.get("balance_sheet_check", {})
    if bs:
        errors = validate_balance_sheet_check(bs)
        all_errors.extend(errors)

    # 输出结果
    if all_warnings:
        print("\n⚠️  警告:")
        for w in all_warnings:
            print(f"  {w}")

    if all_errors:
        print("\n❌ 错误:")
        for e in all_errors:
            print(f"  {e}")
        print(f"\n结果: 发现 {len(all_errors)} 个错误, {len(all_warnings)} 个警告")
        return False
    else:
        print(f"\n✅ 验证通过! ({len(all_warnings)} 个警告)")
        return True


def main():
    if len(sys.argv) != 2:
        print("用法: python validate_dcf.py <dcf_yaml_file>")
        print("\nYAML 文件格式示例:")
        print("""
company: "贵州茅台"
wacc_parameters:
  risk_free_rate: 0.028
  equity_risk_premium: 0.065
  beta: 0.75
  cost_of_debt: 0.035
  tax_rate: 0.15
  debt_to_total_capital: 0.05
  wacc: 0.095
terminal_value:
  method: perpetuity_growth
  perpetuity_growth_rate: 0.03
  tv_as_pct_of_ev: 0.65
projections:
  - year: 2025E
    revenue: 170000
    ebit: 85000
    fcff: 72000
    capex: -8000
    depreciation_amortization: 5000
  - year: 2026E
    revenue: 190000
    ebit: 96000
    fcff: 82000
    capex: -9000
    depreciation_amortization: 5500
""")
        sys.exit(1)

    file_path = sys.argv[1]
    success = validate_dcf(file_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
