from formatting import add_documentation_to_file

import click


@click.command()
@click.argument('file_or_directory', type=click.Path(exists=True))
def main(file_or_directory):

    models = {
        'small': "SEBIS/code_trans_t5_small_code_documentation_generation_python_multitask_finetune",
        'medium': "SEBIS/code_trans_t5_base_code_documentation_generation_python_multitask_finetune",
        'base': "SEBIS/code_trans_t5_base_code_documentation_generation_python_multitask_finetune",
        'large': "SEBIS/code_trans_t5_large_code_documentation_generation_python_multitask_finetune"
    }

    add_documentation_to_file(file_name=file_or_directory)
    print('\nFINISHED\n')


if __name__ == '__main__':
    main()