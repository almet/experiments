from string import Template


with open('myfile.template', 'r') as f:
    content = f.read()

print(Template(content).substitute(foo='Foo !', bar='Babar'))
