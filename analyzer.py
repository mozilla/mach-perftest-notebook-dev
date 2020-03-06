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

    
def main():
    
    print("running analyzer.py")

if __name__=="__main__":
    main()
    