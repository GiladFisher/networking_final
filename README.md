# Packet Recording Analysis

This Python script is designed to analyze recordings of encrypted packets from network captures saved in PCAP format. The script will form a dataframe representing secure instant messages sizes and time of transmission. The script will then plot the data in a bar graph.

## Requirements

- Python 3 or higher (tested on Python 3.9)
- `pyshark` library
- `pandas` library
- `matplotlib` library

Install the required libraries using the following command:

```bash
pip install pyshark pandas matplotlib
```
## Usage
Simply replace the path in the arguments for recording_to_csv() with the path your own PCAP file and desired csv path and run the script. The script will output a bar graph of the data.

After running the script for the first time, a csv file will be created in the specified path. The script will use this csv file for future runs to save time. 

## Output
The script will output a bar graph of the data. The x-axis represents the time of transmission and the y-axis represents the size of the message in MBs.

***Here is an example of the output:***
![graph_2.PNG](..%2F..%2FDesktop%2Ffiles%20for%20project%2Frecording_2%2Fgraph_2.PNG)


