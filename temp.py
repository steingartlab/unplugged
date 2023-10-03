import json

from unplugged import controller, database

with open('dummy_meta.json', 'r') as json_file:
    meta = json.load(json_file)

# controller.write_meta(meta)


meta = controller.load_most_recent_meta()
print(meta)
# def write_meta(updated_jigs: dict) -> None:    
#     database_ = database.Metadata()
#     database_.write(meta)
#     database_.close()

# write_meta(meta)