import json, sys, os

def fill_buffs(buffs):
	if buffs is None: buffs = {}
	possible_buffs = ["FactoryUpgrade", "ElectricUpgrade", "KontorUpgrade", "PassiveTradeGoodGenUpgrade", "ModuleOwnerUpgrade", "BuildingUpgrade","ResidenceUpgrade", "PopulationUpgrade", "CultureUpgrade", "ShipyardUpgrade", "TradeShipUpgrade", "AttackerUpgrade", "AttackableUpgrade", "ProjectileUpgrade"]
	for possible_buff in possible_buffs:
		buffs[possible_buff] = buffs.get(possible_buff, "")
	return buffs


def generate_buff_description(text, cur_id):
	cur_id += 1
	xml = """	<ModOp GUID="15767" Type="addNextSibling">
		<Asset>
		  <Template>Text</Template>
		  <Values>
			<Standard>
			  <GUID>{}</GUID>
			  <Name>academy buff description {}</Name>
			</Standard>
			<Text>
			  <LocaText>
				<English>
				  <Text>{}</Text>
				  <Status>Exported</Status>
				  <ExportCount>1</ExportCount>
				</English>
			  </LocaText>
			  <LineID>22729</LineID>
			</Text>
		  </Values>
		</Asset>
	</ModOp>""".format(cur_id, cur_id, text)
	return xml, cur_id

def generate_buff(description_id, fluff_id, cur_id, icon_path, name, buffs = None, targets = None):
	cur_id += 1
	buffs = fill_buffs(buffs)
	targets = "\n".join(["""				<Item>
				  <GUID>{}</GUID>
				</Item>""".format(target) for target in targets]) if targets else None
	xml = """	<ModOp GUID="191145" Type="addNextSibling">
		<Asset>
		  <Template>HarbourOfficeBuff</Template>
		  <Values>
			<Standard>
			  <GUID>{id}</GUID>
			  <Name>academy buff {id}</Name>
			  <IconFilename>{icon}</IconFilename>
			  <InfoDescription>{info_id}</InfoDescription>
			</Standard>
			<ItemEffect>
			  <EffectTargets>
				<Item>
				  <GUID>191563</GUID>
				</Item>
				{other_targets}
			  </EffectTargets>
			</ItemEffect>
			<Text>
			  <LocaText>
				<English>
				  <Text>{name}</Text>
				  <Status>Exported</Status>
				  <ExportCount>1</ExportCount>
				</English>
			  </LocaText>
			  <LineID>21927</LineID>
			</Text>
			<FactoryUpgrade> {FactoryUpgrade} </FactoryUpgrade>
			<BuildingUpgrade> {BuildingUpgrade} </BuildingUpgrade>
			<Buff>
			  <PossibleFluffTexts>
				<Item>
				  <FluffText>{fluff_id}</FluffText>
				</Item>
			  </PossibleFluffTexts>
			</Buff>
			<AttackerUpgrade> {AttackerUpgrade} </AttackerUpgrade>
			<VisitorHarborUpgrade>
			  <SpawnProbabilityFactor>
				<Value>10</Value>
				<Percental>1</Percental>
			  </SpawnProbabilityFactor>
			</VisitorHarborUpgrade>
			<VisitorUpgrade />
			<PassiveTradeGoodGenUpgrade> {PassiveTradeGoodGenUpgrade} </PassiveTradeGoodGenUpgrade>
			<KontorUpgrade> {KontorUpgrade} </KontorUpgrade>
			<AttackableUpgrade />
			<PierUpgrade />
			<CultureUpgrade> {CultureUpgrade} </CultureUpgrade>
			<ShipyardUpgrade> {ShipyardUpgrade} </ShipyardUpgrade>
			<ElectricUpgrade> {ElectricUpgrade} </ElectricUpgrade>
			<TradeShipUpgrade> {TradeShipUpgrade} </TradeShipUpgrade>
			<PopulationUpgrade> {PopulationUpgrade} </PopulationUpgrade>
			<ResidenceUpgrade> {ResidenceUpgrade} </ResidenceUpgrade>
			<ModuleOwnerUpgrade> {ModuleOwnerUpgrade} </ModuleOwnerUpgrade>
		  </Values>
		</Asset>
	</ModOp>""".format(id = cur_id, icon = icon_path, fluff_id = fluff_id, info_id = description_id, name = name, other_targets = targets, **buffs)
	return xml, cur_id

