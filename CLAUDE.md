# victoriasickness-admin (PUBLIC)

Admin for victoriasickness-web (La Senyal model). No private data here.
- `web/config.yml` is generated: edit `scripts/make_config.py`, then `python3 scripts/make_config.py ../victoriasickness-web web/config.yml`. Regenerate whenever text keys or a content file's shape change in victoriasickness-web (keys missing from a form may be dropped on save).
- Validate against Sveltia's schema (`npm pack @sveltia/cms` → `package/schema/sveltia-cms.json`). Keep: `slugify_filename: false`, `dropdown_threshold: 12` on selects, `output.json.indent_size: 1`. Admin folder is `web/` (Sveltia can't write into a folder with the same path as its page).
- Test without a token: Sveltia `backend: {name: test-repo}` in a local copy, seed the OPFS folder `sveltia-cms-test` with the content files (Playwright), Save, diff.
- No Google, no Amazon: fonts in `fonts/`; Sveltia loads from unpkg.
- Commit author `Cia. Victoria Sickness <victoriasickness@gmail.com>`.
