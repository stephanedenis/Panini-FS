#!/usr/bin/env python3
"""
HeadlessEnvLoader — utilitaire minimal pour charger des secrets/env en mode headless.

Contrat léger:
- HeadlessEnvLoader(): construction sans argument
- is_headless_mode() -> bool
- get_github_token() -> Optional[str]
- get_fallback_config() -> Dict[str, Any]
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional


class HeadlessEnvLoader:
    def __init__(self) -> None:
        self._cache: Dict[str, Any] = {}

    def is_headless_mode(self) -> bool:
        # Activé si variable d'env HEADLESS=1 (par défaut False)
        return os.getenv("HEADLESS", "0") in {"1", "true", "TRUE", "yes", "YES"}

    @staticmethod
    def get_github_token() -> Optional[str]:
        # Cherche un token GitHub dans les variables standard
        for key in ("GITHUB_TOKEN", "GH_TOKEN", "GH_PAT"):
            val = os.getenv(key)
            if val:
                return val
        return None

    @staticmethod
    def get_fallback_config() -> Dict[str, Any]:
        return {
            "headless": os.getenv("HEADLESS", "0"),
            "github_user": os.getenv("GITHUB_USER", "stephanedenis"),
            "default_branch": os.getenv("DEFAULT_BRANCH", "main"),
        }


def main() -> None:
    loader = HeadlessEnvLoader()
    print({
        "headless": loader.is_headless_mode(),
        "gh_token_present": bool(loader.get_github_token()),
        "fallback": loader.get_fallback_config(),
    })


if __name__ == "__main__":
    main()
