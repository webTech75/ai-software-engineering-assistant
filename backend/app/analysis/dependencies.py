# from pathlib import Path
# import re

# from app.analysis.base import BaseAnalyzer


# class DependencyAnalyzer(BaseAnalyzer):
#     """
#     Analyze project dependencies.
#     """

#     def analyze(self, project_directory: str) -> dict:

#         root = Path(project_directory)

#         packages = []

#         requirements = root / "requirements.txt"

#         if requirements.exists():

#             for line in requirements.read_text(
#                 encoding="utf-8",
#                 errors="ignore",
#             ).splitlines():

#                 line = line.strip()

#                 if not line or line.startswith("#"):
#                     continue

#                 match = re.match(
#                     r"^([A-Za-z0-9_.\-\[\]]+)\s*([<>=!~].+)?$",
#                     line,
#                 )

#                 if match:
#                     packages.append(
#                         {
#                             "name": match.group(1),
#                             "version": match.group(2).strip() if match.group(2) else None,
#                         }
#                     )

#         return {
#             "dependencies": {
#                 "python": {
#                     "manager": "pip",
#                     "packages": packages,
#                 }
#             }
#         }