import os, requests, shutil, time
from urllib.parse import urlparse

API_KEY = "1AhbgX6f-AVV6SPFX7-1q9v0HJ55kghAcuz3XE_4cms"
BASE_URL = "https://trefle.io/api/v1/species"


#DOWNLOADING IMAGES!!!!

ROOT = "/Users/graceyan/Downloads/St.Gallen /Computerscience"
IMAGES_PER_SPECIES = 5

plant_types = {
    "Flower": [
    "bellis-perennis", "viola-tricolor", "chrysanthemum-morifolium", "helianthus-annuus",
    "taraxacum-officinale", "convolvulus-arvensis", "achillea-millefolium", "oxalis-acetosella",
    "anemone-nemorosa", "lychnis-flos-cuculi", "pulsatilla-vulgaris", "myosotis-arvensis",
    "digitalis-purpurea", "primula-vulgaris", "campanula-rotundifolia", "dianthus-deltoides",
    "potentilla-erecta", "trifolium-pratense", "centaurea-nigra", "galium-verum",
    "solidago-virgaurea", "leucanthemum-vulgare", "scabiosa-columbaria", "ranunculus-acris",
    "lotus-corniculatus", "gentiana-verna", "saxifraga-granulata", "linaria-vulgaris",
    "melilotus-officinalis", "lamium-purpureum", "lamium-album", "geranium-robertianum",
    "claytonia-sibirica", "geranium-pratense", "tropaeolum-majus", "malva-sylvestris",
    "cardamine-pratensis", "caltha-palustris", "tanacetum-vulgare", "veronica-chamaedrys",
    "veronica-officinalis", "anthyllis-vulneraria", "euphrasia-officinalis", "silene-dioica",
    "armeria-maritime", "lysimachia-vulgaris", "sanguisorba-minor", "pulmonaria-officinalis",
    "ajuga-reptans", "stachys-officinalis",
    "rosa-rubiginosa", "rosa-canina", "rosa-gallica", "tulipa-gesneriana",
    "narcissus-pseudonarcissus", "crocus-sativus", "crocus-vernus", "iris-sibirica",
    "iris-pseudacorus", "lilium-candidum", "lilium-lancifolium", "papaver-rhoeas",
    "papaver-somniferum", "calendula-officinalis", "hyacinthus-orientalis", "muscari-armeniacum",
    "fritillaria-meleagris", "helleborus-niger", "erythronium-dens-canis", "corydalis-solida",
    "cyclamen-hederifolium", "leucojum-aestivum", "anthericum-liliago", "aconitum-napellus",
    "alchemilla-vulgaris", "amaryllis-belladonna", "aquilegia-vulgaris", "argemone-mexicana",
    "asclepias-syriaca", "aster-alpinus", "aster-amellus", "astilbe-arendsii",
    "aubrieta-deltoidea", "campanula-carpatica", "campanula-latifolia", "centranthus-ruber",
    "chelidonium-majus", "erysimum-cheiri", "colchicum-autumnale", "comarum-palustre",
    "convallaria-majalis", "coreopsis-tinctoria", "dahlia-pinnata", "delphinium-elatum",
    "dianthus-caryophyllus", "dictamnus-albus", "hesperis-matrionalis", "erodium-cicutarium",
    "eryngium-maritimum", "eupatorium-perfoliatum", "eupatorium-purpureum", "eustoma-grandiflorum",
    "fuchsia-magellanica", "gaillardia-pulchella", "galanthus-nivalis", "gazania-rigens",
    "gerbera-jamesonii", "leontopodium-alpinum", "lobelia-erinus", "lupinus-polyphyllus",
    "matthiola-incana", "meconopsis-betonicifolia", "mimulus-guttatus", "monarda-didyma",
    "papaver-orientale", "pelargonium-peltatum", "penstemon-husker-red", "perovskia-atriplicifolia",
    "petunia-hybrida", "phlox-paniculata", "physalis-alkekengi", "polemonium-caeruleum",
    "polianthes-tuberosa", "polygonatum-odoratum", "ranunculus-bulbocodium", "rhododendron-maximum",
    "rudbeckia-hirta", "salvia-nemorosa", "salvia-sclarea", "scilla-siberica",
    "sedum-spectabile", "silene-uniflora", "sisyrinchium-striatum", "solidago-canadensis",
    "spiraea-japonica", "strelitzia-reginae", "symphyotrichum-novae-angliae", "tellima-grandiflora",
    "thalictrum-aquilegiifolium", "trollius-europaeus", "tiarella-cordifolia", "valeriana-officinalis",
    "verbascum-thapsus", "verbena-bonariensis", "veronica-spicata", "vinca-minor",
    "viola-pubescens", "zantedeschia-aethiopica", "zinnia-elegans", "tussilago-farfara"
    ],
    
    "Tree": [
    "quercus-robur", "quercus-petraea", "fagus-sylvatica", "tilia-cordata", "betula-pendula",
    "betula-pubescens", "alnus-glutinosa", "populus-nigra", "populus-alba", "salix-alba",
    "salix-caprea", "fraxinus-excelsior", "ulmus-glabra", "carpinus-betulus", "corylus-avellana",
    "acer-campestre", "acer-platanoides", "acer-pseudoplatanus", "sorbus-aucuparia",
    "sorbus-torminalis", "juglans-regia", "castanea-sativa", "platanus-orientalis",
    "tilia-platyphyllos", "prunus-avium", "prunus-padus", "prunus-domestica", "populus-tremula",
    "quercus-suber", "cercis-siliquastrum", "ginkgo-biloba", "larix-decidua", "picea-abies",
    "pinus-sylvestris", "pinus-nigra", "abies-alba", "juniperus-communis", "sequoiadendron-giganteum",
    "cryptomeria-japonica", "tsuga-canadensis", "taxus-baccata", "cedrus-libani", "quercus-ilex",
    "eucalyptus-globulus", "catalpa-bignonioides", "robinia-pseudoacacia", "broussonetia-papyrifera",
    "ailanthus-altissima", "gleditsia-triacanthos",
    "acer-saccharum", "acer-rubrum", "acer-palmatum", "acer-griseum", "acer-macrophyllum", "acer-buergerianum", "acer-negundo",
    "aesculus-hippocastanum", "aesculus-californica", "aesculus-flava", "aesculus-glabra",
    "alnus-incana", "alnus-rubra", "alnus-occidentalis",
    "amelanchier-verticalis", "amelanchier-laevis",
    "betula-nigra", "betula-lenta", "betula-occidentalis",
    "carya-ovata", "carya-cordiformis", "carya-glabra",
    "castanea-mollissima",
    "catalpa-speciosa",
    "cedrus-atlantica", "cedrus-deodara",
    "celtis-australis",
    "cercidiphyllum-japonicum",
    "chionanthus-virginicus",
    "cornus-kousa", "cornus-nuttallii",
    "crataegus-monogyna", "crataegus-crus-galli",
    "cupressus-sempervirens", "cupressus-leylandii", "cupressus-hesperoxylon",
    "davidia-involucrata",
    "dracaena-draco",
    "eucalyptus-camaldulensis", "eucalyptus-grandis",
    "ficus-benghalensis", "ficus-microcarpa",
    "jacaranda-mimosifolia",
    "laburnum-anagyroides",
    "liriodendron-tulipifera",
    "magnolia-grandiflora", "magnolia-liliiflora", "magnolia-soulangeana",
    "mangifera-indica",
    "persea-americana",
    "cocos-nucifera",
    "elaeis-guineensis",
    "phoenix-dactylifera",
    "malus-domestica", "malus-sylvestris", "malus-baccata",
    "pyrus-communis", "pyrus-pashia",
    "syzygium-jambos",
    "eugenia-uniflora",
    "bombax-ceiba",
    "bauhinia-variegata",
    "cecropia-peltata",
    "dalbergia-nigra",
    "paulownia-tomentosa",
    "taxodium-distichum",
    "metasequoia-glyptostroboides",
    "morus-alba", "morus-nigra",
    "prunus-serotina", "prunus-cerasifera", "prunus-persica", "prunus-armeniaca", "prunus-serrulata", "prunus-yedoensis",
    "sequoia-sempervirens",
    "quercus-alba", "quercus-coccinea", "quercus-phellos", "quercus-macrocarpa", "quercus-velutina", "quercus-rubra", "quercus-palustris", "quercus-gambelii",
    "fagus-grandifolia",
    "tilia-americana",
    "populus-trichocarpa", "populus-balsamifera",
    "salix-babylonica", "salix-viminalis", "salix-purpurea",
    "fraxinus-americana", "fraxinus-pennsylvanica",
    "ulmus-minor", "ulmus-pumila",
    "carpinus-caroliniana",
    "corylus-colurna",
    "juglans-nigra",
    "platanus-occidentalis",
    "carya-illinoensis"
    ],
    
    "Grass": [
    "dactylis-glomerata", "festuca-rubra", "phleum-pratense", "lolium-perenne", "alopecurus-pratensis",
    "poa-pratensis", "cynodon-dactylon", "agrostis-capillaris", "bromus-inermis", "elymus-repens",
    "andropogon-gerardii", "arundinaria-gigantea", "chrysopogon-gryllus", "danthonia-spicata", 
    "deschampsia-flexuosa", "digitaria-sanguinalis", "eragrostis-curvula", "festuca-ovina", 
    "glyceria-maxima", "hordeum-jubatum", "koeleria-macrantha", "leymus-arenarius", 
    "melica-nutans", "miscanthus-sinensis", "molinia-caerulea", "nassella-tenuissima", 
    "panicum-virgatum", "pennisetum-alopecuroides", "phalaris-arundinacea", "piptochaetium-avenaceum",
    "schizachyrium-scoparium", "sorghastrum-nutans", "sorghum-halepense", "sporobolus-heterolepis",
    "stipa-tenacissima", "tridens-flavus", "trisetum-flavescens", "vulpia-myuros", "zea-mays",
    "zoysia-japonica", "xerochloa-imberbis", "urochloa-decipiens", "themeda-triandra",
    "setaria-italica", "paspalum-notatum", "oryzopsis-hymenoides", "oryza-sativa", "elymus-canadensis",
    "achnatherum-hymenoides", "aira-pratensis", "aristida-purpurea", "avena-sativa", "avena-fatua",
    "avena-sterilis", "brachypodium-distachyon", "brachypodium-sylvaticum", "bouteloua-gracilis",
    "bouteloua-curtipendula", "briza-maxima", "briza-minor", "cenchrus-ciliaris", "cenchrus-longispinus",
    "cenchrus-purpureus", "chloris-gayana", "chloris-barbata", "crypsis-schoenoides",
    "dichelachne-crinita", "echinochloa-crus-galli", "echinochloa-colona", "festuca-arundinacea",
    "glyceria-fluitans", "glyceria-declinata", "holcus-lanatus", "holcus-mollis", "hordeum-vulgare",
    "hordeum-murinum", "hordeum-bulbosum", "hordeum-marinum", "imperata-cylindrica",
    "ischaemum-rubrum", "koeleria-cristata", "lolium-multiflorum", "lolium-temulentum",
    "lolium-rigidum", "melica-ciliata", "muhlenbergia-capillaris", "muhlenbergia-rigens",
    "nassella-pulchra", "nassella-leucotricha", "oplismenus-hirtellus", "phalaris-aquatica",
    "phalaris-minor", "phragmites-australis", "poa-trivialis", "poa-annua", "polypogon-monspeliensis",
    "schedonorus-arundinaceus", "setaria-viridis", "setaria-verticillata", "setaria-pumila",
    "spartina-alterniflora", "spartina-anglica", "spartina-pectinata", "sporobolus-indicus",
    "stenotaphrum-secundatum", "themeda-quadrivalvis", "themeda-australis", "tragus-racemosus",
    "tragus-australianus", "urochloa-ruziziensis", "vetiveria-zizanioides", "zoysia-matrella",
    "zoysia-pacifica", "zoysia-tenuifolia", "poa-labillardierei", "poa-bulbosa", "eragrostis-trichodes",
    "cynosurus-cristatus", "bromus-mollis", "bromus-tectorum", "bromus-commutatus", "bromus-hordeaceus",
    "bromus-sterilis", "dasypyrum-villosum", "leptochloa-fusca", "setaria-parviflora",
    "hemarthria-altissima", "aristida-striata", "aristida-longiseta", "andropogon-bladhii",
    "andropogon-gayanus", "miscanthus-giganteus", "deschampsia-caespitosa", "deschampsia-cespitosa",
    "spartina-cynosuroides", "spartina-patens", "echinochloa-oryzoides", "hyparrhenia-rufa",
    "cymbopogon-nardus", "cymbopogon-citratus", "phragmites-mauritianus", "elymus-sibiricus",
    "elymus-trachycaulus", "arundo-donax", "glyceria-borealis", "ctenium-arundinaceum",
    "brachiaria-humidicola", "phyllostachys-bambusoides"
    ],
    
    "Edible": [
    "malus-domestica", "citrus-limon", "vitis-vinifera", "musa-paradisiaca", "fragaria-vesca",
    "prunus-persica", "citrullus-lanatus", "pyrus-communis", "rubus-idaeus", "ficus-carica",
    "vaccinium-corymbosum", "ribes-nigrum", "ribes-rubrum", "sambucus-nigra", "cydonia-oblonga",
    "actinidia-deliciosa", "passiflora-edulis", "psidium-guajava", "annona-muricata", "durio-zibethinus",
    "diospyros-kaki", "syzygium-samarangense", "carica-papaya", "mangifera-indica", "litchi-chinensis",
    "tamarindus-indica", "monstera-deliciosa", "myrciaria-dubia", "morinda-citrifolia", "eugenia-uniflora",
    "artocarpus-altilis", "spondias-mombin", "melicoccus-bijugatus", "carya-illinoensis", "juglans-regia",
    "canarium-ovatum", "cornus-mas", "elaeagnus-umbellata", "hippophae-rhamnoides", "amelanchier-alnifolia",
    "arbutus-unedo", "cercis-canadensis", "hylocereus-undatus", "olea-europaea", "zanthoxylum-piperitum",
    "garcinia-mangostana", "citrus-paradisi", "citrus-reticulata", "citrus-sinensis", "citrus-maxima",
    "lactuca-sativa", "daucus-carota", "solanum-tuberosum", "allium-cepa", "spinacia-oleracea",
    "brassica-oleracea", "beta-vulgaris", "phaseolus-vulgaris", "cucumis-sativus", "solanum-lycopersicum",
    "allium-sativum", "apium-graveolens", "asparagus-officinalis", "brassica-rapa", "capsicum-annuum",
    "cichorium-intybus", "coriandrum-sativum", "cucurbita-pepo", "foeniculum-vulgare", "levisticum-officinale",
    "pastinaca-sativa", "petroselinum-crispum", "pisum-sativum", "rheum-rhabarbarum", "rucola-sativa",
    "satureja-hortensis", "scorzonera-hispanica", "sinapis-alba", "tropaeolum-majus", "valerianella-locusta",
    "vigna-unguiculata", "zea-mays", "abobra-tenuifolia", "brassica-juncea", "brassica-napus",
    "carum-carvi", "cucurbita-maxima", "cucurbita-moschata", "lupinus-albus", "lycopersicon-pimpinellifolium",
    "mentha-spicata", "ocimum-basilicum", "origanum-majorana", "portulaca-oleracea", "rosmarinus-officinalis",
    "satureja-montana", "solanum-melongena", "thymus-vulgaris", "trigonella-foenum-graecum", "urtica-dioica",
    "glycine-max", "arachis-hypogaea", "lens-culinaris", "cicer-arietinum", "triticum-aestivum",
    "triticum-durum", "triticum-spelta", "avena-sativa", "secale-cereale", "eleusine-coracana",
    "panicum-miliaceum", "eragrostis-tef", "digitaria-exilis", "sesamum-indicum", "helianthus-annuus",
    "theobroma-cacao", "zingiber-officinale", "curcuma-longa", "piper-nigrum", "piper-longum",
    "syzygium-aromaticum", "cinnamomum-verum", "elettaria-cardamomum", "myristica-fragrans", "alpinia-galanga",
    "allium-porrum", "allium-fistulosum", "armoracia-rusticana", "wasabia-japonica", "vaccinium-macrocarpon",
    "vaccinium-oxyccoccos", "vaccinium-angustifolium", "oenothera-biennis", "chenopodium-quinoa",
    "borago-officinalis", "berberis-vulgaris", "capparis-spinosa", "arctium-lappa", "cynara-scolymus",
    "vicia-faba", "phaseolus-coccineus", "phaseolus-lunatus", "phaseolus-angularis", "vigna-radiata",
    "vigna-angularis", "cajanus-cajan", "canavalia-ensiformis", "dolichos-lablab", "glycyrrhiza-glabra",
    "apios-americana", "ipomoea-batatas", "manihot-esculenta", "colocasia-esculenta", "xanthosoma-sagittifolium",
    "dioscorea-esculenta", "dioscorea-alata", "dioscorea-bulbifera", "arracacia-xanthorrhiza",
    "chenopodium-album", "rumex-acetosella", "rumex-acetosa", "brassica-carinata", "brassica-nigra",
    "nasturtium-officinale", "prunus-cerasus", "prunus-salicina", "prunus-dulcis", "prunus-serotina",
    "prunus-mahaleb", "prunus-spinosa", "actinidia-arguta", "fragaria-chiloensis", "fragaria-ananassa",
    "sambucus-canadensis", "sambucus-racemosa", "pimpinella-anisum", "illicium-verum", "malva-sylvestris",
    "hibiscus-sabdariffa", "calendula-officinalis", "tagetes-erecta", "pyrus-pashia", "malus-sylvestris",
    "celtis-australis", "prunus-domestica", "morus-alba", "morus-nigra", "lycium-barbarum",
    "schisandra-chinensis", "aegle-marmelos", "cercis-siliquastrum", "ceratonia-siliqua", "punica-granatum",
    "citrus-aurantifolia", "citrus-aurantium", "aegopodium-podagraria", "taraxacum-officinale",
    "centaurea-cyanus"
    ],
    
    "Succulent": [
    "opuntia-ficus-indica", "aloe-vera", "crassula-ovata", "echeveria-elegans", "agave-americana",
    "sedum-morganianum", "kalanchoe-blossfeldiana", "euphorbia-trigona", "haworthia-fasciata", "graptopetalum-paraguayense",
    "aeonium-arboreum", "adromischus-cristatus", "agave-victoriae-reginae", "alworthia-pentagona",
    "anacampseros-rufescens", "astroloba-sp", "cotyledon-orbiculata", "delosperma-cooperi",
    "dudleya-brittonii", "echeveria-lilacina", "euphorbia-obesa", "gasteria-sp", "graptopetalum-bellum",
    "gynura-aurantiaca", "haworthia-cymbiformis", "kalanchoe-daigremontiana", "lampranthus-aurantiacus",
    "lithops-sp", "mammillaria-spinosissima", "orbea-variegata", "peperomia-dolabriformis", "portulacaria-afra",
    "pseudolithos-migiurtinus", "rebutia-krainziana", "rhipsalis-baccifera", "schlumbergera-truncata",
    "sedeveria-letizia", "senecio-rowleyanus", "senecio-radicans", "stapelia-gigantea",
    "succulent-sp", "titanopsis-calcarea", "tradescantia-pallida", "xerosicyos-danguyi",
    "yucca-gloriosa", "zamioculcas-zamiifolia",
    "aloe-arborescens", "aloe-ferox", "aloe-saponaria", "aloe-plicatilis",
    "haworthia-attenuata", "haworthia-reinwardtii", "haworthia-pumila", "haworthiopsis-limifolia",
    "echeveria-imbricata", "echeveria-agavoides", "echeveria-runyonii", "echeveria-chihuahuaensis",
    "graptopetalum-fernandezianum", "graptopetalum-amethystinum",
    "pachyveria-glauca", "pachyveria-lushii",
    "pachyphytum-oviferum", "pachyphytum-compactum",
    "sempervivum-tectorum", "sempervivum-arachnoideum",
    "sedum-spurium", "sedum-pachyphyllum", "sedum-album", "sedum-telephium",
    "sedum-reflexum", "sedum-adolphi", "sedum-rubrotinctum", "sedum-ternatum",
    "aeonium-urbicum", "aeonium-kiwi", "aeonium-armstrongii", "aeonium-gomerense",
    "adromischus-alstonii", "adromischus-maculatus", "adromischus-millephyllus", "adromischus-pectinatus",
    "crassula-perforata", "crassula-tetragona", "crassula-multicava", "crassula-rupestris",
    "kalanchoe-thyrsiflora", "kalanchoe-pinnata",
    "lampranthus-spectabilis", "lampranthus-glaucoides",
    "anacampseros-alstonii", "anacampseros-filimontana", "anacampseros-turbinata",
    "astroloba-herrei", "astroloba-congesta",
    "delosperma-echinatum", "delosperma-lehmannii", "delosperma-sikkimensis",
    "dudleya-cotyledon", "dudleya-edulis",
    "pachypodium-lamerei", "pachypodium-geayi",
    "euphorbia-pseudocactus", "euphorbia-artericans", "euphorbia-mammillaris",
    "euphorbia-lactea", "euphorbia-ingens", "euphorbia-ambovombensis",
    "agave-parryi", "agave-attenuata", "agave-deserti", "agave-ferox", "agave-filifera",
    "yucca-filamentosa", "yucca-elephantipes", "yucca-rostrata",
    "cylindropuntia-prolifera", "cylindropuntia-bigelovii",
    "opuntia-microdasys", "opuntia-ingens",
    "mammillaria-elata", "mammillaria-hahniana", "mammillaria-elongata",
    "echinocactus-grusonii", "ferocactus-horridus",
    "gymnocalycium-mihanovichii", "parodia-magnifica", "astrophytum-asterias",
    "copiapoa-cylindrica", "leuchtenbergia-principis",
    "peniocereus-pentlandianus", "carnegiea-gigantea",
    "pachycereus-pringlei", "cephalocereus-columnaris",
    "stenocactus-speciosus", "ariocarpus-fissuratus",
    "echinopsis-pachanoi", "echinopsis-peruviana",
    "rhipsalis-pilocarpa", "stapelia-grandiflora",
    "huernia-zebrina", "orbea-grandiflora", "ceropegia-woodii",
    "senecio-confusus", "othonna-capensis", "peperomia-rotundifolia"
]
}

