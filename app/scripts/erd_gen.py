from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData
from config.settings import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_NAME

PG_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_NAME}"


def generate_erd():
    graph = create_schema_graph(metadata=MetaData(PG_URL))
    graph.write_png("DeFi ERD.png")


if __name__ == "__main__":
    generate_erd()
