def create_cg_for_var(ast: list, var: str) -> tuple[list, int]:
    latest_use = -1
    is_root = False
    length = 0
    for item in ast:
        if isinstance(item, dict):
            if item["type"] == "call":
                if item["func"] == "*get_value" and item["args"][0] == f"${var}":
                    latest_use = length
                else:
                    result = create_cg_for_var(item["args"], var)
                    if result[1] != -1:
                        latest_use = length
                        ast[length]["args"] = result[0]
            elif item["type"] == "var":
                if item["name"] == var:
                    is_root = True
        elif isinstance(item, list):
            result = create_cg_for_var(item, var)
            if result[1] != -1:
                latest_use = length
                ast[length] = result[0]
        length += 1
    if is_root and latest_use != -1:
        ast.insert(latest_use + 1, {"type": "del", "var": [var]})
        return ast, latest_use
    elif is_root:
        ast.append({"type": "del", "var": [var]})
        return ast, latest_use
    else:
        return ast, latest_use


def get_vars(ast: list) -> list:
    var_list = []
    for item in ast:
        if isinstance(item, dict):
            if item["type"] == "call":
                var_list += get_vars(item["args"])
            elif item["type"] == "var":
                if item["var_type"] == "let":
                    var_list.append(item["name"])
        elif isinstance(item, list):
            var_list += get_vars(item)

    return list(set(var_list))


def remove_sqd_in_args(_ast: list) -> list:
    ast = _ast.copy()
    length = 0
    for item in ast:
        if type(item) == dict:
            if item["type"] == "call":
                if len(item["args"]) == 1:
                    if type(item["args"][0]) == list:
                        ast[length]["args"] = item["args"][0]
                        continue
            if item["type"] == "call":
                ast[length]["args"] = remove_sqd_in_args(ast[length]["args"])
        if type(item) == list:
            ast[length] = remove_sqd_in_args(ast[length])
        # 我也不知道为什么只能删除一部分，但是毕竟能删（shitcode）
        length += 1
    return ast


def codegen(ast: list) -> list:
    for var in get_vars(ast):
        ast = create_cg_for_var(ast, var)[0]
    # TODO 删除 ARGS 中多余中括号
    ast = remove_sqd_in_args(ast)
    return ast
