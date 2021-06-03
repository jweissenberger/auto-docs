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


def pull_out_top_function(file_string, indentation):
    if file_string.find('def ') == -1:
        return None

    lines = file_string.split('\n')

    end = False
    decorators = False  # you can have multiple decorators on a function and we want to include them
    start_and_end = []  # first index is the start of the function and second is the end
    for index in range(len(lines)):
        line = lines[index]

        # these are all of the scenarios I can think of where a function would end (looking line by line)

        # case where a new function is being defined with a decorator
        if len(line) > 1 and '@' == line[0]:
            end = True
            if not decorators:
                start_and_end.append(index)
            decorators = True

        # case where a function is being defined with no indentation or a class is being defined
        elif len(line) > 5 and 'def ' == line[:4]:
            end = True
            if not decorators:
                start_and_end.append(index)

            decorators = False

        # case where there is code underneath either of these statements (auto-docs is only designed for functions)
        elif 'if __name__ == "__main__"' in line or "if __name__ == '__main__'" in line:
            end = True
            start_and_end.append(index)

        # case where there is another function defined at the same indentation as the current function (like in a class)
        # using len(indentation) here is important because it could be tabs or spaces
        elif len(line) > len(indentation) + 4 and f'{indentation}def ' == line[:len(indentation) + 4]:
            end = True
            if not decorators:
                start_and_end.append(index)
            decorators = False

        # case where a function has a decorator at the same indentation (like a static method in a class)
        elif len(line) > len(indentation) + 1 and f'{indentation}@' == line[:len(indentation) + 1]:
            end = True
            if not decorators:
                start_and_end.append(index)
            decorators = True

        # the code inside a function will always be indented so if a line begins with a character other than a tab or
        # space, it must be the start of another piece of code
        elif end:
            if len(line) and not line[0].isspace():
                start_and_end.append(index)

        if len(start_and_end) == 2:
            break

    if len(start_and_end) == 1:
        function = '\n'.join(lines[start_and_end[0] - 1:])
    elif len(start_and_end) == 2:
        function = '\n'.join(lines[start_and_end[0] - 1:start_and_end[1] - 1])
    else:
        raise Exception(
            'File parsing error, please check the file formatting. If this is unexpected, please open an issue here: '
            'https://github.com/jweissenberger/auto-docs/issues/new'
        )

    return function.strip()


def get_function_name(function: str):

    name = function.split('def')[1].split('(')[0].strip()

    return name


def get_indentation(sub_file_string: str):

    lines = sub_file_string.split('\n')

    for line in lines:
        if 'def ' in line:
            return line.split('def ')[0]


def add_documentation_to_file(file_name,
                              model_name="SEBIS/code_trans_t5_large_code_documentation_generation_python_multitask_finetune",
                              ):

    file = read_file(file_name)
    print(f"Generating documentation for {file_name}")

    sub_file = file
    new_file = file

    while 'def ' in sub_file:

        indent = get_indentation(sub_file)
        function = pull_out_top_function(sub_file, indent)

        name = get_function_name(function)

        # skip class inits
        if name == "__init__":
            sub_file = file[file.find(function) + len(function):]
            continue

        print(f'Generating documentation for {name}')

        original_function = function
        summary = generate_code_summary(function.strip(), model_and_tokenizer=model_name)

        function = function.replace('):\n', f'):\n{indent}    """\n{indent}    {summary}\n{indent}    """\n', 1)

        new_file = new_file.replace(original_function, function)

        sub_file = file[file.find(original_function) + len(
            original_function):]  # grab the rest of the file after the function

    write_file(file_name, new_file)
    print(f"Generated documentation for {file_name}")
