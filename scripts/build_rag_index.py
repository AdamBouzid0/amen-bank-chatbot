from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from backend.app.rag.indexer import build_index


def main() -> None:
    total = build_index(recreate=True)

    print()
    print("Index RAG créé avec succès")
    print("--------------------------")
    print(f"Nombre de chunks indexés : {total}")


if __name__ == "__main__":
    main()
