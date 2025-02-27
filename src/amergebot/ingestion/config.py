"""This module defines the configuration for data sources and stores in the Wandbot ingestion system.

This module contains classes that define the configuration for various data sources and stores used in the Wandbot
ingestion system. Each class represents a different type of data source or store, such as English and Japanese
documentation, example code, SDK code, and more. Each class is defined with various attributes like name,
data source, docstore directory, etc.

Typical usage example:

  data_store_config = DataStoreConfig()
  docodile_english_store_config = DocodileEnglishStoreConfig()
"""

import datetime
import pathlib
from typing import List, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from amergebot.utils import get_logger

logger = get_logger(__name__)


class DataSource(BaseSettings):
    cache_dir: pathlib.Path = Field("data/cache/raw_data", env="WANDBOT_CACHE_DIR")
    ignore_cache: bool = False
    remote_path: str = ""
    repo_path: str = ""
    local_path: Optional[pathlib.Path] = None
    branch: Optional[str] = None
    base_path: Optional[str] = ""
    file_patterns: List[str] = ["*.*"]
    is_git_repo: bool = False
    git_id_file: Optional[pathlib.Path] = Field(None, env="WANDBOT_GIT_ID_FILE")


class DataStoreConfig(BaseModel):
    name: str = "docstore"
    source_type: str = ""
    data_source: DataSource = DataSource()
    docstore_dir: pathlib.Path = pathlib.Path("docstore")

    @model_validator(mode="after")
    def _set_cache_paths(cls, values: "DataStoreConfig") -> "DataStoreConfig":
        values.docstore_dir = (
            values.data_source.cache_dir / "_".join(values.name.split()) / values.docstore_dir
        )
        data_source = values.data_source

        if data_source.repo_path:
            data_source.is_git_repo = urlparse(data_source.repo_path).netloc == "github.com"
            local_path = urlparse(data_source.repo_path).path.split("/")[-1]
            if not data_source.local_path:
                data_source.local_path = data_source.cache_dir / "_".join(values.name.split()) / local_path
            if data_source.is_git_repo:
                if data_source.git_id_file is None:
                    logger.debug(
                        "The source data is a git repo but no git_id_file is set."
                        " Attempting to use the default ssh id file"
                    )
                    data_source.git_id_file = pathlib.Path.home() / ".ssh" / "id_rsa"
        values.data_source = data_source

        return values


class DocodileEnglishStoreConfig(DataStoreConfig):
    name: str = "English Documentation"
    source_type: str = "documentation"
    data_source: DataSource = DataSource(
        remote_path="https://docs.wandb.ai/",
        repo_path="https://github.com/wandb/docodile",
        base_path="docs",
        file_patterns=["*.md"],
        is_git_repo=True,
    )
    language: str = "en"
    docstore_dir: pathlib.Path = pathlib.Path("wandb_documentation_en")


class ExampleCodeStoreConfig(DataStoreConfig):
    name: str = "Examples code"
    source_type: str = "code"
    data_source: DataSource = DataSource(
        remote_path="https://github.com/wandb/examples/tree/master/",
        repo_path="https://github.com/wandb/examples",
        base_path="examples",
        file_patterns=["*.py"],
        is_git_repo=True,
    )
    docstore_dir: pathlib.Path = pathlib.Path("wandb_examples_code")


class ExampleNotebookStoreConfig(DataStoreConfig):
    name: str = "Examples Notebooks"
    source_type: str = "notebook"
    data_source: DataSource = DataSource(
        remote_path="https://github.com/wandb/examples/tree/master/",
        repo_path="https://github.com/wandb/examples",
        base_path="colabs",
        file_patterns=["*.ipynb"],
        is_git_repo=True,
    )
    docstore_dir: pathlib.Path = pathlib.Path("wandb_examples_colab")


class SDKCodeStoreConfig(DataStoreConfig):
    name: str = "Wandb SDK code"
    source_type: str = "code"
    data_source: DataSource = DataSource(
        remote_path="https://github.com/wandb/wandb/tree/main/",
        repo_path="https://github.com/wandb/wandb",
        base_path="wandb",
        file_patterns=["*.py"],
        is_git_repo=True,
    )
    docstore_dir: pathlib.Path = pathlib.Path("wandb_sdk_code")


