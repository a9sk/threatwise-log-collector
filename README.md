# Winnie the phoo

Winnie the phoo (very original name), is a python tool for the collection and analysis of alerts and logs generated from different ThreatWise Metallic Honeypots.

## Guides

#### Explanation

For a brief explanation of what ThreatWise gives components wise read the file [explanation.md](explanation.md).

#### API Guide

For a guide on the API usage and overview read the file [TSOC_API.md](TSOC_API.md).

#### API CheatSheet

For an easier cheatsheet on the API calls read the file [cheatsheet_API.md](cheatsheet_API.md)


## Usage

To run the script use the following command from the main directory:
```python
python3 <PATH>/winnie.py -f <filename>.ini 
```
NOTE: change \<filename> with the actual name or path of your configuration file and \<PATH> with the path to the script from where you are in the terminal.

## TODO

- [x] Create a script to parse the addresses
- [x] Create a python script for the analysis of a single trap
- [x] Create a python script for the analysis of a whole configuration of traps
- [ ] Create a setup script to make the winnie.py run by only calling winnie in the terminal (symlink in linux)

## Licence

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).

## Contacts

To report bugs, request new features, or ask questions, contact the project author:

- Email: 920a9sk42f76c765@proton.me
- GitHub: [@a9sk](https://github.com/a9sk)