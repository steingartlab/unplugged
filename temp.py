import json

from unplugged import controller

with open('dummy_meta.json', 'r') as json_file:
    meta = json.load(json_file)


print(meta)
controller.write_meta(meta=meta)


meta = controller.load_most_recent_meta()
print(meta)