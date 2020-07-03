### kindledown
Convert kindle highlights and notes to markdown
### Usage
The input file should be one of:
- a json file created using [bookcision](https://readwise.io/bookcision)
- A folder that contains json files created using bookcision
- the 'My clippings.txt' file generated by Kindle

`python convert.py <path to folder/json file/ My clippings.txt> --output <output_dir>`

### Coming soon:
- Convert the .csv file generated by a readwise.io export
- Generate a contents.md page with a list of titles
- Allow abritrary markdown for highlights through a config file