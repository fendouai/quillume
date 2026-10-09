# Quillume — by WarmQuant

*Your ideas. Your voice. A little more light.*

Turn original notes into clear English drafts, with a writing angle, an author voice, a reader profile and an editable style.

This is a standalone [Agent Skill](https://agentskills.io/specification). It uses the language model in your existing agent host. The optional Python helper lists presets and constructs prompts offline; it does not generate text or contact a service. No separate WarmQuant account or API key is required. Your host's model limits and data policies still apply.

## Included

| Collection | Presets |
| --- | ---: |
| Writing angles | 10 |
| Creator voices | 10 |
| Reader profiles | 10 |
| Voice and style | 10 |
| Editing methods | 12 |
| Refinement tools | 7 |

Choose any angle, creator and reader: 1,000 core combinations are available from one shared catalog. Styles can accompany any combination. Every collection supports custom instructions or profiles. Profiles are editable hypothetical templates, not claims about you or researched customers.

## Install

Download or clone this repository into a folder named `quillume`. Copy the whole folder to the skill-discovery directory supported by your agent host. Keep `SKILL.md`, `scripts/`, `references/`, and `agents/` together. There is no install script that changes your environment.

For Codex, a user-level installation can be made by copying the folder into `~/.codex/skills/quillume`. Restart or reload your host's skill catalog if needed. Other hosts should use their own documented skill location; folder discovery and invocation syntax vary. `agents/openai.yaml` is optional Codex UI metadata, while `SKILL.md` is the portable entrypoint.

## Use with an agent

In Codex:

```text
Use $quillume to expand these notes for busy founders.
Use a candid founder voice and the Professional style.

Source: We reduced the internal weekly reporting workflow from five steps to three.
We checked one workflow. Customer time savings have not been measured.
```

Or ask for a concise rewrite without choosing profiles. The skill defaults to plain language and does not invent an author identity or audience. Drafts are English. It retains source qualifications and reviews unsupported claims before delivery.

The source above is a fictional example, not a WarmQuant result or customer testimonial.

## Optional offline helper

Python 3.10+ is sufficient; there are no pip packages to install. Run these from the repository root:

```sh
python3 scripts/quillume.py list --kind style
python3 scripts/quillume.py show creator indie-founder
python3 scripts/quillume.py compose --source examples/notes.txt \
  --angle expand --creator indie-founder --reader busy-founder \
  --style professional --prompt claim-aware
python3 scripts/quillume.py compose --source examples/notes.txt \
  --config examples/custom-setup.json
python3 scripts/quillume.py compose --source examples/notes.txt --tool check
```

`compose` prints a provider-neutral JSON message bundle to stdout. Ask your current agent to execute the writing task, or pass the bundle to a model through your own integration. Source text can also be piped to stdin. The helper never reads environment credentials, fetches links, executes preset text or saves a draft. Its output contains your supplied source and configuration, so handle it as carefully as those inputs.

CLI options override matching fields in a custom setup. Defaults are `rewrite` and `plain`; creator, reader, editing method and refinement tool are optional. Use `none` to clear an optional selection. When a refinement tool is chosen, it performs that operation on the source rather than also generating the angle's format.

## Customize and extend

[Customization](references/customization.md) explains preset IDs, custom objects and supported fields. Add original entries to [the catalog](references/catalog.json) to expand the library; there is no hard-coded cap on collection size. Keep `rewrite` and `plain` as default IDs, or update the defaults and their documentation together. The helper picks up new entries without route generation or a build step.

Examples and case-review guidance are in [references/examples.md](references/examples.md); [a complete fictional draft](examples/draft.md) demonstrates the source in `examples/notes.txt`. Only supplied text is used as factual evidence. Voice samples guide expression, not factual claims. The skill does not claim to bypass AI detectors, determine authorship, research an audience automatically or publish on your behalf.

## Validate

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The validator checks skill structure, links, catalog consistency and accidental inclusion of credential patterns or private deployment artifacts. Tests cover prompt composition, custom fields, CLI behavior, all preset combinations and extension behavior. They do not prove that every model will preserve facts or follow safety instructions; review generated drafts in your host.

Local verification on 2026-10-09: the Skill Creator format check, publication hygiene validation and 16 unit/CLI checks passed. The checks exercise all 1,000 core combinations and an added creator preset. Python 3.10 syntax compatibility was checked; a multi-host model benchmark was not performed.

GitHub Actions is configured to run validation and tests with Python 3.10 and 3.13 after you publish the repository; that remote workflow has not run yet.

## Repository layout

```text
SKILL.md                  Portable agent instructions
agents/openai.yaml        Optional Codex presentation metadata
references/catalog.json   Maintained public presets
references/*.md           On-demand selection, customization and sources
scripts/quillume.py      Offline discovery and prompt composition
scripts/validate.py       Structure and publication hygiene checks
tests/                    Dependency-free behavioral tests
examples/                 Fictional notes and custom setup
LICENSE                   MIT
```

## License and sources

The code and original editorial templates in this repository are available under the [MIT License](LICENSE). External framework references are listed in [references/sources.md](references/sources.md); linked publications are not included or relicensed. Reference links do not imply endorsement. This repository has no SaaS billing, authentication, deployment configuration, user database, analytics or referral-signature logic.
