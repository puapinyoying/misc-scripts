## Script for organizing high-throughput imaging files

By: Prech Brian Uapinyoying

Updated: 12/21/2018

#### Notes 

- `organize_nd2.py` 
    + The main python3 script used to organize high throughput images from a 384 well plate into folders according to drugs and doses. It will also rename files with spaces and commas in the process. 

    + It's an example of how you can use regular expressions and python to move, rename and organize large amounts of files into more complex directory structures. 

    + File names must have a specific naming scheme for it to work. Here is an example of a few filenames used. Note that they contain key information such as experimental conditions, well number, and channels used. In addition, there are spaces and commas in the filename which can cause trouble:
        
        - 'grn_d6_24hr_posttx_WellA01_Channel405 nm,488 nm,561 nm,640 nm_Seq0024.nd2'
        - 'grn_d6_24hr_posttx_WellG01_Channel405 nm,488 nm,561 nm,640 nm_Seq0144.nd2'
        - 'grn_d6_24hr_posttx_WellM03_Channel405 nm,488 nm,561 nm,640 nm_Seq0290.nd2'

    + The code can be modifed to accept a different filenaming scheme by modifying the REGEXP formula or changing the drug and dose directory names etc.

- `notes_on_organize_nd2.ipynb`
    + Jupyter notebook that walks through in detail all the logic that went into writing `organize_nd2.py`

- `create_orig_files.sh`
    + bash script that can be run to generate example files to test `organize_nd2.py` which is also used for follwing along with the jupyter notebook.

- `test_sample_list.txt`
    + the original file names

- `README.MD` 
    + this file... 