def generate_item_set_description(text, cur_id):
	cur_id += 1
	xml= """	<ModOp GUID="15360" Type="addNextSibling">
		<Asset>
		  <Template>Text</Template>
		  <Values>
			<Standard>
			  <GUID>{}</GUID>
			  <Name>academy expositions fluff {}</Name>
			</Standard>
			<Text>
			  <LocaText>
				<English>
				  <Text>{}</Text>
				  <Status>Exported</Status>
				  <ExportCount>2</ExportCount>
				</English>
			  </LocaText>
			</Text>
		  </Values>
		</Asset>
	</ModOp>""".format(cur_id, cur_id, text)
	return xml, cur_id

def generate_item_set(description_id, cur_id, buff_id, icon_path, name, scope = "Area"):
	cur_id += 1
	xml = """	<ModOp GUID="191130" Type="addNextSibling">
		<Asset>
		  <Template>ItemSet</Template>
		  <Values>
			<Standard>
			  <GUID>{}</GUID>
			  <Name>academy expositions {}</Name>
			  <IconFilename>{}</IconFilename>
			  <InfoDescription>{}</InfoDescription>
			</Standard>
			<ItemSocketSet>
			  <SetBuff>{}</SetBuff>
			  <BuffScope>{}</BuffScope>
			</ItemSocketSet>
			<Text>
			  <LocaText>
				<English>
				  <Text>{}</Text>
				  <Status>Exported</Status>
				  <ExportCount>1</ExportCount>
				</English>
			  </LocaText>
			  <!--<LineID>21962</LineID> -->
			</Text>
			<Locked />
		  </Values>
		</Asset>
	</ModOp>""".format(cur_id, cur_id,icon_path, description_id, buff_id, scope, name)
	return xml, cur_id

def generate_reward_pool(item_ids, cur_id):
	item_pool = []
	item_pool.append("""			  <ItemsPool>""")
	item_pool.extend(["""				<Item>
				  <ItemLink>{}</ItemLink>
				</Item>""".format(id) for id in item_ids])
	item_pool.append("""			  </ItemsPool>""")
	item_pool = "\n".join(item_pool)
	cur_id += 1
	xml = """	<ModOp GUID="191510" Type="addNextSibling">
		<Asset>
		  <Template>RewardPool</Template>
		  <Values>
			<Standard>
			  <GUID>{}</GUID>
			  <Name>Academy Specialists Pool {}</Name>
			  <IconFilename>data/ui/2kimages/main/3dicons/specialists/systemic/icon_normaldress_810.png</IconFilename>
			</Standard>
			<RewardPool>
{}
			  <IgnoreUnlocks>1</IgnoreUnlocks>
			</RewardPool>
			<Locked />
			<Text />
		  </Values>
		</Asset>
	</ModOp>""".format(cur_id, cur_id, item_pool)
	return xml, cur_id
	
def register_reward_pool(pool_id, buff_id):
	xml = """	<ModOp GUID="2001173" Path="Values/TourismFeature/SpecialistPoolsThroughSets" Type="add">
		<Item>
		  <Pool>{}</Pool>
		  <UnlockingSetBuff>{}</UnlockingSetBuff>
		  <Weight>3</Weight>
		</Item>
	</ModOp>""".format(pool_id, buff_id)
	return xml

def update_set_item(item_id, item_set_id):
	xml = """	<ModOp GUID="{}" Path="Values/Item" Type="add">
		<ItemSet>{}</ItemSet>
	</ModOp>""".format(item_id, item_set_id)
	return xml
	
