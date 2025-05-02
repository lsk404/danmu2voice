def write_append(text, path):
    with open(path, "a", encoding="utf-8") as f:  # 使用 "a" 模式追加
        f.write(text)