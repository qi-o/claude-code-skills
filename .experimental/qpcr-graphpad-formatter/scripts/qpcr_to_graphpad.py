#!/usr/bin/env python3
"""
QPCR Data Formatter for GraphPad Prism
Converts qPCR CSV data to LC/KO two-column format.

Usage:
    python qpcr_to_graphpad.py <csv_file> [--control GROUP] [--ref GENES] [--targets GENES]

Example:
    python qpcr_to_graphpad.py data.csv --control siNC --ref RPLP0,HPRT1 --targets NCOA4,SLC7A11
"""

import pandas as pd
import numpy as np
import argparse
import os
import sys


def calculate_fold_change(data, control_group, target_genes, reference_genes):
    """
    计算相对表达量 (2^-ΔΔCt方法)

    Args:
        data: DataFrame with Sample, Group, Gene, TechRep, Ct columns
        control_group: Name of control group
        target_genes: List of target gene names
        reference_genes: List of reference (housekeeping) gene names

    Returns:
        DataFrame with Sample, Group, Gene, FoldChange columns
    """
    # 按样本和基因分组计算平均Ct值（技术重复平均）
    avg_ct = data.groupby(['Sample', 'Group', 'Gene'])['Ct'].mean().reset_index()

    # 计算每个样本的内参基因平均Ct值
    ref_ct = avg_ct[avg_ct['Gene'].isin(reference_genes)].groupby(['Sample', 'Group'])['Ct'].mean().reset_index()
    ref_ct.columns = ['Sample', 'Group', 'RefCt']

    # 合并数据
    merged = avg_ct.merge(ref_ct, on=['Sample', 'Group'])

    # 筛选目标基因
    target_data = merged[merged['Gene'].isin(target_genes)].copy()

    # 计算ΔCt
    target_data['DeltaCt'] = target_data['Ct'] - target_data['RefCt']

    # 计算对照组的ΔCt平均值
    control_deltact = target_data[target_data['Group'] == control_group].groupby('Gene')['DeltaCt'].mean().reset_index()
    control_deltact.columns = ['Gene', 'ControlDeltaCt']

    # 合并对照组ΔCt
    target_data = target_data.merge(control_deltact, on='Gene')

    # 计算ΔΔCt和Fold Change
    target_data['DeltaDeltaCt'] = target_data['DeltaCt'] - target_data['ControlDeltaCt']
    target_data['FoldChange'] = 2 ** (-target_data['DeltaDeltaCt'])

    return target_data[['Sample', 'Group', 'Gene', 'FoldChange']]


def format_for_graphpad(result, gene, control_group='siNC'):
    """
    整理成GraphPad Prism格式

    Args:
        result: DataFrame with Sample, Group, Gene, FoldChange columns
        gene: Gene name to format
        control_group: Name of control group (will be labeled as LC)

    Returns:
        Tuple of (lc_values, ko_values) as numpy arrays
    """
    gene_data = result[result['Gene'] == gene].copy()

    # 获取对照组和处理组的数据
    lc_data = gene_data[gene_data['Group'] == control_group]['FoldChange'].values
    ko_groups = [g for g in gene_data['Group'].unique() if g != control_group]

    if ko_groups:
        ko_data = gene_data[gene_data['Group'] == ko_groups[0]]['FoldChange'].values
    else:
        ko_data = gene_data[gene_data['Group'] != control_group]['FoldChange'].values

    # 确保两组数据长度一致
    min_len = min(len(lc_data), len(ko_data))
    lc_data = lc_data[:min_len]
    ko_data = ko_data[:min_len]

    return lc_data, ko_data


def main():
    parser = argparse.ArgumentParser(
        description='Convert qPCR CSV data to GraphPad Prism format (LC/KO columns)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
    python qpcr_to_graphpad.py data.csv
    python qpcr_to_graphpad.py data.csv --control siNC --ref RPLP0,HPRT1 --targets NCOA4,SLC7A11
        """
    )

    parser.add_argument('csv_file', help='Path to qPCR data CSV file')
    parser.add_argument('--control', default='siNC',
                        help='Control group name (default: siNC)')
    parser.add_argument('--ref', default='RPLP0,HPRT1',
                        help='Reference genes comma-separated (default: RPLP0,HPRT1)')
    parser.add_argument('--targets',
                        help='Target genes comma-separated (default: auto-detect)')

    args = parser.parse_args()

    # 检查文件是否存在
    if not os.path.exists(args.csv_file):
        print(f"Error: File not found: {args.csv_file}")
        sys.exit(1)

    # 读取数据
    data = pd.read_csv(args.csv_file)

    # 验证必需列
    required_cols = ['Sample', 'Group', 'Gene', 'TechRep', 'Ct']
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        print(f"Error: Missing required columns: {missing_cols}")
        sys.exit(1)

    # 解析参数
    reference_genes = args.ref.split(',')
    control_group = args.control

    # 自动检测或使用指定的目标基因
    if args.targets:
        target_genes = args.targets.split(',')
    else:
        # 自动检测：排除参考基因的基因
        all_genes = data['Gene'].unique()
        target_genes = [g for g in all_genes if g not in reference_genes]

    if not target_genes:
        print("Error: No target genes found")
        sys.exit(1)

    # 计算Fold Change
    result = calculate_fold_change(data, control_group, target_genes, reference_genes)

    # 确定输出文件路径
    csv_dir = os.path.dirname(args.csv_file)
    output_file = os.path.join(csv_dir, "GraphPad_Prism_Data.txt") if csv_dir else "GraphPad_Prism_Data.txt"

    # 写入文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"QPCR Data for GraphPad Prism\n")
        f.write(f"Input: {os.path.basename(args.csv_file)}\n")
        f.write("=" * 60 + "\n\n")

        for gene in target_genes:
            lc, ko = format_for_graphpad(result, gene, control_group)
            f.write(f"{gene}:\n")
            f.write("LC\tKO\n")
            for i in range(len(lc)):
                f.write(f"{lc[i]:.3f}\t{ko[i]:.3f}\n")
            f.write("\n")

    # 同时打印到控制台
    print("=" * 60)
    print(f"QPCR Data for GraphPad Prism")
    print(f"Input: {args.csv_file}")
    print("=" * 60)
    print()

    for gene in target_genes:
        lc, ko = format_for_graphpad(result, gene, control_group)
        print(f"{gene}:")
        print("LC\tKO")
        for i in range(len(lc)):
            print(f"{lc[i]:.2f}\t{ko[i]:.2f}")
        print()

    print("=" * 60)
    print(f"Saved to: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
