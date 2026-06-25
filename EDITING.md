# Editing the Diligent Services website

This site is a small [Quarto](https://quarto.org) site. Every page is a plain text
file you can edit by hand. You do **not** need to be a programmer to update the
words, the contact details, or the colors. This guide walks through the common
changes step by step.

> **Golden rule:** edit the text, preview it, then publish. Nothing you type goes
> live until you run the publish step at the bottom.

---

## 1. Which file is which page?

| To change this page... | Edit this file |
|---|---|
| Home | `index.qmd` |
| Services | `services.qmd` |
| About Us | `about.qmd` |
| Contact | `contact.qmd` |
| Support | `support/index.qmd` |
| Blog (the list) | `blog/index.qmd` |
| A blog post | the matching file in `blog/` |
| The menu, footer, contact email/phone | `_quarto.yml` |
| Colors and fonts | `styles/custom.scss` |
| The "made with AI" note (G611) | `_g611.qmd` |

Each `.qmd` file starts with a small block between `---` lines (the "front
matter", which sets the title) followed by the page text written in **Markdown**.

---

## 2. Change the words on a page

1. Open the file from the table above in any text editor.
2. Below the `---` block, edit the text. Markdown basics:
   - `## A Heading` makes a section heading.
   - `- item` makes a bullet. `**bold**` makes bold text.
   - `[link text](contact.qmd)` makes a link to another page.
3. Save the file, then **preview** (section 5) and **publish** (section 6).

Keep these lines exactly as they are wherever they appear, they are required:

- `Diligent Services is a DBA of Carmelita Enterprises Inc.`
- the CSLB license number `1132892`

---

## 3. Change the menu, footer, email, or phone

Open `_quarto.yml`.

- **Menu items** live under `navbar:` `left:`. Each item has a `text:` (what shows)
  and an `href:` (which file it opens).
- **Footer** lives under `page-footer:`. The `center:` line is the required legal
  line, leave it as is.
- **Email / phone** show on the Contact and Support pages, edit those files
  (`contact.qmd`, `support/index.qmd`). The little email icon in the top-right menu
  is the `mailto:` line near the bottom of `_quarto.yml`.

---

## 4. Change the colors or fonts

Open `styles/custom.scss`. The top section has a short list of named colors with
comments, for example:

```scss
$ds-cream:  #FBF9F4;  // page background (warm off-white)
$ds-brass:  #9A6B1E;  // the one warm accent (buttons, active nav, rules)
```

Change a `#` hex value to recolor the site, then preview. To change a font, update
the two `font-family` lines here **and** the Google Fonts `<link>` near the bottom
of `_quarto.yml` so the new font actually loads.

---

## 5. Add a blog post

1. Copy an existing post in `blog/` to a new file, e.g. `blog/my-new-post.qmd`.
2. Edit the front matter at the top: `title`, `date`, `description`, and the
   `categories`.
3. Write the post in Markdown below the front matter.
4. Preview, then publish. The post appears on the Blog page automatically.

(There is a longer how-to post already in the blog:
"How to Create and Publish a Quarto Blog Post".)

---

## 6. Preview your changes locally

From a terminal, in the project folder:

```bash
quarto preview
```

This opens the site in your browser and refreshes as you save. Press `Ctrl+C` to
stop. Use this to check your edits before publishing.

---

## 7. Publish to the live site

The live site does **not** update automatically when you save or push, you have to
publish it. The site runs on the company's web server (Hetzner). The steps:

1. Commit and push your changes to GitHub
   (`git add <files you changed>`, `git commit -m "update copy"`, `git push`).
2. Connect to the server over SSH (the login key is stored in the company
   1Password under "Hetzner | root | diligentservices.io").
3. On the server:
   ```bash
   cd /var/www/diligentservices/diligentservices-quarto
   git pull
   source .venv/bin/activate   # required, or the blog posts fail to build
   quarto render
   ```
   The web server serves the freshly rendered `_site/` folder. No restart needed.

> **Review before publish.** Public, client-facing copy should be read over (and,
> for blog posts, approved by Sam) before this publish step. When in doubt, preview
> and ask first.

---

## 8. House rules

- **No client names or project specifics** on the public site unless you have
  written permission. Keep capability copy generic.
- Keep the **DBA legal line** and the **CSLB 1132892** number wherever they appear.
- Keep the **`/support`** page live with a working email link, an app store requires it.
- The AI-authorship note (`_g611.qmd`, shown on Support) stays for any page that is
  largely written with AI help.
