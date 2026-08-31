# micjm

A minimal Hugo blog using the [Hugo Bear Blog](https://github.com/janraasch/hugo-bearblog) theme.

## Local development

Install Hugo on macOS if needed:

```sh
brew install hugo
```

Start the local server, including draft posts:

```sh
hugo server --buildDrafts
```

Then open <http://localhost:1313>.

## Create a post

```sh
hugo new content blog/my-post.md
```

Edit the generated Markdown file and change `draft = true` to `draft = false` when it is ready to publish.

## Production build

```sh
hugo build --cleanDestinationDir --gc --minify
```

The generated site is written to `public/`, which is intentionally excluded from Git.

## GitHub Pages

1. Push this repository to GitHub with `main` as the default branch.
2. In the repository, open **Settings → Pages** and select **GitHub Actions** as the source.
3. Add the custom domain in **Settings → Pages → Custom domain** and configure the DNS records GitHub provides.
4. Enable **Enforce HTTPS** after the certificate is ready.

Every push to `main` will build and publish the site automatically.
