# Custom setup

Presets are optional. If the user describes their voice or audience directly, use that context without requesting a filled questionnaire. The offline helper accepts `--config setup.json`. Every selection can be a preset ID or a custom object; `none` clears optional creator/reader/prompt/tool selections. Angle and style are required, with `rewrite` and `plain` defaults.

## Object shape

```json
{
  "angle": {"name": "Client follow-up", "instructions": "Summarize the agreed scope and supported next step. Do not invent urgency."},
  "creator": {"name": "My voice", "details": {"tone": "Direct and respectful.", "boundaries": "No invented experience."}},
  "reader": {"name": "My reader", "details": {"description": "A hypothetical evaluator.", "goals": "Understand the implementation limits."}},
  "style": "concise",
  "prompt": "claim-aware",
  "tool": null,
  "requirements": "Use two short paragraphs."
}
```

- `angle`, `style`, `prompt`, `tool`: custom `name` plus `instructions`.
- `creator`: custom `name` plus `details` using `positioning`, `expertise`, `tone`, `style`, `boundaries`, `samples`.
- `reader`: custom `name` plus `details` using `description`, `painPoints`, `goals`, `contentPreferences`.
- `requirements`: optional explicit format/length or other editorial guidance.

Unknown fields, duplicate JSON keys, non-finite values, empty profiles and invalid preset IDs are rejected. Partial profiles are welcome; provide at least one meaningful field. Names have a 100-character limit; instruction fields 4,000; profile fields 1,000 (samples 3,000); requirements 2,000; source text 20,000. The helper does not fetch a URL supplied instead of source text.

CLI flags override only their matching config fields. A refinement tool takes precedence over the angle's output format. Explicit length/format requests take precedence over suggested preset lengths, while factual fidelity and profile boundaries remain required.

## Extend the shared catalog

Add original entries to `references/catalog.json`, with a unique lowercase kebab-case ID in their collection. Preserve the default `rewrite` and `plain` IDs. Creator and reader entries use the same `details` fields as custom profiles. Other entries need `instructions`; include a useful name/summary, source references and accurate provenance where applicable.

Run `python3 scripts/validate.py` and the tests. Counts and combination discovery follow the lists; there is no per-user slot limit. Keep the README and selection guide in step with catalog additions. Do not add private user profiles, copied commercial presets or scraped datasets to the public catalog.
