# Writing Quality Rules

## Mandatory Checks Before Delivery

STOP. Do NOT deliver any serious writing output until all items below are verified.

- [ ] All factual claims have a cited source (PubMed ID, DOI, or named database)
- [ ] All statistics and numerical data match the cited source exactly
- [ ] No hyperlinks or DOIs are fabricated — each one resolves to the claimed content
- [ ] Internal logic is consistent (no contradictory statements across sections)
- [ ] Conclusions are supported by the evidence presented, not extrapolated beyond it
- [ ] Terminology is used consistently throughout (no silent synonym swaps)
- [ ] All figures/tables referenced in text actually exist in the document
- [ ] No claims of "recent studies show..." without a specific citation

## What Counts as Serious Writing Output

Any of the following triggers mandatory independent Agent review:

- Academic manuscript sections (Introduction, Methods, Results, Discussion)
- Literature review or systematic review summaries
- Grant proposal text
- Clinical or translational interpretation of data
- Any output produced by `academic-writing-suite` or `deep-research` skills

## Independent Agent Review Protocol

❌ Wrong — deliver immediately after writing:
[academic-writing-suite produces draft] -> send to user

✅ Correct — always gate delivery through independent review:
[academic-writing-suite produces draft] -> quality-reviewer + verifier -> deliver

### Trigger Rule

After any serious writing task completes, the producing agent MUST NOT self-review.
A separate `quality-reviewer` (sonnet) agent reviews for logic, consistency, and factual coherence.
A separate `verifier` (sonnet) agent confirms all mandatory checks above are satisfied.
Only after both agents return clean results may the output be delivered.

## Integration with Existing Skills

| Skill | Review Required | Agents to Invoke |
|-------|----------------|-----------------|
| `academic-writing-suite` | Always | `quality-reviewer` + `verifier` |
| `deep-research` | Always | `quality-reviewer` + `verifier` |
| `ai-check-humanizer` | After humanization | `verifier` only |
| `paper-search` | No (search results, not prose) | — |

## Escalation

If `quality-reviewer` or `verifier` flags issues:
1. STOP — do not deliver the draft
2. Return flagged issues to the writing agent for revision
3. Re-run review after revision
4. Maximum 2 revision cycles; if unresolved after 2 cycles, surface issues to user explicitly
