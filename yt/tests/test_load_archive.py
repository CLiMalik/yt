import sys

import pytest

from yt.config import ytcfg
from yt.loaders import load_archive
from yt.sample_data.api import _download_sample_data_file, get_data_registry_table
from yt.testing import requires_module_pytest


@pytest.fixture()
def data_registry():
    yield get_data_registry_table()


@pytest.fixture()
def tmp_data_dir(tmp_path):
    print(tmp_path)
    pre_test_data_dir = ytcfg["yt", "test_data_dir"]
    ytcfg.set("yt", "test_data_dir", str(tmp_path))

    yield tmp_path

    ytcfg.set("yt", "test_data_dir", pre_test_data_dir)


@requires_module_pytest("pooch")
@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="Should not work on Windows",
)
@pytest.mark.parametrize(
    "fn ,exact_loc, class_",
    [
        (
            "ToroShockTube.tar.gz",
            "ToroShockTube/DD0001/data0001",
            "EnzoDataset",
        ),
        (
            "ramses_sink_00016.tar.gz",
            "ramses_sink_00016/output_00016",
            "RAMSESDataset",
        ),
    ],
)
def test_load_archive(fn, exact_loc, class_: str, tmp_data_dir, data_registry):
    # First load the sample file (.tar.gz'd file)
    archive_path = _download_sample_data_file(filename=fn)
    # Now try opening the tar directly
    ds = load_archive(archive_path, exact_loc)
    assert type(ds).__name__ == class_


@pytest.mark.skipif(
    not sys.platform.startswith("win"),
    reason="Should not work on Windows",
)
def test_load_archive_fail_windows():
    with pytest.raises(RuntimeError):
        load_archive("whatever")
