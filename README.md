# mach-perftest-notebook-dev
Development Repository for Mach Perftest Notebook Tooling. This tool will be used to standardize analysis/visualization techniques across Mozilla.

## Development Steps
These are the issues we will need to solve in this development repository (1 and 2 will likely need to be developed in parallel). The audience for this tool are software developers so we can take advantage of this for data transformation/standardization and other aspects of this tool.

1. Develop data standardization techniques.
    1. Ideas:
        1. Build a decorator to decoarte custom transform/standardization functions in a provided script.
        1. Use a named function from a supplied script as the transform function.
        1. In addition to these two, build simple transformers for simple data formats so they don't need to be rewritten by developpers.
1. Build some basic units of analysis/visualization in Python.
    1. Plotting data in a graph with custom x and y labels. Graph can be a line plot, scatter plot, or bar graph for now.
1. Dynamically integrate basic units into an Iodide web page.
    1. Ensure that each basic unit can have it's standardized data modified easily.

Each of these steps should have proper testing for the functionality as well, pytest will work fine in this case.

Once something basic is built, we will look into builing the mach tool for this in mozilla-central.

## Contributing
Feel free to ping us in #perftest for information on how to contribute.
 
