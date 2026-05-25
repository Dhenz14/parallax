import importlib.metadata
import json
import os
import urllib.request


DEFAULT_RELEASE_API_URL = "https://api.github.com/repos/Dhenz14/parallax/releases/latest"


def get_current_version():
    version = "unknown"
    try:
        version = importlib.metadata.version("parallax")
    except Exception:
        try:
            import parallax

            version = getattr(parallax, "__version__", "unknown")
        except Exception:
            pass
    return version


def check_latest_release():
    """
    Check if the current version matches the latest GitHub release.
    If not, print an update notification.
    """
    version = get_current_version()
    release_api_url = os.environ.get("PARALLAX_RELEASE_API_URL", DEFAULT_RELEASE_API_URL)
    try:
        with urllib.request.urlopen(release_api_url, timeout=4) as response:
            data = json.loads(response.read())
            latest = data.get("tag_name") or data.get("name")
            if latest:
                latest = latest.lstrip("vV")
                ver = version.lstrip("vV")
                if latest != ver:
                    print(
                        f"\033[93m[Parallax] New version available: {latest} (current: {ver})\033[0m\n"
                        f"For macOS, run `git pull && pip install -e '.[mac]'` to update.\n"
                        f"For Linux, run `git pull && pip install -e '.[gpu]'` to update.\n"
                        f"For Windows, run `parallax install` to update\n"
                    )
    except Exception:
        pass
