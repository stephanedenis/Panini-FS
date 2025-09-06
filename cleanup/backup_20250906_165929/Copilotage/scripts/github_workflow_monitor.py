#!/usr/bin/env python3
"""
GitHubWorkflowMonitor — monitor minimal (structure) pour état des workflows.

Contrat léger:
- GitHubWorkflowMonitor(): construction sans argument
- check_all_repos_status() -> Dict
"""
from __future__ import annotations

import os
from typing import Dict, List


class GitHubWorkflowMonitor:
    def __init__(self) -> None:
        self.user = os.getenv("GITHUB_USER", "stephanedenis")

    def check_all_repos_status(self) -> Dict:
        # Version minimale: renvoie un squelette de données
        return {
            "user": self.user,
            "repos": [],
            "summary": {
                "workflows": 0,
                "alerts": 0,
                "status": "unknown",
            },
        }


def main() -> None:
    monitor = GitHubWorkflowMonitor()
    print(monitor.check_all_repos_status())


if __name__ == "__main__":
    main()
