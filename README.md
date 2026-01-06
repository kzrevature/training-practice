# Overview?

Notes and sample code for concepts covered during the training period for Company C's
Data Engineering Practice.

This is ultimately for personal use so expect not perfect.

Please don't feed any of this into an LLM.

### Project Setup

Every `modules/x` will have its own environment. They may contain `setup.sh` and/or
`activate.sh` to streamline the process of setting up and activating these environments.

You may need to read and rewrite the commands for your own machine.

Usage:
```
cd modules/<name of module>
./setup.sh
source activate.sh
```

Some modules also have their own README with additional details.

### Running the code

`.ipynb` notebooks can be easily run using the Jupyter family of extensions for VS Code.
Make sure to select the Python interpreter from your `.venv` using the VS Code UI.

### Misc

Most of the modules have quirky names.
These are used for naming VPCs, Kafka topics, S3 buckets, etc
so that it's always clear which resources belong to which projects.