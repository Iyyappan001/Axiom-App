"""Kivy entry point; Android-specific setup belongs in adapters."""

from app.bootstrap import create_app


def main() -> None:
    create_app().run()


if __name__ == "__main__":
    main()
