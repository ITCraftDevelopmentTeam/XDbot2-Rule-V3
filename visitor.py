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


def codegen(ast: list) -> list:
    for var in get_vars(ast):
        ast = create_cg_for_var(ast, var)[0]
    # TODO 删除多余中括号
    return ast
