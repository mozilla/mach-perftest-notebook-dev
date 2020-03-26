import filecmp
import json
import perftestnotebook
import pytest
import yaml
from perftestnotebook.utilities import get_nested_values
from functools import reduce
from operator import add
from pathlib import Path


class TestTransformer(object):
    def check_transformation(self, test_config_filepath, target_config_filepath, get_nested_keys):
        """
        This function checks:
            - File existance.
            - Both test and local config files from the arguments have "file_groups" field.
            - Each entry of the transformed output has "data", "name", and "subtest" fields.
                - Each "data" field has "file", "value", and "xaxis" fields.
                    - Each file from "file" field is included in the
                     "file_groups" field of the config file.
                    - The number of files from "file" field is equal to
                     the size of "file_groups" of the config file.
                    - The number of xaxis from "xaxis" field is equal to
                     the number of items got from the resource object by
                      nested keys.
                    - Each value from "value" field is included in the
                     values got from the recource object by nested key. 
                    - The length of "data" field is equal to the sum of
                     the occuerrence of each xaxis.
            - The test output file is the same as the local output file.

        :param str test_config_filepath: The test config file directory.
        :param str target_config_filepath: The local config file directory.
        :param function get_nested_keys: A function to get nested keys.
         The result is used to get data value from resource files.
        """

        # Check if config files exists.
        assert Path(test_config_filepath).exists()
        assert Path(target_config_filepath).exists()

        # Check both test and local config files have "file_groups" field.
        with open(test_config_filepath, "r") as f, open(target_config_filepath, "r") as g:
            test_config = yaml.safe_load(f)
            target_config = yaml.safe_load(g)
        assert "file_groups" in test_config
        assert "file_groups" in target_config

        test_ptnb = perftestnotebook.PerftestNotebook(
            test_config["file_groups"], test_config, sort_files=True
        )
        target_ptnb = perftestnotebook.PerftestNotebook(
            target_config["file_groups"], target_config, sort_files=True
        )

        # Get resource files from local config.
        target_resource_files = set()
        for name, files in target_ptnb.file_groups.items():
            file_groups = target_ptnb.parse_file_grouping(files)
            if isinstance(file_groups, list):
                target_resource_files.update(file_groups)
            else:
                for entry in file_groups.values():
                    target_resource_files.update(entry)

        # Get output files.
        test_output_filepath = test_ptnb.parse_output()
        target_output_filepath = target_ptnb.parse_output()
        assert Path(test_output_filepath).exists()
        assert Path(target_output_filepath).exists()

        # Check if the test output file exists.
        assert Path(test_output_filepath).exists()
        with open(test_output_filepath, "r") as f:
            test_output = json.load(f)
        assert isinstance(test_output, list)

        test_data_files = set()
        for entry in test_output:
            # Check fields existance.
            assert "data" in entry
            assert isinstance(entry["data"], list)
            assert "name" in entry
            assert "subtest" in entry
            assert len(entry) == 3

            data_xaxis = {}
            for data in entry["data"]:
                # Check fields existance.
                assert "file" in data
                assert "value" in data
                assert "xaxis" in data
                assert len(data) == 3

                # Check if each file from "file" field is included in the
                # "file_groups" field of the config file.
                assert data["file"] in target_resource_files

                test_data_files.add(data["file"])
                data_xaxis.update({data["xaxis"]: data_xaxis.get(data["xaxis"], 0) + 1})

            # Check if the number of xaxis from "xaxis" field is equal to the
            # number of items got from the recource object by nested keys.
            assert len(entry["data"]) == reduce(add, data_xaxis.values())

            for data in entry["data"]:
                assert Path(data["file"]).exists()
                with open(data["file"], "r") as f:
                    resource_data = json.load(f)
                nested_keys = get_nested_keys(entry)
                nested_values = get_nested_values(resource_data, nested_keys)

                # Check if each value from "value" field is included in the
                # values got from the recource object by nested key.
                assert data["value"] in nested_values
                assert len(nested_values) == data_xaxis[data["xaxis"]]

        # Check the total number of files from "file" field is equal to the
        # size of "file_groups" of the config file.
        assert len(test_data_files) == len(target_resource_files)

        # Check if both test and local output file have the same content.
        assert filecmp.cmp(test_output_filepath, target_output_filepath, shallow=False)

    def test_simple_perfherder_transformer(self):
        test_config = "testing/configs/config_artifactdownloader_output_test.yaml"
        target_config = "testing/configs/config_artifactdownloader_output.yaml"
        self.check_transformation(test_config, target_config, lambda anything: ["suites", "value"])

    def test_single_json_retriever(self):
        test_config = "testing/configs/config_single_json_test.yaml"
        target_config = "testing/configs/config_single_json.yaml"
        self.check_transformation(
            test_config, target_config, lambda entry: entry["subtest"].split(".")
        )