def get_image_urls(slug):
    url = f"{BASE_URL}/{slug}?token={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"[ERROR] Failed: {slug} → {r.status_code}")
            return []
        data = r.json().get("data", {})
        urls = []
        if data.get("image_url"):
            urls.append(data["image_url"])
        for img in data.get("images", []):
            if isinstance(img, dict) and img.get("image_url"):
                urls.append(img["image_url"])
        urls = list(dict.fromkeys(urls))
        return urls[:IMAGES_PER_SPECIES]
    except Exception as e:
        print(f"[ERROR] Exception for {slug}: {e}")
        return []

def download(url, dest):
    try:
        r = requests.get(url, stream=True, timeout=5)
        r.raise_for_status()
        with open(dest, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        print(f"  ✔ Saved: {os.path.basename(dest)}")
    except Exception as e:
        print(f"  ✘ Failed: {url} — {e}")

def main():
    for category, slugs in plant_types.items():
        folder = os.path.join(ROOT, category)
        os.makedirs(folder, exist_ok=True)

        for slug in slugs:
            print(f"\n➡️  {category} > {slug}")
            urls = get_image_urls(slug)
            if not urls:
                print("  ⚠ No images found")
                continue

            for i, url in enumerate(urls):
                raw_name = os.path.basename(urlparse(url).path)
                filename = f"{slug}_{i}_{raw_name}" if raw_name else f"{slug}_{i}.jpg"
                if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    filename += ".jpg"
                path = os.path.join(folder, filename)
                download(url, path)
                time.sleep(0.3)

    print("\n✅ All images downloaded into type folders.")

if __name__ == "__main__":
    main()
    
    