class SDKTestsStoreConfig(DataStoreConfig):
    name: str = "Wandb SDK tests"
    source_type: str = "code"
    data_source: DataSource = DataSource(
        remote_path="https://github.com/wandb/wandb/tree/main/",
        repo_path="https://github.com/wandb/wandb",
        base_path="tests",
        file_patterns=["*.py"],
        is_git_repo=True,
    )
    docstore_dir: pathlib.Path = pathlib.Path("wandb_sdk_tests")


class WeaveCodeStoreConfig(DataStoreConfig):
    name: str = "Weave SDK code"
    source_type: str = "code"
    data_source: DataSource = DataSource(
        remote_path="https://github.com/wandb/weave/tree/master/",
        repo_path="https://github.com/wandb/weave",
        base_path="weave",
        file_patterns=["*.py", "*.ipynb"],
        is_git_repo=True,
    )
    docstore_dir: pathlib.Path = pathlib.Path("weave_sdk_code")


class WeaveExamplesStoreConfig(DataStoreConfig):
    name: str = "Weave Examples"
    source_type: str = "code"
    data_source: DataSource = DataSource(
        remote_path="https://github.com/wandb/weave/tree/master/",
        repo_path="https://github.com/wandb/weave",
        base_path="examples",
        file_patterns=["*.py", "*.ipynb"],
        is_git_repo=True,
    )
    docstore_dir: pathlib.Path = pathlib.Path("weave_examples")


class WeaveDocStoreConfig(DataStoreConfig):
    name: str = "Weave Documentation"
    source_type: str = "documentation"
    data_source: DataSource = DataSource(
        remote_path="https://wandb.github.io/weave/",
        repo_path="https://github.com/wandb/weave",
        base_path="docs/docs",
        file_patterns=[
            "*.md",
        ],
        is_git_repo=True,
    )
    language: str = "en"
    docstore_dir: pathlib.Path = pathlib.Path("weave_documentation")


class WandbEduCodeStoreConfig(DataStoreConfig):
    name: str = "Wandb Edu code"
    source_type: str = "code"
    data_source: DataSource = DataSource(
        remote_path="https://github.com/wandb/edu/tree/main/",
        repo_path="https://github.com/wandb/edu",
        base_path="",
        file_patterns=["*.py", "*.ipynb", "*.md"],
        is_git_repo=True,
    )
    docstore_dir: pathlib.Path = pathlib.Path("wandb_edu_code")


class WeaveJsStoreConfig(DataStoreConfig):
    name: str = "Weave JS code"
    source_type: str = "code"
    data_source: DataSource = DataSource(
        remote_path="https://github.com/wandb/weave/tree/master/",
        repo_path="https://github.com/wandb/weave",
        base_path="weave-js",
        file_patterns=["*.js", "*.ts"],
        is_git_repo=True,
    )
    docstore_dir: pathlib.Path = pathlib.Path("weave_js")


class FCReportsStoreConfig(DataStoreConfig):
    name: str = "FC Reports"
    source_type: str = "report"
    data_source: DataSource = DataSource(
        remote_path="wandb-production",
        repo_path="",
        base_path="reports",
        file_patterns=["*.json"],
        is_git_repo=False,
    )
    docstore_dir: pathlib.Path = pathlib.Path("fc_reports")

    @model_validator(mode="after")
    def _set_cache_paths(cls, values: "DataStoreConfig") -> "DataStoreConfig":
        values.docstore_dir = values.data_source.cache_dir / values.name / values.docstore_dir
        data_source = values.data_source

        data_source.local_path = (
            data_source.cache_dir / values.name / f"reports_{int(datetime.datetime.now().timestamp())}.json"
        )
        values.data_source = data_source

        return values


class VectorStoreConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")
    collection_name: str = "vectorstore"
    persist_dir: pathlib.Path = pathlib.Path("data/cache/vectorstore")
    embedding_model_name: str = "text-embedding-3-small"
    tokenizer_model_name: str = "text-embedding-ada-002"
    embedding_dimensions: int = 512
    batch_size: int = 256
    artifact_url: str = Field(
        "wandbot/wandbot-dev/chroma_index:latest",
        env="WANDB_INDEX_ARTIFACT",
        validation_alias="wandb_index_artifact",
    )
