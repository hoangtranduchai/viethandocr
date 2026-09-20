import json

with open('01_Data_Preparation_and_EDA.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'def build_metadata' in ''.join(cell['source']):
        source = ''.join(cell['source'])
        new_source = source.replace(
            "'image_path': img_path,",
            "'image_path': img_path[img_path.find('UIT_HWDB_'):] if 'UIT_HWDB_' in img_path else img_path,"
        )
        cell['source'] = [line + '\n' for line in new_source.split('\n')]
        # Remove trailing newline from the last element if any, or just let json dump handle it.
        # Actually split('\n') adds an empty string at the end if it ends with \n.
        # Let's just do an exact string replace without messing with split/join if we can.
        # Let's revert source to a simpler replace on the list itself.

# A safer way to replace in list of strings:
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        for i, line in enumerate(cell['source']):
            if "'image_path': img_path," in line:
                cell['source'][i] = line.replace(
                    "'image_path': img_path,",
                    "'image_path': img_path[img_path.find('UIT_HWDB_'):] if 'UIT_HWDB_' in img_path else img_path,"
                )

with open('01_Data_Preparation_and_EDA.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
