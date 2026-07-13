from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from backend.app.rag.retriever import search


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage : python3 scripts/query_rag.py "
            "\"Comment faire opposition à une carte ?\""
        )
        raise SystemExit(1)

    query = " ".join(sys.argv[1:])

    results = search(
        query,
        top_k=4,
    )

    print()
    print(f"Question : {query}")
    print("=" * 80)

    for index, result in enumerate(results, start=1):
        print()
        print(f"Résultat {index}")
        print("-" * 80)
        print(f"Score       : {result.score}")
        print(f"Distance    : {result.distance}")
        print(f"Titre       : {result.title}")
        print(f"Domaine     : {result.domain}")
        print(f"Source      : {result.source_file}")

        if result.page is not None:
            print(f"Page        : {result.page}")

        if result.source_image:
            print(f"Image       : {result.source_image}")

        print()
        print(result.text[:1200])


if __name__ == "__main__":
    main()