def generate_tourism_texts(language, buff_description, buff_fluff, item_set_description, name, buff_id, item_set_id, buff_description_id, buff_fluff_id, item_set_description_id, default_language = "english"):
	buff_fluff = buff_fluff[language] if language in buff_fluff else buff_fluff[default_language]
	buff_description = buff_description[language] if language in buff_description else buff_description[default_language]
	item_set_description = item_set_description[language] if language in item_set_description else item_set_description[default_language]
	name = name[language] if language in name else name[default_language]
	
	xml = """	<ModOp Type="add" Path="/TextExport/Texts">
    <Text>
      <GUID>{}</GUID>
      <Text>{}</Text>
    </Text>
  </ModOp>
  <ModOp Type="add" Path="/TextExport/Texts">
    <Text>
      <GUID>{}</GUID>
      <Text>{}</Text>
    </Text>
  </ModOp>
  <ModOp Type="add" Path="/TextExport/Texts">
    <Text>
      <GUID>{}</GUID>
      <Text>{}</Text>
    </Text>
  </ModOp>
  <ModOp Type="add" Path="/TextExport/Texts">
    <Text>
      <GUID>{}</GUID>
      <Text>{}</Text>
    </Text>
  </ModOp>
  <ModOp Type="add" Path="/TextExport/Texts">
    <Text>
      <GUID>{}</GUID>
      <Text>{}</Text>
    </Text>
  </ModOp>""".format(buff_id, name, item_set_id, name, buff_description_id, buff_description, item_set_description_id, item_set_description,buff_fluff_id,buff_fluff)
	return xml
	
def generate_other_texts(language, item_set_description, name, item_set_id, item_set_description_id, default_language = "english"):
	item_set_description = item_set_description[language] if language in item_set_description else item_set_description[default_language]
	name = name[language] if language in name else name[default_language]
	
	xml = """	<ModOp Type="add" Path="/TextExport/Texts">
    <Text>
      <GUID>{}</GUID>
      <Text>{}</Text>
    </Text>
  </ModOp>
  <ModOp Type="add" Path="/TextExport/Texts">
    <Text>
      <GUID>{}</GUID>
      <Text>{}</Text>
    </Text>
  </ModOp>""".format(item_set_id, name, item_set_description_id, item_set_description)
	return xml
	
	
	
