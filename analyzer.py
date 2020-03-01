import numpy as np
import scipy.stats as stats

<<<<<<< HEAD
=======
import requests

import flask
from flask import Flask, Response, request, send_file
import os

import webbrowser
>>>>>>> scatter plot test data

class NotebookAnalyzer(object):
    """
    Analyze the standardized data. The methods in these functions
    will be injected in an Iodide page in the future.
    """

    def __init__(self, data):
        """
        Initialize the Analyzer.

        :param dict data: Standardized data, post-transformation.
        """
        self.data = data

    def split_subtests(self):
        """
        If the subtest field exists, split the data based
        on it, grouping data into subtest groupings.
        """
        if "subtest" not in self.data[0]:
            return {"": self.data}

        split_data = {}
        for entry in self.data:
            subtest = entry["subtest"]
            if subtest not in split_data:
                split_data[subtest] = []
            split_data[subtest].append(entry)

        return split_data

    def ttest(self):
        """
        Take the data and perform a cross-ttest on the rows.
        Data returned looks like the following:
        ```
            [
                {
                    'ttest': 7.2,
                    'pval': 0.01,
                    'name1': macosx-raptor,
                    'name2': macosx-browsertime
                }, ...
            ]
        ```

        :return dict: List of results.
        """
        results = []

        split_data = self.split_subtests()

        for subtest in split_data:
            done = {}
            for entry1 in split_data[subtest]:
                name = entry1["name"]

                for entry2 in split_data[subtest]:
                    if entry2["name"] == name:
                        continue
                    if (
                        "%s-%s" % (name, entry2["name"]) in done
                        or "%s-%s" % (entry2["name"], name) in done
                    ):
                        continue
                    done["%s-%s" % (name, entry2["name"])] = True

                    tval, pval = stats.ttest_ind(entry1["data"], entry2["data"])

                    results.append(
                        {
                            "ttest": tval,
                            "pval": pval,
                            "name1": name + "-%s" % subtest,
                            "name2": entry2["name"] + "-%s" % subtest,
                            "ts1": entry1["data"],
                            "ts2": entry2["data"],
                        }
                    )

        return results
<<<<<<< HEAD
=======
    '''
    # Later, create a seperate file/function for the server requests.
    def start_local_server():
        app = Flask(__name__)
    '''
    
def main():
    
    '''
    Currently not working. Might continue on this afterwards.
    # Post to Iodide
    def post_to_iodide():

        url = "http://localhost:8000/customize"      
        script_path = os.path.dirname(__file__)
        data_relative_path = "testing/template/template.txt"
        absolute_file_path = os.path.join(script_path,data_relative_path) 

        files = {'template':open(absolute_file_path,'rb')}

        requests.post(url,files=files)
        #print(r.text)
    '''


    # Flask localhost with API for Iodide
    app = Flask(__name__)
    app.config["DEBUG"]= True
    
    @app.route('/data', methods=['GET'])
    def return_data():

        script_path = os.path.dirname(__file__)
        data_relative_path = "testing/output/data.json"
        absolute_file_path = os.path.join(script_path,data_relative_path)

        response = flask.make_response(send_file(absolute_file_path))
        response.headers['Access-Control-Allow-Origin'] = '*'

        return response

    '''
    
    @app.route('/post',methods=['GET'])
    def send_template():
        post_to_iodide()
    
    '''

    webbrowser.open('upload_file.html')
    
    app.run()



    
    
    
    
    
    

if __name__=="__main__":
    main()
>>>>>>> scatter plot test data
