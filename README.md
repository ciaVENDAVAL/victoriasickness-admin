# victoriasickness-admin

Edit the website of **Cia. Victoria Sickness** from the phone, without code: https://ciavendaval.github.io/victoriasickness-admin/

- **Formularios** (`web/`, [Sveltia CMS](https://sveltiacms.app)): texts in 8 languages side by side, shows (title, video, credits, supporters, gallery), "about" photos, photo credits, PDFs per language, colours and font.
- **Editar en la página:** any page of the site + `#edit` (the editor lives in victoriasickness-web `src/edit.js`).
- Every Save / Publish is one commit in `ciaVENDAVAL/victoriasickness-web`; its workflow translates (Softcatalà) and rebuilds the site in 3–5 minutes. History = undo.
- Sign-in: a GitHub fine-grained token (owner ciaVENDAVAL, only victoriasickness-web, Contents: read and write). Steps on the start page.

Model: La Senyal (`ciaVENDAVAL/lasenyal-admin`). GitHub Pages: branch main, folder / (root).

```
index.html            start page (Spanish), fonts/ (OFL), favicon.svg
web/index.html        loads Sveltia CMS
web/config.yml        GENERATED — python3 scripts/make_config.py ../victoriasickness-web web/config.yml
scripts/make_config.py  field lists; the Texts form is generated from victoriasickness-web/content/i18n/es.json
```
