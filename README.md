
> ⚠️ This repository is archived
> 
> This codebase is no longer in use and is not under active development.
> If you are interested in reviving or contributing to this project, please contact us at fellesdatakatalog@digdir.no.


# jsonschematordf
A library that will map a json schema to rdf
### Eksempelbruk av bibliotek
```
from datacatalogtordf import Catalog
from jsonschematordf import jsonschematordf

catalog = Catalog()
catalog.title = {"nb": "FDK informasjonsmodellkatalog"}
catalog.identifier = Config.fdk_model_publisher_uri()

url = "https://raw.githubusercontent.com/Informasjonsforvaltning/dsop-api-spesifikasjoner/master/specs/Grue_Sparebank_937886705_Accounts-API.json"
schema = requests.get(url).text
model_metadata = data_service
model = jsonschematordf.parseJsonSchema(idenftifier, schema, model_metadata)
#parseJsonSchema(
# identifier,
# schema,
# model_metadata={
#   title,
#   keyword,
#   theme,
#   description,
#   publisher,
#   landing_page,
#   language,
#   access_rights,
#   conformsTo,
#   dct_type})

catalog.models.append(model)
rdf = catalog.to_rdf()
```
