import js2py
filename = '20201229js.js'
with open(filename,'r') as f:
    content = f.read()

js_object = js2py.eval_js(content)
print(js_object)