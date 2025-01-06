import os

from amergebot.ingestion import prepare_data, preprocess_data, vectorstores
from amergebot.ingestion.report import create_ingestion_report
from amergebot.utils import get_logger

logger = get_logger(__name__)


def main():
    project = os.environ.get("WANDB_PROJECT")
    entity = os.environ.get("WANDB_ENTITY")

    raw_artifact = prepare_data.load(project, entity)
    preprocessed_artifact = preprocess_data.load(project, entity, raw_artifact)
    vectorstore_artifact = vectorstores.load(
        project, entity, preprocessed_artifact
    )

    create_ingestion_report(project, entity, raw_artifact, vectorstore_artifact)
    print(vectorstore_artifact)


if __name__ == "__main__":
    main()
