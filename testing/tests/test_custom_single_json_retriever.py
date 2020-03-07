from utilities import get_values_from_nested_object
import filecmp
import json
import pytest


def test_single_json_retriever():
    """
    At present, only test JSON file.
    """
    actual_file = "testing/outputs/single_json_output_test.json"
    expected_file = "testing/outputs/single_json_output.json"
    assert filecmp.cmp(actual_file, expected_file)

    with open(actual_file, "r") as af:
        actual_data = json.load(af)
        assert isinstance(actual_data, list)

        for entry in actual_data:
            assert "data" in entry
            assert isinstance(entry["data"], list)
            assert "name" in entry
            assert "subtest" in entry

            for data in entry["data"]:
                assert "file" in data
                assert "value" in data
                assert "xaxis" in data

                with open(data["file"], "r") as rf:
                    resource_data = json.load(rf)
                    nested_keys = entry["subtest"].split(".")

                    assert data["value"] in get_values_from_nested_object(resource_data, nested_keys)
