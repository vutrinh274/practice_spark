import os
from dataclasses import dataclass
from pathlib import Path
import yaml

PROBLEMS_DIR = Path(os.getenv("PROBLEMS_DIR", "/problems"))
SPARK_PROBLEMS_DIR = os.getenv("SPARK_PROBLEMS_DIR", "/problems")

VALID_STRATEGIES = {"dataframe_equal", "dataframe_equal_ordered", "schema_only", "row_count"}
VALID_SOURCES = {"csv", "parquet", "json"}


@dataclass
class Dataset:
    name: str
    source: str
    path: str  # relative to problem dir, as seen by Spark Connect server


@dataclass
class Validation:
    strategy: str
    ordered: bool = False
    type_coerce: bool = False


@dataclass
class Problem:
    id: str
    title: str
    difficulty: str
    tags: list[str]
    datasets: list[Dataset]
    validation: Validation
    reference_solution: str
    schema: dict[str, list[dict]]  # table -> [{column, type}]
    description: str = ""
    hint_paths: list[Path] = None      # ordered list of hint markdown paths
    solution_paths: dict[str, Path] = None  # {"sql": Path, "dataframe": Path}

    def __post_init__(self):
        if self.hint_paths is None:
            self.hint_paths = []
        if self.solution_paths is None:
            self.solution_paths = {}


_registry: dict[str, Problem] = {}


def _load_problem(problem_dir: Path) -> Problem:
    yaml_path = problem_dir / "problem.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"problem.yaml not found in {problem_dir}")

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    # Validate strategy
    strategy = data.get("validation", {}).get("strategy", "dataframe_equal")
    if strategy not in VALID_STRATEGIES:
        raise ValueError(f"Unknown validation strategy '{strategy}'. Valid: {VALID_STRATEGIES}")

    datasets = []
    for ds in data.get("datasets", []):
        source = ds["source"]
        if source not in VALID_SOURCES:
            raise ValueError(f"Unknown dataset source '{source}'. Valid: {VALID_SOURCES}")
        # Resolve path relative to Spark Connect server's mount point
        spark_path = f"{SPARK_PROBLEMS_DIR}/{data['id']}/{Path(ds['path']).name}"
        datasets.append(Dataset(name=ds["name"], source=source, path=spark_path))

    validation = Validation(
        strategy=strategy,
        ordered=data.get("validation", {}).get("ordered", False),
        type_coerce=data.get("validation", {}).get("type_coerce", False),
    )

    description_path = problem_dir / "problem.md"
    description = description_path.read_text() if description_path.exists() else ""

    hint_paths = [
        problem_dir / Path(h).name if "/" not in h else problem_dir / h.lstrip("./")
        for h in data.get("hints", [])
        if (problem_dir / h.lstrip("./")).exists()
    ]

    raw_solution = data.get("solution", {})
    solution_paths = {}
    for mode in ("sql", "dataframe"):
        if mode in raw_solution:
            p = problem_dir / raw_solution[mode].lstrip("./")
            if p.exists():
                solution_paths[mode] = p

    return Problem(
        id=data["id"],
        title=data["title"],
        difficulty=data["difficulty"],
        tags=data.get("tags", []),
        datasets=datasets,
        validation=validation,
        reference_solution=str(problem_dir / data.get("reference", {}).get("solution", "reference.py")),
        schema=data.get("schema", {}),
        description=description,
        hint_paths=hint_paths,
        solution_paths=solution_paths,
    )


def load_registry() -> None:
    registry_path = PROBLEMS_DIR / "registry.yaml"
    if not registry_path.exists():
        raise FileNotFoundError(f"registry.yaml not found at {registry_path}")

    with open(registry_path) as f:
        registry = yaml.safe_load(f)

    for entry in registry.get("problems", []):
        raw_path = entry["path"].lstrip("./")
        problem_dir = PROBLEMS_DIR / raw_path
        problem = _load_problem(problem_dir)
        _registry[problem.id] = problem


def get_problem(problem_id: str) -> Problem:
    if not _registry:
        load_registry()
    if problem_id not in _registry:
        raise KeyError(f"Problem '{problem_id}' not found in registry")
    return _registry[problem_id]


def list_problems() -> list[Problem]:
    if not _registry:
        load_registry()
    return list(_registry.values())


def get_dataset_local_path(problem: Problem, dataset_name: str) -> Path:
    """Return the local filesystem path for a dataset file."""
    ds = next((d for d in problem.datasets if d.name == dataset_name), None)
    if ds is None:
        raise KeyError(f"Dataset '{dataset_name}' not found in problem '{problem.id}'")
    return PROBLEMS_DIR / problem.id / Path(ds.path).name
