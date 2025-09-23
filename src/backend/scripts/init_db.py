from src.backend.db import get_engine, Base


def main() -> None:
    engine = get_engine(echo=True)
    Base.metadata.create_all(engine)
    print("Database tables created.")


if __name__ == "__main__":
    main()



