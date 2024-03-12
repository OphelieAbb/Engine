import utilities.urpc_services as services

asset_ser = services.asset_service()
asset_module = asset_ser.get_asset_module()

dep_services = services.dependency_service()
asset_ser = services.asset_service()
asset_module = asset_ser.get_asset_module()

juice_service = services.juice_service()


# Test types
# asset_type_string = test_asset.get_type_string()
# type_to_find = f"ASSETTYPE_{asset_type_string}".upper()
# asset_type_id = asset_ser.get_asset_type_by_name(type_to_find)
# asset_list = asset_module.get_assets_of_type(asset_type_id)
# print(f"There is {len(asset_list)} asset of type {asset_type_string} | TYPE ID: {asset_type_id} | STRING TYPE NAME:{type_to_find}")
# Get asset type id
#asset_type_id = asset_ser.get_asset_type_by_name(f"ASSETTYPE_{reconstructed_type_string}")
# Asset Type list
asset_types = ["ASSETTYPE_FACEBUILDER_ANIMATION","ASSETTYPE_ANIMATION",]

data = {"error_count":0}
# Search by type

for asset_type in asset_types:
    data[asset_type] = {}
    # Get asset type id for type filtering
    asset_type_id = asset_ser.get_asset_type_by_name(asset_type)
    asset_list = asset_module.get_assets_of_type(asset_type_id)
    i = 0
    print(f"Working on {len(asset_list)} of type {asset_type} | {asset_type_id}")
    for asset in asset_list:
        #if asset.get_name() != "a_mq_020_can_cin_cantoescape_kay_facial":
        #   continue
        data[asset_type][asset.get_name()] = dict(
            count = 0,
            asset_deps = []
        )

        try:
            animation_name = asset.get_name().lower()
            dependency_session = dep_services.open_tree_session()
            dependency_node = dependency_session.find(asset.get_filenames()[0])

            # Get parent
            parent_nodes = dependency_node.get_parent_array()

            # uids = []
            # names = []
            for dep in parent_nodes:
                path = dep.get_file()
                print(f"\tWorking on {path}")
                if "dependencies" in path:
                    continue
                if "metadata" in path:
                    continue
                dep_asset = asset_module.get_asset_by_real_filename(path)
                data[asset_type][asset.get_name()]["asset_deps"].append(dep_asset.get_name().lower())
                data[asset_type][asset.get_name()]["count"] = len(data[asset_type][asset.get_name()]["asset_deps"])
            i += 1
        except Exception as e:
            data["error_count"] = data["error_count"] + 1
            print(f"\tSomething went wrong: {e}")

from pprint import pprint
# pprint( data[asset_type])

import json
with open(r"D:\test.json", "w") as f:
    f.write(json.dumps(data, indent=4))