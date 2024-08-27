# Oplog Populate
Oplog Populate creates a sample client, project, and oplog within a Ghostwriter instance.

This tool demonstrates how to use Ghostwriter's GraphQL API to interact with Ghostwriter's data.

## Getting Started

First, clone the project.

Thern, fill out the config file with a valid set of Ghostwriter credentials
![image](https://github.com/user-attachments/assets/ed3d201c-c88e-40bb-8244-6592e8de3827)

Finally, run `oplog_populate.py`. Oplog Populate will create a custom client, project, and operation log and the operation 
log will be populated with data from `/config/oplog.csv`

If you want a new operation log, delete `/config/oplog.csv`. Oplog Populate will generate a new csv with 5,000 oplog entries.
