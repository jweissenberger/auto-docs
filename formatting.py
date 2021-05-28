from transformers import AutoTokenizer, AutoModelWithLMHead, SummarizationPipeline
import warnings
import os


warnings.filterwarnings("ignore")


def generate_code_summary(code_snippet,
                          model_and_tokenizer=
                          "SEBIS/code_trans_t5_large_code_documentation_generation_python_multitask_finetune"):

    pipeline = SummarizationPipeline(
        model=AutoModelWithLMHead.from_pretrained(model_and_tokenizer),
        tokenizer=AutoTokenizer.from_pretrained(model_and_tokenizer, skip_special_tokens=True)
    )

    return pipeline([code_snippet])[0]['summary_text']


def read_file(file_name):

    assert os.path.isfile(file_name), "Must pass in a file or a path to a file"
    assert file_name[-3:] == '.py', "File must be a '.py' file "

    f = open(file_name, 'r')
    file = f.read()
    f.close()

    return file


def write_file(file_name, file_contents):

    f = open(file_name, 'w')
    f.write(file_contents)
    f.close()


def pull_out_top_function(file_string):
    # find first def
    index = file_string.find('def ')  # won't work if something ends in def like a variable
    if index == -1:
        return None

    # then grab all of the following text until there is no space between a newline character and the next character
    # (signifying the first code outside the function)
    sub_file = file_string[index:]
    for i in range(len(sub_file) - 1):
        # you don't look for return statements because there can be more than one
        if sub_file[i] == '\n' and not sub_file[i + 1].isspace():
            return sub_file[:i]

    # def was found but
    return sub_file.strip()


def get_function_name(function: str):

    name = function.split('def')[1].split('(')[0].strip()

    return name


def add_documentation_to_file(file_name,
                              model_name="SEBIS/code_trans_t5_large_code_documentation_generation_python_multitask_finetune",
                              ):

    file = read_file(file_name)
    print(f"Generating documentation for {file_name}")

    sub_file = file
    new_file = file

    while 'def ' in sub_file:
        function = pull_out_top_function(sub_file)

        name = get_function_name(function)
        print(f'Generating documentation for {name}')

        original_function = function
        summary = generate_code_summary(function, model_and_tokenizer=model_name)

        # TODO won't work for functions within classes or things that need more spaces
        # need to find a way to dynamically get the correct spacing
        function = function.replace(':\n', f':\n    """\n    {summary}\n    """\n', 1)  # TODO this won't work for the case where theres a lot of type hints in the function definition and theres a ':\n'

        new_file = new_file.replace(original_function, function)

        sub_file = file[file.find(original_function) + len(
            original_function):]  # grab the rest of the file after the function

    write_file(file_name, new_file)
    print(f"Generated documentation for {file_name}")
