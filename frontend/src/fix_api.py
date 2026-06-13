import os
import re

src_dir = r'C:\Users\Prateek\Downloads\Vehicle_Parking_v2-4e42283744af637e3546aada8321ca17616e7cc0\Vehicle_Parking_v2-4e42283744af637e3546aada8321ca17616e7cc0\frontend\src'
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.vue') or file.endswith('.js'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = re.sub(r"fetch\('/api/", "fetch(`${window.API_URL}/api/", content)
            new_content = re.sub(r"\$\{window\.API_URL\}/api/([^'`]*)'", r"${window.API_URL}/api/\1`", new_content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed: {file}")

print("Done!")