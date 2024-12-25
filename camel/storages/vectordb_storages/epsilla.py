# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union, cast

if TYPE_CHECKING:
    from pyepsilla import vectordb, cloud

from camel.storages.vectordb_storages import (
    BaseVectorStorage,
    VectorDBQuery,
    VectorDBQueryResult,
    VectorDBStatus,
    VectorRecord,
)
from camel.types import VectorDistance
from camel.utils import dependencies_required

logger = logging.getLogger(__name__)


class EpsillaStorage(BaseVectorStorage):
    r"""An implementation of the `BaseVectorStorage` for interacting with
    Epsilla, a vector search engine.

    The detailed information about Epsilla is available at:
    `Epsilla <https://epsilla.com/>`_

    Notes:
        - If `url_and_api_key` is provided, it takes priority and the client
          will attempt to connect to the remote Epsilla instance using the URL
          endpoint.
        - If `url_and_api_key` is not provided and `path` is given, the client
          will use the local path to initialize Epsilla.
        - If neither `url_and_api_key` nor `path` is provided, the client will
          be initialized with default.
    """

    @dependencies_required('pyepsilla')
    def __init__(
        self,
        vector_dim: int,
        collection_name: Optional[str] = None,
        url_and_api_key: Optional[Tuple[str, str]] = None,
        path: Optional[str] = None,
        distance: VectorDistance = VectorDistance.COSINE,
        delete_collection_on_del: bool = False,
        **kwargs: Any,
    ) -> None:
        from pyepsilla import vectordb, cloud

        self._client: 
        self._local_path: Optional[str] = None
        self._create_client(url_and_api_key, path, **kwargs)

        self.vector_dim = vector_dim
        self.distance = distance
        self.collection_name = (
            collection_name or self._generate_collection_name()
        )

        self._check_and_create_collection()

        self.delete_collection_on_del = delete_collection_on_del

    def load(self) -> None:
        r"""Load the collection hosted on cloud service."""
        pass

    @property
    def client(self) -> "EpsillaClient":
        r"""Provides access to the underlying vector database client."""
        return self._client
