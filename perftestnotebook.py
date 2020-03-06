import json
import os
import pathlib
import yaml

import transformer as tfmr

from analyzer import NotebookAnalyzer
from notebookparser import parse_args
from task_processor import get_task_data_paths
from logger import NotebookLogger

import flask
from flask import Flask, Response, request, send_file

import webbrowser


logger = NotebookLogger()


class PerftestNotebook(object):
    """
    Controller class for the Perftest-Notebook.
    """

    def __init__(self, file_groups, config, custom_transform=None):
        """
        Initializes PerftestNotebook.

        :param dict file_groups: A dict of file groupings. The value
            of each of the dict entries is the name of the data that
            will be produced.
        :param str custom_transform: Path to a file containing custom
            transformation logic. Must implement the Transformer
            interface.
        """
        self.fmt_data = {}
        self.file_groups = file_groups
        self.config = config

        if custom_transform:
            if not os.path.exists(custom_transform):
                raise Exception("Cannot find the custom transform file.")
            import importlib

            tail, file = os.path.split(custom_transform)

            # Import the relevant module
            moduleDirectory = os.path.join(tail, os.path.splitext(file)[0])
            moduleStr = moduleDirectory.replace(os.path.sep, ".")
            module = importlib.import_module(moduleStr)

            # Look for classes that implements the Transformer class
            self.transformer = None
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) and issubclass(obj, tfmr.Transformer):
                    self.transformer = obj(files=[])
                    logger.info("Found %s transformer" % self.transformer.__class__.__name__)
                    break
            if not self.transformer:
                raise Exception("Could not get a transformer from %s" % custom_transform)
        else:
            self.transformer = tfmr.SimplePerfherderTransformer(files=[])

        self.analyzer = NotebookAnalyzer(data=None)

    def parse_file_grouping(self, file_grouping):
        """
        Handles differences in the file_grouping definitions. It can either be a
        path to a folder containing the files, a list of files, or it can contain
        settings from an artifact_downloader instance.

        :param file_grouping: A file grouping entry.
        :return: A list of files to process.
        """
        files = []
        if type(file_grouping) == list:
            # A list of files was provided
            files = file_grouping
        elif type(file_grouping) == dict:
            # A dictionary of settings from an artifact_downloader instance
            # was provided here
            files = get_task_data_paths(
                file_grouping["task_group_id"],
                file_grouping["path"],
                artifact=file_grouping["artifact"],
                artifact_dir=file_grouping.get("artifact_dir", None),
                run_number=file_grouping["run_number"],
            )
        elif type(file_grouping) == str:
            # Assume a path to files was given
            filepath = files

            newf = [f for f in pathlib.Path(filepath).rglob("*.json")]
            if not newf:
                # Couldn't find any JSON files, so take all the files
                # in the directory
                newf = [f for f in pathlib.Path(filepath).rglob("*")]

            files = newf
        else:
            raise Exception("Unknown file grouping type provided here: %s" % file_grouping)

        if not files:
            raise Exception("Could not find any files in this configuration: %s" % file_grouping)

        return files

    def process(self):
        """
        Process the file groups and return the results of the requested analyses.

        :return: All the results in a dictionary. The field names are the Analyzer
            funtions that were called.
        """
        fmt_data = []

        for name, files in self.file_groups.items():
            files = self.parse_file_grouping(files)
            if type(files) == dict:
                for subtest, files in files.items():
                    self.transformer.files = files

                    trfm_data = self.transformer.process(name)

                    if type(trfm_data) == list:
                        for e in trfm_data:
                            if "subtest" not in e:
                                e["subtest"] = subtest
                            else:
                                e["subtest"] = "%s-%s" % (subtest, e["subtest"])
                        fmt_data.extend(trfm_data)
                    else:
                        if "subtest" not in trfm_data:
                            trfm_data["subtest"] = subtest
                        else:
                            trfm_data["subtest"] = "%s-%s" % (subtest, trfm_data["subtest"],)
                        fmt_data.append(trfm_data)
            else:
                # Transform the data
                self.transformer.files = files
                trfm_data = self.transformer.process(name)

                if type(trfm_data) == list:
                    fmt_data.extend(trfm_data)
                else:
                    fmt_data.append(trfm_data)

        self.fmt_data = fmt_data

        if "analysis" in self.config:
            # Analyze the data
            all_results = {}
            self.analyzer.data = fmt_data
            for func in self.config["analysis"]:
                all_results[func] = getattr(self.analyzer, func)()
            return all_results

        return self.fmt_data


def main():
    args = parse_args()

    NotebookLogger.debug = args.debug

    config = None
    with open(args.config, "r") as f:
        logger.info("yaml_path: {}".format(args.config))
        config = yaml.safe_load(f)

    custom_transform = config.get("custom_transform", None)

    ptnb = PerftestNotebook(config["file_groups"], config, custom_transform=custom_transform)
    results = ptnb.process()

    if "analysis" in config:
        # TODO: Implement filtering techniques or add a configuration
        # for the analysis?
        new_results = {"ttest": []}
        for res in results["ttest"]:
            if abs(res["pval"]) < 0.005:
                new_results["ttest"].append(res)

        # Pretty print the results
        #print(json.dumps(new_results, sort_keys=True, indent=4))

        with open("fperf-testing-test.json", "w") as f:
            json.dump(new_results, f, indent=4, sort_keys=True)

        from matplotlib import pyplot as plt

        plt.figure()
        for c, entry in enumerate(new_results["ttest"]):
            plt.scatter([c for _ in entry["ts1"]], entry["ts1"], color="b")
            plt.scatter([c for _ in entry["ts2"]], entry["ts2"], color="r")
        plt.show(block=True)

    #print(json.dumps(ptnb.fmt_data, indent=4, sort_keys=True))

    prefix = "output" if "prefix" not in config else config["prefix"]
    filepath = "%s_fmt_data.json" % prefix

    if "output" in config:
        filepath = config["output"]

    print("Writing results to %s" % filepath)

    with open(filepath, "w") as f:
        json.dump(ptnb.fmt_data, f, indent=4, sort_keys=True)


    # Upload template file to Iodide
    template = 'testing/template/template.txt'
    tdata = ''
    with open(template, 'r') as f:
        tdata = f.read()

    html = ''
    with open('template_upload_file.html', 'r') as f:
        html = f.read()

    html = html.replace('replace_me', repr(tdata))
    with open('upload_file.html', 'w+') as f:
        f.write(html)
    
    webbrowser.open_new_tab('upload_file.html')

    # Set up local server data API. 
    # Iodide will visit localhost:5000/data
    app = Flask(__name__)
    app.config["DEBUG"]= False
    
    @app.route('/data', methods=['GET'])
    def return_data():

        script_path = os.path.dirname(__file__)
        data_relative_path = "testing/output/data.json"
        absolute_file_path = os.path.join(script_path,data_relative_path)

        response = flask.make_response(send_file(absolute_file_path))
        response.headers['Access-Control-Allow-Origin'] = '*'

        return response
    
    app.run()

if __name__=="__main__":
    main()
