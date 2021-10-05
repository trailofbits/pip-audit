from pathlib import Path
from typing import Iterator, List

from packaging.requirements import Requirement
from pip_api import parse_requirements
from pip_api.exceptions import PipError

from pip_audit.dependency_source import (
    DependencyResolver,
    DependencyResolverError,
    DependencySource,
    DependencySourceError,
)
from pip_audit.service import Dependency


class RequirementSource(DependencySource):
    def __init__(self, filenames: List[Path], resolver: DependencyResolver):
        self.filenames = filenames
        self.resolver = resolver

    def collect(self) -> Iterator[Dependency]:
        # TODO(alex): I wonder whether we need to do some deduplication of requirements/dependencies
        # here
        for filename in self.filenames:
            try:
                reqs = parse_requirements(filename=filename)
            except PipError as pe:
                raise RequirementSourceError("requirement parsing raised an error") from pe

            # Invoke the dependency resolver to turn requirements into dependencies
            reqs: List[Requirement] = [Requirement(str(req)) for req in reqs.values()]
            try:
                for _, deps in self.resolver.resolve_all(reqs):
                    for dep in deps:
                        yield dep
            except DependencyResolverError as dre:
                raise RequirementSourceError("dependency resolver raised an error") from dre


class RequirementSourceError(DependencySourceError):
    pass
