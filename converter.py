import os
import json
import argparse
from collections import defaultdict


def convert_txt_file_to_markdown(filename, output_dir):
    books_to_highlights = defaultdict(list)
    all_lines = open(filename, encoding="utf-8").read().splitlines()

    i = 0
    while i < len(all_lines):
        title = all_lines[i]

        if 'Your Highlight' in all_lines[i+1]:
            highlight = {
                "text": all_lines[i+3],
            }
            highlight["note"] = None

            if 'Your Note' in all_lines[i-4]:
                highlight["note"] = all_lines[i-2]

            books_to_highlights[title].append(highlight)

        i = i+5

    for title, highlight in books_to_highlights.items():
        markdown = convert_json_to_markdown({"title": title, "highlights": highlight})
        with open(os.path.join(output_dir, "{}.md".format(title)), "w") as f:
            f.write(markdown)


def convert_json_to_markdown(json_obj):
    highlights = json_obj["highlights"]
    markdown_lines = []

    for highlight in highlights:
        text = highlight["text"]
        markdown_lines.append("> {}".format(text))
        if highlight.get("location"):
            location = highlight["location"]["value"]
            url = highlight["location"]["url"]
            markdown_lines.append("[location: {0}]({1})".format(location, url))
        note = highlight["note"]
        if note is not None:
            markdown_lines.append("\n{0}".format(note))

        markdown_lines.append("\n")

    return "\n".join(markdown_lines)


def convert_json_files_to_markdown(filenames, output_dir):
    for filename in filenames:
        json_obj = json.load(open(filename, encoding='utf-8'))
        markdown = convert_json_to_markdown(json_obj)
        output_file = os.path.join(output_dir, "{}.md".format(json_obj["title"]))
        with open(output_file, "w") as f:
            f.write(markdown)


def convert(path, output_dir):
    """
    The main driver function. Calls appropriate method based on whether path points to a directory, a json file, or a
    .txt file
    """
    if os.path.isdir(path):
        filenames = [os.path.join(path, filename) for filename in os.listdir(path) if filename.endswith("json")]
        convert_json_files_to_markdown(filenames, output_dir)
    elif path.endswith(".json"):
        convert_json_files_to_markdown([path], output_dir)
    elif path.endswith(".txt"):
        convert_txt_file_to_markdown(path, output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--output", help="Output directory")
    args = parser.parse_args()

    path = args.path
    output_dir = args.output if args.output else "."

    convert(path, output_dir)
