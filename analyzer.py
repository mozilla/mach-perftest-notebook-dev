import numpy as np
import scipy.stats as stats


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

    def get_header(self):
        template_header_path = "testing/resources/template/header"
        with open(template_header_path, "r") as f:
            template_header_content = f.read()
            return template_header_content

    def get_analysis_template(self,func):
        template_function_folder_path = "testing/resources/analysis-templates/"
        template_function_file_path = template_function_folder_path + func
        print(template_function_file_path)
        with open(template_function_file_path,"r") as f:
            return f.read()


def main():
    
    print("running analyzer.py")
    analyzer = NotebookAnalyzer(None)
    print(analyzer.get_header())

    tempString = analyzer.get_analysis_template("scatterplot")
    print(tempString)


if __name__=="__main__":
    main()
    