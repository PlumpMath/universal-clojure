import json
import sys
import util.treadle as tr


with open(sys.argv[1]) as f:
    nodes = json.load(f)["items"][1:]


node_emitters = {}
const_emitters = {}

def node_emitter(f):
    node_emitters[f.__name__.replace("_", "-").replace("--compile-", "")] = f
    return f

def const_emitter(f):
    const_emitters[f.__name__.replace("_", "-").replace("--compile-", "")] = f
    return f

def compile_node(node, env):
    return node_emitters[node["node-type"]](node, env)

def compile_const(node, env):
    return const_emitters[node["data-type"]](node, env)

@node_emitter
def __compile_const(node, env):
    return compile_const(node, env)

@const_emitter
def __compile_string(node, env):
    return tr.Const(node["value"])

@node_emitter
def __compile_invoke(node, env):
    fn = tr.Global(node["fn"]["value"])
    args = []
    for x in node["args"]:
        args.append(compile_node(x, env))

    return tr.Call(fn, *args)


@const_emitter
def __compile_nil(node, env):
    return tr.Const(None)

nodes = [{"node-type": "const", "data-type": "string", "value": "foo"}]
print nodes
for x in nodes:
    print x
    comp = compile_node(x, {})
    print comp.toFunc()()
