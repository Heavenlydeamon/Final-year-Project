import ast
import os
import sys

def get_python_files(root_dir):
    py_files = []
    # Apps to check, avoiding venv or .git
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.git' in dirpath or 'venv' in dirpath or 'migrations' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.py'):
                py_files.append(os.path.join(dirpath, filename))
    return py_files

def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {'error': f"Could not read file: {e}"}

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return {'syntax_error': f"Syntax error at line {e.lineno}: {e.msg}"}

    functions = []
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            functions.append({"name": node.name, "line": node.lineno})
        elif isinstance(node, ast.ClassDef):
            classes.append({"name": node.name, "line": node.lineno})
            
    return {
        'functions': functions,
        'classes': classes
    }

def analyze_project(root_dir):
    files = get_python_files(root_dir)
    report = {
        'syntax_errors': [],
        'read_errors': [],
        'all_functions': {},
        'all_classes': {},
        'file_details': {}
    }

    for f in files:
        rel_path = os.path.relpath(f, root_dir)
        res = analyze_file(f)
        
        if 'error' in res:
            report['read_errors'].append((rel_path, res['error']))
            continue
        if 'syntax_error' in res:
            report['syntax_errors'].append((rel_path, res['syntax_error']))
            continue
            
        report['file_details'][rel_path] = res
        
        for func in res['functions']:
            if func['name'] not in report['all_functions']:
                report['all_functions'][func['name']] = []
            report['all_functions'][func['name']].append({'file': rel_path, 'line': func['line']})
            
        for cls in res['classes']:
            if cls['name'] not in report['all_classes']:
                report['all_classes'][cls['name']] = []
            report['all_classes'][cls['name']].append({'file': rel_path, 'line': cls['line']})

    return report

def generate_markdown(report):
    md = "# Project Analysis Report\n\n"
    
    md += "## 1. Syntax Errors\n"
    if not report['syntax_errors']:
        md += "No syntax errors found.\n"
    else:
        for f, err in report['syntax_errors']:
            md += f"- **{f}**: {err}\n"
            
    md += "\n## 2. Duplicate Functions\n"
    dup_funcs = {name: locs for name, locs in report['all_functions'].items() if len(locs) > 1}
    # Filter out common names that are expected to be duplicated, e.g., __init__, __str__, get_context_data, etc.
    common_funcs = {'__init__', '__str__', 'get_context_data', 'setUp', 'tearDown', 'ready'}
    meaningful_dups = {n: l for n, l in dup_funcs.items() if n not in common_funcs}
    
    if not meaningful_dups:
        md += "No meaningful duplicate functions found.\n"
    else:
        for name, locs in meaningful_dups.items():
            md += f"### Function: `{name}`\n"
            for loc in locs:
                md += f"- `{loc['file']}` (Line {loc['line']})\n"
                
    md += "\n## 3. Duplicate Classes\n"
    dup_classes = {name: locs for name, locs in report['all_classes'].items() if len(locs) > 1}
    # Filter out common classes like Meta
    common_classes = {'Meta'}
    meaningful_dup_classes = {n: l for n, l in dup_classes.items() if n not in common_classes}
    
    if not meaningful_dup_classes:
        md += "No meaningful duplicate classes found.\n"
    else:
        for name, locs in meaningful_dup_classes.items():
            md += f"### Class: `{name}`\n"
            for loc in locs:
                md += f"- `{loc['file']}` (Line {loc['line']})\n"

    return md

if __name__ == '__main__':
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    report = analyze_project(root_dir)
    md = generate_markdown(report)
    with open('report.md', 'w', encoding='utf-8') as f:
        f.write(md)
    print("Report generated as report.md")
