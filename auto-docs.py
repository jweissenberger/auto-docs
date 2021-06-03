from formatting import add_documentation_to_file

import click


@click.command()
@click.argument('file_or_directory', type=click.Path(exists=True))
def main(file_or_directory):
    add_documentation_to_file(file_name=file_or_directory)
    print('\nFINISHED\n')


if __name__ == '__main__':
    main()