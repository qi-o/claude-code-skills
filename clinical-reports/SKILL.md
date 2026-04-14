---
name: clinical-reports
description: |
  Write comprehensive clinical reports including case reports (CARE guidelines), diagnostic reports (radiology/pathology/lab), clinical trial reports (ICH-E3, SAE, CSR), and patient documentation (SOAP, H&P, discharge summaries). Full support with templates, regulatory compliance (HIPAA, FDA, ICH-GCP), and validation tools.
  触发场景：
  (1) 用户需要撰写病例报告、临床报告、诊断报告、出院小结、SOAP记录
  (2) 用户说"病例报告"、"临床报告"、"诊断报告"、"出院小结"、"SOAP记录"、"case report"、"clinical report"、"discharge summary"、"SOAP note"、"H&P"、"SAE report"
  Do NOT use for treatment planning (use treatment-plans instead) or medical imaging processing (use pydicom instead).
allowed-tools: [Read, Write, Edit, Bash]
license: MIT License
metadata:
    skill-author: K-Dense Inc.
---

# Clinical Report Writing

## Overview

Clinical report writing is the process of documenting medical information with precision, accuracy, and compliance with regulatory standards. This skill covers four major categories: case reports for journal publication, diagnostic reports for clinical practice, clinical trial reports for regulatory submission, and patient documentation for medical records.

**Critical Principle**: Clinical reports must be accurate, complete, objective, and compliant with applicable regulations (HIPAA, FDA, ICH-GCP). Patient privacy and data integrity are paramount.

## When to Use This Skill

- Writing clinical case reports for journal submission (CARE guidelines)
- Creating diagnostic reports (radiology, pathology, laboratory)
- Documenting clinical trial data and adverse events
- Preparing clinical study reports (CSR) for regulatory submission
- Writing patient progress notes, SOAP notes, and clinical summaries
- Drafting discharge summaries, H&P documents, or consultation notes
- Ensuring HIPAA compliance and proper de-identification
- Preparing serious adverse event (SAE) reports

> **前置检查（HARD 门控）**
>
> 起草临床报告前必须满足以下条件，否则拒绝执行：
>
> | 检查项 | 通过条件 | 不通过时 |
> |--------|---------|---------|
> | 临床数据已提供 | 患者基本信息、诊断/治疗数据可用 | 要求用户提供数据 |
> | 数据已脱敏 | 无患者姓名、身份证号、联系电话等 PHI | 使用 HIPAA 安全港标准脱敏后重试 |
>
> 如果用户坚持跳过脱敏，拒绝执行：「临床报告必须先完成 PHI 脱敏，这是法规要求，不可跳过。」

## Visual Enhancement with Scientific Schematics

**MANDATORY: Every clinical report MUST include at least 1 AI-generated figure using the scientific-schematics skill.**

Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (patient timeline, diagnostic algorithm, treatment workflow)
2. For case reports: include clinical progression timeline
3. For trial reports: include CONSORT flow diagram

```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

---

## Core Capabilities

### 1. Clinical Case Reports

Case reports describe unusual clinical presentations, novel diagnoses, or rare complications for peer-reviewed journal publication.

**Key requirements**: CARE guidelines compliance, patient de-identification (18 HIPAA identifiers), informed consent for publication.

**CARE sections**: Title → Keywords → Abstract → Introduction → Patient Information → Clinical Findings → Timeline → Diagnostic Assessment → Therapeutic Interventions → Follow-up and Outcomes → Discussion → Patient Perspective → Informed Consent.

For full CARE checklist, de-identification guide, and journal requirements, see [`references/report_details.md#1-case-report-components`](references/report_details.md).

### 2. Clinical Diagnostic Reports

Diagnostic reports communicate findings from imaging, pathology, and laboratory tests.

| Report Type | Key Sections | Standards |
|-------------|-------------|-----------|
| Radiology | Demographics, Indication, Technique, Comparison, Findings, Impression | ACR lexicon, RadLex; Lung-RADS, BI-RADS, LI-RADS, PI-RADS |
| Pathology | Patient Info, Specimen, Clinical History, Gross, Microscopic, Diagnosis, Comment | CAP synoptic reporting, TNM staging |
| Laboratory | Patient/Specimen Info, Test/Method, Results, Interpretation, QC | Critical value notification required |

For full structure details and examples, see [`references/report_details.md#2-diagnostic-reports`](references/report_details.md).

### 3. Clinical Trial Reports

**Serious Adverse Event (SAE) Reports**: Document unexpected serious adverse reactions. Regulatory timelines: fatal/life-threatening SAEs → 7-day preliminary + 15-day complete report; other serious unexpected events → 15 days.

**Clinical Study Reports (CSR)**: ICH-E3 structure, 15 main sections from Title Page through Appendices. Submitted to regulatory agencies for drug approval.

**Protocol Deviations**: Minor, Major, or Violation categories; require CAPA documentation.

For full SAE components, ICH-E3 structure, and regulatory timelines, see [`references/report_details.md#3-clinical-trial-reports`](references/report_details.md).

### 4. Patient Clinical Documentation

| Document | Format | Key Elements |
|----------|--------|-------------|
| SOAP Note | Subjective / Objective / Assessment / Plan | Most common progress note format |
| H&P | 10-section comprehensive assessment | CC, HPI (OPQRST), PMH, Meds, Allergies, FH, SH, ROS, PE, A&P |
| Discharge Summary | 10 required elements | Hospital course, discharge meds, follow-up plans, patient instructions |

