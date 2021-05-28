from formatting import add_documentation_to_file

import click


@click.command()
@click.option('-f', '--file',
              prompt='the name of the python file you want to generate documentation for',
              help="Name of file to generate documentation for",
              type=str)
def main(file):
    add_documentation_to_file(file_name=file)


if __name__ == '__main__':
    main()