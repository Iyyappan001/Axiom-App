"""Validate migration filenames and ordering before database integration."""

from pathlib import Path


def main() -> None:
    migrations = sorted(Path("app/data/migrations").glob("[0-9][0-9][0-9]_*.sql"))
    assert migrations, "no migrations found"
    assert [p.name[:3] for p in migrations] == ["001", "002", "003"]
    print(f"validated {len(migrations)} migrations")


if __name__ == "__main__":
    main()
