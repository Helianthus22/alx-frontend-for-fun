#!/usr/bin/python3
"""
This is a script to convert a Markdown file to HTML with advanced features.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import argparse
import pathlib
import re
import sys
import html  # Added for HTML escaping
import hashlib  # Added for MD5 hashing

def convert_md_to_html(input_file, output_file):
    '''
    Converts markdown file to HTML file with advanced features.
    '''
    try:
        # Read the contents of the input file
        with open(input_file, encoding='utf-8') as f:
            md_content = f.read()

        # Handle [[content]] for MD5 hashing
        md_content = re.sub(r'\[\[(.*?)\]\]', lambda x: hashlib.md5(x.group(1).encode()).hexdigest(), md_content)

        # Handle ((content)) for case-insensitive removal of 'c'
        md_content = re.sub(r'\(\((.*?)\)\)', lambda x: x.group(1).replace('c', '').replace('C', ''), md_content)

        # Split the content into lines
        md_lines = md_content.split('\n')

        html_content = []
        ul_opened = False
        ol_opened = False

        for line in md_lines:
            # Check if the line is a heading
            match = re.match(r'(#){1,6} (.*)', line)
            if match:
                # Get the level of the heading
                h_level = len(match.group(1)
                # Get the content of the heading and HTML escape it
                h_content = html.escape(match.group(2))
                # Append the HTML equivalent of the heading
                html_content.append(f'<h{h_level}>{h_content}</h{h_level}>')
            elif line.strip().startswith('- '):
                # Unordered list
                if not ul_opened:
                    html_content.append('<ul>')
                    ul_opened = True
                html_content.append(f'<li>{line[2:]}</li>')
            elif re.match(r'^\d+\.', line):
                # Ordered list
                if not ol_opened:
                    html_content.append('<ol>')
                    ol_opened = True
                html_content.append(f'<li>{line[line.index(" ") + 1:]}</li>')
            elif line:
                # Paragraph text
                html_content.append(f'<p>{html.escape(line)}</p>')

        if ul_opened:
            html_content.append('</ul>')
        if ol_opened:
            html_content.append('</ol>')

        # Write the HTML content to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_content))

    except Exception as e:
        print(f'An error occurred: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert markdown to HTML with advanced features')
    parser.add_argument('input_file', help='path to input markdown file')
    parser.add_argument('output_file', help='path to output HTML file')
    args = parser.parse_args()

    # Check if the input file exists
    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f'Missing {input_path}', file=sys.stderr)
        sys.exit(1)

    # Convert the markdown file to HTML
    convert_md_to_html(args.input_file, args.output_file)
