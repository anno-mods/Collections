import json, sys, os, math

# Check 190865 for all GUIDs when updating the json

def radius_function(data):
	return int(math.sqrt(data["module_limit"] * 15 /math.pi))

def generate_farm_module_owner(data):
	xml = """	<ModOp GUID = '{GUID}' Path="Values/ModuleOwner/ModuleBuildRadius" Type="merge">
			<ModuleBuildRadius>{radius}</ModuleBuildRadius>			 
	</ModOp>""".format(radius = radius_function(data), **data)
	return xml


try:
	if __name__ == "__main__":
		with open("farm_data.json") as farm_data_file:
			farm_data = json.load(farm_data_file)	
		
		mod_Ops = []
		for entry in farm_data["FarmData"]:
			mod_Ops.append(generate_farm_module_owner(entry))
			
		# write asset file
		with open("export/main/asset/assets.xml", "w") as file:
			file.write("<ModOps>\n")		
			file.write("\n".join(mod_Ops))
			file.write("\n</ModOps>") 
			
except Exception as err:
	print(err)
	print("Unexpected error:", sys.exc_info()[2].tb_lineno)
	input()