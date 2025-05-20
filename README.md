# Universal Commands YAML with Aliases

This repo holds a structured YAML dataset of essential commands and snippets — starting with **Linux** but designed to expand across multiple languages and platforms like **Go**, **Python**, **Rust**, **C**, **Kubernetes**, and more.

## Why YAML + Aliases?

* **Aliases** let you hit topics with multiple search terms (e.g., `svc`, `svcs`, or `service` for systemd stuff).
* The clean YAML format makes it easy to **scale and extend** into any tech domain.
* Acts as a **single source of truth** for commands, helping automate docs, cheat sheets, APIs, or CLIs.

## How It Works with Sheet CLI

* The [sheet CLI](https://github.com/thinesh40/sheet-cli) fetches this YAML live.
* Search by topic or alias to instantly get commands/snippets in your terminal.
* Supports **multiple domains**, so you’ll soon find Go stdlib, Python, Rust, Kubernetes commands here too.

### Examples:

```bash
sheet linux network
sheet go fmt
sheet python io
sheet k8s pods
```

All thanks to the alias and extensible structure.

## Future Plans

* Add YAML sections for Go, Python, Rust, C, Kubernetes, and more.
* Build APIs and integrations (IDEs, chatbots) using this dataset as a unified backend.
* Enable users to add custom commands/snippets for their favorite tools and languages.

## Contributing

PRs welcome! Add your language/topic with `name`, `alias`, and `syntax` blocks in the same YAML style.

---

This keeps your repo future-ready, clean, and powerful for multiple DevOps and SRE toolsets. Want me to help draft example YAML sections for Rust or Kubernetes next?
