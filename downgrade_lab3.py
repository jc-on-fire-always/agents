import json

ipynb_path = '/Users/as-mac-1214/Desktop/projects/agents/1_foundations/3_lab3.ipynb'

with open(ipynb_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

for cell in notebook.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = cell.get('source', [])
        source_str = ''.join(source)
        
        # Replace gemini-2.5-flash with gemini-1.5-flash due to rate limits
        if 'gemini-2.5-flash' in source_str:
            new_source = []
            for line in source:
                line = line.replace('"gemini-2.5-flash"', '"gemini-1.5-flash"')
                line = line.replace("'gemini-2.5-flash'", "'gemini-1.5-flash'")
                new_source.append(line)
            cell['source'] = new_source
            cell['outputs'] = []

with open(ipynb_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)

print("Successfully downgraded all gemini-2.5-flash occurrences to gemini-1.5-flash in lab3.")
