# Google Translate for Flow Launcher

Translate text with [Google Translate](https://translate.google.com/) and copy the result from [Flow Launcher](https://www.flowlauncher.com/).

## How to use

Trigger with **tr** (or your configured keyword), then:

| Input | Example | Description |
|-------|---------|-------------|
| **Text only** | `tr hello world` | Translates to Vietnamese (default). Source language is auto-detected. |
| **:to** | `tr :vi hello world` | Same as above: auto-detect source, translate to the language after `:`. |
| **from:to** | `tr en:vi hello world` | Translate from English to Vietnamese. |

- **Copy**: Select the result (Enter) to copy the translation to the clipboard.

Default target language is **Vietnamese** (`vi`). Use the `:to` or `from:to` prefix to change source and target (e.g. `:es`, `en:ja`).

## Credit

Modified from [Wox.Plugin.GoogleTranslate](https://github.com/laercioskt/Wox.Plugin.GoogleTranslate) by [laercioskt](https://github.com/laercioskt).
