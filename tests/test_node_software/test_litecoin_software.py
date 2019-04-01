import os
from tempfile import TemporaryDirectory

import pytest

from node_launcher.constants import TARGET_LITECOIN_RELEASE, OPERATING_SYSTEM, WINDOWS
from node_launcher.services.litecoin_software import LitecoinSoftware


def mock_get_latest_release_version(*args):
    return TARGET_LITECOIN_RELEASE


@pytest.fixture
def litecoin_software():
    with TemporaryDirectory() as tmpdirname:
        litecoin_software = LitecoinSoftware(tmpdirname)
        litecoin_software.get_latest_release_version = mock_get_latest_release_version
        return litecoin_software


class TestLitecoinSoftware(object):
    @pytest.mark.slow
    def test_litecoin_qt(self, litecoin_software: LitecoinSoftware):
        assert os.path.isfile(litecoin_software.litecoin_qt)

    def test_release_version(self, litecoin_software: LitecoinSoftware):
        assert litecoin_software.release_version == TARGET_LITECOIN_RELEASE.replace('v', '')

    @pytest.mark.slow
    def test_get_latest_release_version(self):
        latest = LitecoinSoftware().get_latest_release_version()
        if latest is not None:
            assert latest == TARGET_LITECOIN_RELEASE

    def test_binary_name(self, litecoin_software: LitecoinSoftware):
        assert litecoin_software.download_name

    def test_binaries_directory(self, litecoin_software: LitecoinSoftware):
        d = litecoin_software.downloads_directory_path
        assert os.path.isdir(d)

    def test_binary_directory(self, litecoin_software: LitecoinSoftware):
        d = litecoin_software.binary_directory_path
        assert os.path.isdir(d)

    def test_download_url(self, litecoin_software: LitecoinSoftware):
        url = litecoin_software.download_url
        if OPERATING_SYSTEM == WINDOWS:
            assert url == 'https://litecoincore.org/bin/litecoin-core-0.17.1/litecoin-0.17.1-win64.zip'
        assert url

    @pytest.mark.slow
    def test_download(self, litecoin_software: LitecoinSoftware):
        litecoin_software.download()
        assert os.path.isfile(litecoin_software.download_compressed_path)
