import importlib.metadata as importlib_metadata
import sys
import gc





def get_file_size(input_obj):
    memory_size = 0
    ids = set()
    objects = [input_obj]
    while objects:
        new = []
        for obj in objects:
            if id(obj) not in ids:
                ids.add(id(obj))
                memory_size += sys.getsizeof(obj)
                new.append(obj)
        objects = gc.get_referents(*new)
    return memory_size




def get_framework_version(framework_name: str) -> str:
    try:
        get_pkg_version = importlib_metadata.version

        framework_version = get_pkg_version(framework_name)


    except importlib_metadata.PackageNotFoundError:
    # Note `importlib_metadata.version(package)` is not necessarily equal to
    # `__import__(package).__version__`. See the example for pytorch below.
    #
    # Example
    # -------
    # $ pip install torch==1.9.0
    # $ python -c "import torch; print(torch.__version__)"
    # 1.9.0+cu102
    # $ python -c "import importlib_metadata; print(importlib_metadata.version('torch'))"
    # 1.9.0
        framework_version = __import__(framework_name).__version__

    return framework_version



def infer_requirements(framework_name) -> str:
    framework_version = get_framework_version(framework_name)

    pip_requirements = f"{framework_name}=={framework_version}"

    return pip_requirements