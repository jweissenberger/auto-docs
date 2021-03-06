# Auto-Docs

Auto-Docs is a CLI tool that automatically generates documentation for your python code using machine learning. 

This is a wrapper built around [this](https://huggingface.co/SEBIS/code_trans_t5_base_code_documentation_generation_python_multitask_finetune) HuggingFace model.

## Usage
I plan on releasing this as a pip package but for now the code can be run directly. 

Clone the repo and install requirements (I used python 3.8.8 but I assume it runs with other versions):
```bash
git clone https://github.com/jweissenberger/auto-docs.git
cd auto-docs
pip install -r requirements.txt
```

Then run `auto-docs.py` and pass in the name of the file you want to generate documentation for:
```bash
python auto-docs.py <name_of_your_python_file>
```
This will automatically download the HuggingFace model if you don't have it already.

## Results
auto-docs summarizes what functions do in plain english. For example, given this function:
```python
def chunks(l, n):
    d, r = divmod(len(l), n)
    for i in range(n):
        si = (d + 1) * (i if i < r else r) + d * (0 if i < r else i - r)
        yield l[si:si + (d + 1 if i < r else d)]
```
It updates it with:
```python
def chunks(l, n):
    """
    Split a list into n - sized chunks .
    """
    d, r = divmod(len(l), n)
    for i in range(n):
        si = (d + 1) * (i if i < r else r) + d * (0 if i < r else i - r)
        yield l[si:si + (d + 1 if i < r else d)]
```

You can see more results in `before.py` and `after.py`

## Tips
You can also specify the size of the model you would like to use in the command with `-m`.
The options are `small`, `medium`, or the default `large`. 
```bash
python auto-docs.py file_to_get_documentation_for.py -m small
```
The trade off is generally inference time vs quality of the summary.
You could hypothetically pass in any HuggingFace model but others probably won't work well.



auto-docs works better when you have good names for your functions and variables as they help it
infer what your code is accomplishing. 


