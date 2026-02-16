"""
Google Translate in Flow Launcher.

Translate text via Google Translate and copy the result to clipboard.
"""

from flowlauncher import FlowLauncher, FlowLauncherAPI
import urllib.parse
import urllib.request
import html
import re
import textwrap
import subprocess


# Defaults and config
DEFAULT_FROM_LANG = "auto"
DEFAULT_TO_LANG = "vi"
GOOGLE_TRANSLATE_CHECK_URL = "https://translate.google.com/"
GOOGLE_TRANSLATE_API_URL = "https://translate.google.com/m?tl=%s&sl=%s&q=%s"
RESULT_CONTAINER_PATTERN = re.compile(r'class="result-container">(.*?)<')
WRAP_LENGTH = 200
ICON_PATH = "Images/gt.png"

HINT_TITLE = "Text to translate"
HINT_SUBTITLE = "input only | from:to text | :to text"
ERROR_TITLE = "Invalid notation or no internet connection"
ERROR_SUBTITLE = "Please verify and try again"


def translate(text, to_lang=None, from_lang=None, wrap_len=WRAP_LENGTH):
    """Fetch translation from Google Translate and return wrapped result."""
    to_lang = to_lang or DEFAULT_TO_LANG
    from_lang = from_lang or DEFAULT_FROM_LANG
    quoted_text = urllib.parse.quote(text)
    url = GOOGLE_TRANSLATE_API_URL % (to_lang, from_lang, quoted_text)
    request = urllib.request.Request(
        url, headers={"User-Agent": "Edge, Brave, Firefox, Chrome, Opera"}
    )
    raw_response = urllib.request.urlopen(request).read()
    html_content = raw_response.decode("utf-8")
    match = RESULT_CONTAINER_PATTERN.search(html_content)
    result = html.unescape(match.group(1)) if match else ""
    width = (
        int(wrap_len)
        if isinstance(wrap_len, str) and wrap_len.isdigit()
        else WRAP_LENGTH
    )
    return "\n".join(textwrap.wrap(result, width))


def copy_to_clipboard(text):
    """Copy text to system clipboard."""
    subprocess.check_call(f"echo {text.strip()}|clip", shell=True)


def _parse_query(raw_query):
    """
    Parse raw query into (from_lang, to_lang, text).
    Supports: plain text | from:to text | :to text
    """
    stripped = raw_query.strip()
    from_lang = DEFAULT_FROM_LANG
    to_lang = DEFAULT_TO_LANG
    text = stripped

    parts = stripped.split(" ", 1)
    if len(parts) > 1 and ":" in parts[0]:
        prefix, text = parts[0], parts[1].strip()
        if prefix.startswith(":"):
            to_lang = prefix[1:].strip() or DEFAULT_TO_LANG
        else:
            lang_parts = prefix.split(":", 1)
            from_lang = lang_parts[0].strip() or DEFAULT_FROM_LANG
            to_lang = lang_parts[1].strip() if len(lang_parts) > 1 else DEFAULT_TO_LANG

    return from_lang, to_lang, text


def _result_item(title, subtitle, copy_translation=None):
    """Build a Flow Launcher result dict."""
    item = {
        "Title": title,
        "SubTitle": subtitle,
        "IcoPath": ICON_PATH,
        "ContextData": "ctxData",
    }
    if copy_translation is not None:
        item["JsonRPCAction"] = {"method": "copy", "parameters": [copy_translation]}
    return item


class GoogTranslate(FlowLauncher):

    def query(self, query):
        results = []
        try:
            urllib.request.urlopen(GOOGLE_TRANSLATE_CHECK_URL)
        except OSError:
            results.append(_result_item(ERROR_TITLE, ERROR_SUBTITLE))
            return results

        if not query.strip():
            results.append(_result_item(HINT_TITLE, HINT_SUBTITLE))
            return results

        from_lang, to_lang, text = _parse_query(query)
        if not text:
            results.append(_result_item(HINT_TITLE, HINT_SUBTITLE))
            return results

        translation = translate(text, to_lang, from_lang)
        results.append(
            _result_item(
                f"{to_lang}: {translation}",
                f"{from_lang}: {text}",
                copy_translation=translation,
            )
        )
        return results

    def copy(self, translation):
        """Copy translation to clipboard and show confirmation."""
        FlowLauncherAPI.show_msg("Copied to clipboard", copy_to_clipboard(translation))


if __name__ == "__main__":
    GoogTranslate()
