import pytest
import filecmp


def test_single_json_retriever():
    actual_file = "testing/outputs/single_json_output_test.json"
    expected_file = "testing/outputs/single_json_output.json"
    assert filecmp.cmp(actual_file, expected_file)
