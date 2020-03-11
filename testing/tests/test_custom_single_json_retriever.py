import filecmp
import json
import perftestnotebook
import pytest
import yaml
from utilities import get_nested_values


class TestTransformer(object):
    def default_transformer(self, test_config_filepath, target_config_filepath):
        with open(test_config_filepath, "r") as f, open(target_config_filepath, "r") as g:

            test_config = yaml.safe_load(f)
            target_config = yaml.safe_load(g)
            assert "file_groups" in test_config
            assert "file_groups" in target_config

            test_ptnb = perftestnotebook.PerftestNotebook(test_config["file_groups"], test_config)
            target_ptnb = perftestnotebook.PerftestNotebook(
                target_config["file_groups"], target_config
            )

            target_resource_files = target_ptnb.parse_file_grouping(
                list(target_ptnb.file_groups.values())
            )

            target_resource_files = get_nested_values(target_resource_files)

            test_output_filepath = test_ptnb.parse_output()
            target_output_filepath = target_ptnb.parse_output()
            assert filecmp.cmp(test_output_filepath, target_output_filepath)

            with open(test_output_filepath, "r") as h:
                test_output = json.load(h)
                assert isinstance(test_output, list)

                for entry in test_output:
                    assert "data" in entry
                    assert isinstance(entry["data"], list)
                    assert "name" in entry
                    assert "subtest" in entry
                    assert len(entry) == 3

                    test_data_files, data_xaxis = set(), {}
                    for data in entry["data"]:
                        assert "file" in data
                        assert "value" in data
                        assert "xaxis" in data
                        assert len(data) == 3

                        test_data_files.add(data["file"])
                        data_xaxis.update({data["xaxis"]: data_xaxis.get(data["xaxis"], 0) + 1})

                    assert len(test_data_files) == len(target_resource_files)

                    for data in entry["data"]:
                        with open(data["file"], "r") as rf:
                            resource_data = json.load(rf)
                            nested_keys = entry["subtest"].split(".")
                            nested_values = get_nested_values(resource_data, nested_keys)

                            assert data["value"] in nested_values
                            assert len(nested_values) == data_xaxis[data["xaxis"]]

    def test_single_json_retriever(self):
        test_config = "testing/configs/config_single_json_test.yaml"
        target_config = "testing/configs/config_single_json.yaml"

        self.default_transformer(test_config, target_config)