For full structure, examples, and documentation tips, see [`references/report_details.md#4-patient-clinical-documentation`](references/report_details.md).

---

## Regulatory Compliance

- **HIPAA**: Safe Harbor (remove 18 identifiers) or Expert Determination method; Business Associate Agreements required for PHI sharing
- **FDA**: 21 CFR Parts 11, 50, 56, 312
- **ICH-GCP**: Protocol adherence, informed consent, source documents, audit trails

For detailed compliance requirements, see [`references/report_details.md#5-regulatory-compliance`](references/report_details.md).

---

## Workflows

### Case Report: 6 phases over ~5 weeks
1. Case identification and consent
2. Literature review
3. Drafting (CARE structure)
4. Internal review
5. Journal selection and submission
6. Revision and resubmission

### Diagnostic Report: Real-time
Review indication → interpret findings → dictate/type → peer review (complex) → sign-out → critical value notification.

### SAE Report: 24 hours to 15 days
Event identified → assessment → causality/expectedness → completion/review → submission → follow-up.

### CSR: 6-12 months post-study
Database lock → statistical analysis → drafting → review → QC → regulatory submission.

---

## Resources

### Reference Files
- [`references/report_details.md`](references/report_details.md) — Full details: CARE checklist, diagnostic report structures, SAE/CSR components, SOAP/H&P/discharge formats, HIPAA, terminology, QA, data presentation, workflows, pitfalls

### Template Assets
- `assets/case_report_template.md` — CARE guidelines case report
- `assets/radiology_report_template.md` — Standard radiology format
- `assets/pathology_report_template.md` — Surgical pathology with synoptic elements
- `assets/lab_report_template.md` — Clinical laboratory format
- `assets/clinical_trial_sae_template.md` — SAE report form
- `assets/clinical_trial_csr_template.md` — CSR outline per ICH-E3
- `assets/soap_note_template.md` — SOAP progress note
- `assets/history_physical_template.md` — Comprehensive H&P
- `assets/discharge_summary_template.md` — Hospital discharge summary
- `assets/consult_note_template.md` — Consultation note
- `assets/quality_checklist.md` — QA checklist for all report types
- `assets/hipaa_compliance_checklist.md` — Privacy and de-identification checklist

### Automation Scripts
- `scripts/validate_case_report.py` — CARE guideline compliance check
- `scripts/validate_trial_report.py` — ICH-E3 structure verification
- `scripts/check_deidentification.py` — Scan for 18 HIPAA identifiers
- `scripts/format_adverse_events.py` — Generate AE summary tables
- `scripts/generate_report_template.py` — Interactive template selection
- `scripts/compliance_checker.py` — Regulatory compliance verification
- `scripts/terminology_validator.py` — Medical terminology and coding validation

---

## Final Checklist

Before finalizing any clinical report:

- [ ] All required sections complete
- [ ] Patient privacy protected (HIPAA compliance)
- [ ] Informed consent obtained (if applicable)
- [ ] Accurate and verified clinical data
- [ ] Appropriate medical terminology and coding
- [ ] Clear, professional language
- [ ] Proper formatting per guidelines
- [ ] References cited appropriately
- [ ] Figures and tables labeled correctly
- [ ] Regulatory requirements met
- [ ] Signatures and dates present
- [ ] Quality assurance review completed

---

**Final Note**: Clinical report writing requires attention to detail, medical accuracy, regulatory compliance, and clear communication. Quality of clinical reports directly impacts patient safety, healthcare delivery, and medical knowledge advancement.

---

## 推荐下一步

| 触发条件 | 推荐 |
|---------|------|
| 报告完成，需要治疗方案 | 使用 `treatment-plans` — 治疗方案制定 |
| 需要输出 Word 格式 | 使用 `docx` — Word 文档生成 |
| 需要输出 PDF 格式 | 使用 `pdf` — PDF 处理 |
| 需要科研图表 | 使用 `pub-figures` — 出版级科研图表 |

---

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| PHI 脱敏验证 | 用户提供了含患者标识符的原始数据 | 确认已按 HIPAA 安全港标准完成脱敏，列出 18 项标识符的检查结果 |
| 报告类型选择 | 用户请求模糊（如"写个临床报告"） | 确认具体报告类型（Case Report / Diagnostic / SAE / SOAP / Discharge） |
| 致命不良事件上报 | SAE 报告涉及 fatal 或 life-threatening 事件 | 确认 7 天初步报告 + 15 天完整报告的时间线要求已告知用户 |

---

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| 脱敏检查未通过 | `check_deidentification.py` 检出 PHI 残留 | 拒绝生成报告，列出检出项，指导用户修正后重试 |
| 关键临床数据缺失 | 模板必填字段为空（如诊断、治疗、随访） | 暂停生成，列出缺失字段清单，等用户补充 |
| 合规验证失败 | `compliance_checker.py` 报告不符合 ICH-GCP/HIPAA | 逐条列出违规项，修正后重新验证 |
| 验证脚本执行失败 | Python 脚本报错或依赖缺失 | 检查依赖安装（`pip install`），降级为人工逐项检查清单 |
