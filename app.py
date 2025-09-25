from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# GST Categories
l1 = ["Wheat", "rice", "atta", "maida", "besan", "milk", "Curd", "Lassi", "Buttermilk",
      "Chena", "Paneer", "vegetables", "fruits", "Fresh eggs", "Natural honey", "Jaggery",
      "Puffed rice", "Papad", "Bread", "Roti", "Chapati", "Paratha", "Parotta", "Khakhra",
      "Pizza Bread", "Life-Saving Drugs", "Onasemnogene abeparvovec", "Daratumumab", "Risdiplam",
      "Human blood", "contraceptives", "Printed books", "newspapers", "journals", "periodicals",
      "Maps", "atlases", "globes", "Children's drawing", "painting", "coloring books",
      "Exercise books", "notebooks", "graph books", "Pencils", "sharpeners", "eraser",
      "crayons", "pastels", "chalk", "Seeds for sowing", "Organic manure", "Raw silk",
      "silk waste", "raw wool", "Khadi fabric", "yarn", "Raw jute fibers", "Firewood",
      "charcoal", "Hand-operated agricultural implements", "The Indian National Flag",
      "Clay lamps", "idols", "Bindi", "Sindoor", "Kajal", "Alta", "bangles", "Salt", "Potable water"]

l2 = ["Branded and packaged paneer", "Condensed milk", "Butter", "ghee", "dairy fats and spreads",
      "Packaged curd", "Packaged lassi", "Packaged namkeens", "bhujia", "mixtures", "Biscuits",
      "pastries", "cakes", "Pasta", "noodles", "cornflakes", "Jams", "jellies", "sauces", "pickles",
      "soups", "Ice cream", "edible ice", "Chocolates", "cocoa products", "Sugar confectionery",
      "sugar-boiled confectionery", "almonds", "walnuts", "pistachios", "cashews", "hazelnuts",
      "dates", "figs", "raisins", "dried mangoes", "Packaged tender coconut water",
      "Packaged drinking water", "Fruit juices", "vegetable juices", "Tea", "coffee",
      "Plant-based milk drinks (including soya milk)", "Sugar", "edible oils", "spices",
      "Processed meat", "fish products", "Malt", "starches", "Hair oil", "shampoo", "soaps",
      "Toothpaste", "tooth powder", "Talcum powder", "face powder", "Shaving cream",
      "aftershave lotion", "Utensils (iron, steel, copper, aluminum)", "Sewing machines",
      "needles", "Candles", "Bicycles", "Feeding bottles and nipples", "Napkins",
      "napkin liners for babies", "clinical diapers", "Ready-made apparel with a sale value up to ₹2,500 per piece.",
      "Footwear with a sale value not exceeding ₹2,500 per pair.", "Man-made fibres", "yarns",
      "Tractors", "horticultural", "forestry machinery for soil preparation", "cultivator",
      "harvestor", "Drip irrigation systems", "sprinklers", "Hand pumps", "Specified bio-pesticides",
      "micronutrients", "Tractor tires", "tubes", "Most drugs and medicines including those from Ayurveda",
      "Unani", "Homeopathy systems", "Diagnostic kits", "reagents", "Medical grade oxygen",
      "Thermometers", "glucometers", "test strips", "Corrective spectacles", "Pens",
      "Packaging containers and boxes", "drones", "Handicrafts", "idols", "paintings",
      "carved wood products", "Leather goods", "Leather handbags", "Leather purses",
      "Leather gloves", "Sand-lime bricks", "stone inlay work", "Bidi wrapper leaves"]

l3 = ["Televisions (up to 32 inches)", "Refrigerators", "Washing machines", "Vacuum cleaners",
      "Dishwashers", "Other home appliances", "Laptops", "Desktop computers", "Monitors", "Printers",
      "Scanners", "Keyboards", "Mice", "Other computer accessories", "Mobile phones", "Smartphones",
      "Landline telephones", "Wires", "Cables", "Electrical transformers", "CCTV cameras", "LEDs",
      "Shampoos", "Hair dyes", "Deodorants", "Perfumes", "Aftershave lotions", "Furniture",
      "Mattresses", "Lighting fixtures", "Sanitaryware (sinks, washbasins)", "Water purifiers",
      "Cutlery", "Kitchen stoves", "Clocks", "Watches", "Luggage (suitcases, briefcases)",
      "Leather goods", "Most industrial machinery", "capital goods", "machine tools",
      "Steel products", "Aluminum products", "Cement", "Other construction materials",
      "A wide range of industrial and chemical products", "Two-wheelers(non-luxury)", "four-wheelers (non-luxury)",
      "Automobile spare parts and accessories", "Branded and packaged snacks", "Instant food mixes",
      "Ready-to-eat meals", "Packaged fruit juices (with added sugar)", "Non-aerated drinks",
      "Condensed milk", "Chocolates (containing cocoa)", "Refined sugar", "Eyewear frames",
      "sunglasses", "All types of musical instruments", "Bricks", "Roofing tiles"]

l4 = ["Motor cars and other motor vehicles with a cylinder capacity exceeding 2,000 cc",
      "Sports Utility Vehicles (SUVs) with an engine capacity of more than 1,500 cc, a length exceeding 4,000 mm, and a ground clearance of 170 mm and above",
      "All imported cars, including Completely Built Units (CBUs) and Completely Knocked Down (CKD) units",
      "Motorcycles and motorbikes with an engine capacity exceeding 350 cc", "Cigarettes", "cigars",
      "Chewing tobacco", "gutkha", "khaini", "Hookah", "other smoking tobacco preparations",
      "Pan Masala containing tobacco.", "Aerated waters containing added sugar", "other sweetening",
      "flavoring matter (soft drinks and sodas)", "colddrinks", "Energy Drinks", "Caffeinated beverages",
      "Aircraft for personal use (private jets).", "Yachts", "other vessels for pleasure or sports.",
      "Lottery", "betting", "gambling services", "beers", "Spirits / Liquor", "wines"]

# Smart GST detection
def detect_gst(item):
    item = item.lower().strip()
    for it in l1:
        if item in it.lower():
            return 0
    for it in l2:
        if item in it.lower():
            return 5
    for it in l3:
        if item in it.lower():
            return 18
    for it in l4:
        if item in it.lower():
            return 40
    return None
@app.route('/')
def index():
    return render_template('Calculator.html')
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    item = data.get("item", "")
    cost = float(data.get("cost", 0))

    gst_rate = detect_gst(item)

    if gst_rate is None:
        return jsonify({"error": "Item not found in GST categories"}), 400

    gst_amount = (cost * gst_rate) / 100
    include_gst = cost + gst_amount
    exclude_gst = cost  # assuming entered cost = base price

    return jsonify({
        "item": item,
        "original_cost": cost,
        "gst_rate": gst_rate,
        "gst_amount": gst_amount,
        "include_gst": include_gst,
        "exclude_gst": exclude_gst
    })

if __name__ == '__main__':
    app.run(debug=True)