buffs = {}
try:
	if __name__ == "__main__":
		base_guid = 93109711
		fluff_guid = 931097111
		with open("buffs.json") as buffs_file:
			buffs = json.load(buffs_file)	
		
		# set up lists to store xml
		xml_parts = []
		item_set_ids = []
		backup_language = buffs["backup_language"]
		texts = {}
		for language in buffs["localizations"]:
			texts[language] = []
		
		# create xml for each tourism set
		for buff_set in buffs["tourism_sets"]:
			buff_description, buff_description_guid = generate_buff_description(buff_set["buff_description"][backup_language], base_guid)
			base_guid = buff_description_guid
			xml_parts.append(buff_description)
			
			buff_fluff, buff_fluff_guid = generate_buff_description(buff_set["buff_fluff"][backup_language], fluff_guid)
			fluff_guid = buff_fluff_guid
			xml_parts.append(buff_fluff)
			
			other_buffs = buff_set.get("buffs", None)
			targets = buff_set.get("targets", None)
			buff, buff_guid = generate_buff(buff_description_guid, buff_fluff_guid, base_guid, buff_set["item_set_icon"], buff_set["name"][backup_language], other_buffs, targets)
			base_guid = buff_guid
			xml_parts.append(buff)
			item_set_description, item_set_description_guid = generate_item_set_description(buff_set["item_set_description"][backup_language], base_guid)
			base_guid = item_set_description_guid
			xml_parts.append(item_set_description)
			item_set, item_set_guid = generate_item_set(item_set_description_guid, base_guid, buff_guid, buff_set["item_set_icon"], buff_set["name"][backup_language])
			base_guid = item_set_guid
			xml_parts.append(item_set)
			reward_pool, reward_pool_guid = generate_reward_pool(buff_set["pool_items"], base_guid)
			base_guid = reward_pool_guid
			xml_parts.append(reward_pool)
			xml_parts.append(register_reward_pool(reward_pool_guid, buff_guid))
			for set_item in buff_set["set_items"]:
				xml_parts.append(update_set_item(set_item, item_set_guid))
			item_set_ids.append(item_set_guid)
			for language in texts:
				texts[language].append(generate_tourism_texts(language, buff_set["buff_description"], buff_set["buff_fluff"], buff_set["item_set_description"], buff_set["name"], buff_guid, item_set_guid, buff_description_guid, buff_fluff_guid, item_set_description_guid, backup_language))
			
			
		# create xml for each tourism set
		for buff_set in buffs["other_sets"]:
			item_set_description, item_set_description_guid = generate_item_set_description(buff_set["item_set_description"][backup_language], base_guid)
			base_guid = item_set_description_guid
			xml_parts.append(item_set_description)
			item_set, item_set_guid = generate_item_set(item_set_description_guid, base_guid, buff_set["buff_id"], buff_set["item_set_icon"], buff_set["name"][backup_language], buff_set["scope"])
			base_guid = item_set_guid
			xml_parts.append(item_set)
			for set_item in buff_set["set_items"]:
				xml_parts.append(update_set_item(set_item, item_set_guid))
			item_set_ids.append(item_set_guid)
			for language in texts:
				texts[language].append(generate_other_texts(language, buff_set["item_set_description"], buff_set["name"], item_set_guid, item_set_description_guid, backup_language))
			
			
			
		# get the culture set information to write into base xml
		culture_sets = []
		single_breaks = [4 + 9*i for i in range(int(len(item_set_ids)/9) + 1)] # UI requires breaks at certain indices
		double_breaks = [9 + 9*i for i in range(int(len(item_set_ids)/9) + 1)]
		for i, item_set_id in enumerate(item_set_ids):
			if i in single_breaks: culture_sets.append("""				<Item/>""")
			if i in double_breaks: culture_sets.append("""				<Item/>
				<Item/>""")
			culture_sets.append("""				<Item>
					<Set>{}</Set>
				</Item>""".format(item_set_id))
			i += 1
		for i in range((9 - len(item_set_ids) % 9) %9): # UI requires to fill up with unknowns
			culture_sets.append("""				<Item>
					<Set>65488</Set>
				</Item>""")
		culture_sets = "\n".join(culture_sets)
		
		# write asset file
		with open("export/main/asset/assets.xml", "w") as file:
			file.write("<ModOps>\n")
			with open("base.xml") as base_file:
				base_xml = str(base_file.read())
				file.write(base_xml.format(culture_sets))
			file.write("\n")			
			file.write("\n".join(xml_parts))
			file.write("\n</ModOps>") 
			
		# write asset file
		with open("export/main/asset/assets - radius.xml", "w") as file:
			file.write("<ModOps>\n")
			
			with open("base.xml") as base_file:
				base_xml = str(base_file.read())
				file.write(base_xml.format(culture_sets))
			file.write("\n")			
			file.write("\n".join(xml_parts))
			file.write("\n")
			with open("radius.xml") as radius_file:
				radius = str(radius_file.read())
				file.write(radius)
			file.write("\n</ModOps>") 
			
		# write localizations
		for language in texts:
			with open("gui/texts_{}.xml".format(language), "w") as file:
				file.write("<ModOps>\n")
				base_file_path = "texts_base_{}.xml".format(language)
				base_file_path = base_file_path if os.path.isfile(base_file_path) else "texts_base_{}.xml".format(backup_language)
				with open(base_file_path) as base_file:
					base_xml = str(base_file.read())
					file.write(base_xml)
				file.write("\n")
				file.write("\n".join(texts[language]))
				file.write("\n</ModOps>")
except Exception as err:
	print(err)
	print("Unexpected error:", sys.exc_info()[2].tb_lineno)
	input()