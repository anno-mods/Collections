
if __name__ == "__main__":
	from lxml import etree
	import os
	import codecs
	
	out_dir = "data/config/gui"
	in_dir = "../../maindata/data13/data/config/gui"
	assets_path = "../../maindata/data13/data/config/export/main/asset/assets.xml"

	def english_tooltip(product, cycles):
		if cycles == "1": cycle_string = "cycle"
		elif cycles != "12" and cycles[-1] == "2": cycle_string = "{}nd cycle".format(cycles)
		elif cycles != "13" and cycles[-1] == "3": cycle_string = "{}rd cycle".format(cycles)
		else: cycle_string = "{}th cycle".format(cycles)
		return "Produces {} every {}.".format(product, cycle_string)
		
	def german_tooltip(product, cycles):
		if cycles == "1": cycle_string = "Zyklus"
		else: cycle_string = "{}ten Zyklus".format(cycles)
		return "Produziert jeden {} {}.".format(cycle_string, product)


	def generate_mod_op(GUID, tooltip):
		xml = """	<ModOp Type="replace" Path="/TextExport/Texts/Text[GUID = '{}']/Text">
		  <Text>{}</Text>
	  </ModOp>"""
		return xml.format(GUID, tooltip)

	el = etree.parse(assets_path)
	relevant_nodes = el.xpath("//AdditionalOutput")
	found_items = {}

	# find all relevant items
	for node in relevant_nodes:
		Template = node.xpath("../../../Template/text()")[0]
		if Template == "GuildhouseItem":
			GUID = node.xpath("../../Standard/GUID/text()")[0]
			products = {item_node.xpath("./Product/text()")[0] : item_node.xpath("./AdditionalOutputCycle/text()")[0] for item_node in node.xpath("./Item")}
			fluff_text_id = node.xpath("../../ExpeditionAttribute/FluffText/text()")[0]
			found_items[GUID] = {"products" : products, "fluff_id" : fluff_text_id}
			
	translations = {
		"texts_english" : english_tooltip,
		"texts_german" : german_tooltip
	}

	# generate new tooltips
	tooltips = {}
	for filename in os.listdir(in_dir):
		if filename.endswith(".xml"):
			tooltips[filename] = {}
			
			# get existing tooltips
			el = etree.parse("{}/{}".format(in_dir, filename))
			
			# get product names
			product_name = {}
			for GUID in found_items:
				for product in found_items[GUID]["products"]:
					product_name[product] = el.xpath("//Text[GUID/text()='{}']/Text/text()".format(product))[0]
			
			for GUID in found_items:
				fluff_text = el.xpath("//Text[GUID/text()='{}']/Text/text()".format(found_items[GUID]["fluff_id"]))[0]
				additional_fluff_texts = [translations.get(filename, translations["texts_english"])(product_name[product], found_items[GUID]["products"][product]) for product in found_items[GUID]["products"]]
				new_fluff_text = "{}\n\n{}".format(fluff_text, "\n".join(additional_fluff_texts))
				tooltips[filename][GUID] = new_fluff_text
				#if filename == "texts_english.xml": print(new_fluff_text)
				
			with codecs.open("{}/{}".format(out_dir, filename), "w", encoding="utf-8") as out_file:
				out_file.write("<ModOps>\n")
				out_file.write("\n".join([generate_mod_op(found_items[GUID]["fluff_id"], tooltips[filename][GUID]) for GUID in tooltips[filename]]))
				out_file.write("\n</ModOps>")
				

        