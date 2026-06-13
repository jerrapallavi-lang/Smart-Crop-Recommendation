
import os
import csv
import pickle
import logging
from datetime import datetime
from io import StringIO
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session, make_response

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'agri-smart-secret-key')

# Ensure models directory exists
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

# Crop information database
CROP_DATA = {
    "rice": {
        "name": "Rice",
        "icon": "🌾",
        "tagline": "The world's most important staple crop",
        "description": "Rice is the primary staple food for over half the world's population. It's a cereal grain that thrives in warm, wet climates with abundant water. Rice is highly nutritious and provides essential carbohydrates, proteins, and minerals.",
        "image": "https://img.etimg.com/thumb/width-420,height-315,imgsize-98586,resizemode-75,msid-93695073/news/economy/agriculture/paddy-sowing-continues-to-lag-acreage-down-by-8-25-per-cent-till-august-18/paddy.jpg",
        "field_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQU_TzDk5gF4zwWA91_hchRr4fN7PX3VCHwqw&s",
        "temperature": "22-27°C optimal",
        "rainfall": "1000-2250mm annually",
        "ph": "6.0-7.0",
        "soil": "Loamy and Alluvial soils",
        "yield": "4200-4500",
        "season": "4-6",
        "demand": "Very High",
        "temp_range": "22-27",
        "rain_range": "1000-2250",
        "ph_range": "6.0-7.0",
        "benefits": [
            "High nutritional value with essential amino acids",
            "Supports millions of farmers globally",
            "Adaptable to various farming methods",
            "Good shelf life and storage potential",
            "Versatile use in food industry"
        ],
        "steps": [
            {"title": "Land Preparation", "description": "Prepare the field by plowing and flooding to create a paddy. Level the field for uniform water distribution."},
            {"title": "Seed Selection & Sowing", "description": "Use high-quality certified seeds. Sow in nurseries first, then transplant seedlings after 30-40 days."},
            {"title": "Transplanting", "description": "Transplant 3-4 week old seedlings at 20cm spacing with 2-3 seedlings per hill."},
            {"title": "Water Management", "description": "Maintain 5-10cm standing water during growing season. Drain 1-2 weeks before harvest."},
            {"title": "Pest & Disease Control", "description": "Monitor for brown plant hoppers, leaf folder, and blast disease. Use integrated pest management."},
            {"title": "Harvesting", "description": "Harvest when 80% of grains are golden. Use combine harvesters or manual cutting."}
        ]
    },
    "wheat": {
        "name": "Wheat",
        "icon": "🌾",
        "tagline": "Golden grain of prosperity and nourishment",
        "description": "Wheat is the second most important cereal crop worldwide, providing 20% of the world's dietary protein. It's a versatile crop that can be grown in various climates. Wheat is used for bread, pasta, flour, and animal feed.",
        "image": "https://www.world-grain.com/ext/resources/2023/07/28/wheat-ears-field_NITR---STOCK.ADOBE.COM_e.jpg?height=635&t=1740666388&width=1200",
        "field_image": "https://www.shutterstock.com/image-photo/view-wheat-field-against-beautiful-260nw-2598613149.jpg",
        "temperature": "15-20°C optimal",
        "rainfall": "600-900mm annually",
        "ph": "6.0-7.5",
        "soil": "Clay and Loamy soils",
        "yield": "3500-3800",
        "season": "6-7",
        "demand": "Very High",
        "temp_range": "15-20",
        "rain_range": "600-900",
        "ph_range": "6.0-7.5",
        "benefits": [
            "Rich source of protein and carbohydrates",
            "Can withstand moderate drought conditions",
            "Excellent crop rotation benefits",
            "Multiple end uses in food industry",
            "Good storage capacity for long periods"
        ],
        "steps": [
            {"title": "Field Preparation", "description": "Prepare seed bed with 2-3 plowings. Remove weeds and debris thoroughly."},
            {"title": "Seed Treatment", "description": "Treat seeds with fungicides to prevent diseases. Use 125-150kg seeds per hectare."},
            {"title": "Sowing", "description": "Sow in October-November depending on region. Use seed drills for uniform spacing."},
            {"title": "Nutrient Management", "description": "Apply 100-150kg nitrogen, 50-60kg phosphorus per hectare in splits."},
            {"title": "Weed & Pest Control", "description": "Apply herbicides for weed control. Monitor for Hessian fly and armyworms."},
            {"title": "Harvesting", "description": "Harvest in March-April when grain moisture is 12-14%. Store in dry conditions."}
        ]
    },
    "millet": {
        "name": "Millet",
        "icon": "🌟",
        "tagline": "Drought-resistant powerhouse of nutrition",
        "description": "Millet is a nutritious cereal crop that's highly drought-resistant and can grow in marginal lands. It's rich in minerals like iron, magnesium, and phosphorus. Millet is gluten-free and excellent for human consumption and animal feed.",
        "image": "https://www.smartfood.org/wp-content/uploads/2020/08/millet-plant-671x403-1.jpg",
        "field_image": "https://png.pngtree.com/background/20250315/original/pngtree-field-of-sorghum-or-millet-picture-image_15444875.jpg",
        "temperature": "28-32°C optimal",
        "rainfall": "400-700mm annually",
        "ph": "6.5-7.5",
        "soil": "Sandy and Red soils",
        "yield": "1700-2000",
        "season": "3-4",
        "demand": "High",
        "temp_range": "28-32",
        "rain_range": "400-700",
        "ph_range": "6.5-7.5",
        "benefits": [
            "Highly drought-resistant and climate-smart",
            "Can thrive in poor soil conditions",
            "Gluten-free and highly nutritious",
            "Short growing season (3-4 months)",
            "Low input requirements and cost-effective"
        ],
        "steps": [
            {"title": "Land Preparation", "description": "Light plowing is sufficient. Millet adapts to marginal lands well."},
            {"title": "Seed Selection", "description": "Use improved varieties. Treat seeds with fungicides. Use 4-6kg seeds per hectare."},
            {"title": "Sowing", "description": "Sow in May-June with onset of monsoon. Maintain 45cm spacing between rows."},
            {"title": "Weed Management", "description": "Apply pre-emergence herbicides or do 1-2 hand weeding."},
            {"title": "Pest Control", "description": "Monitor for shootfly and armyworms. Use neem-based sprays for organic farming."},
            {"title": "Harvesting", "description": "Harvest in August-September when panicles turn golden yellow. Thresh and store."}
        ]
    },
    "corn": {
        "name": "Corn",
        "icon": "🌽",
        "tagline": "Versatile agricultural crop with multiple uses",
        "description": "Corn (Maize) is one of the most widely cultivated crops globally. It has multiple uses - human food, animal feed, and industrial applications. Corn is rich in starch, protein, and essential amino acids.",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgZP4eC1EhJ0Vo4IUc3brUyQY29SE8SvdLpg&s",
        "field_image": "https://www.shutterstock.com/image-photo/corn-cobs-plantation-field-background-600nw-2313869449.jpg",
        "temperature": "20-25°C optimal",
        "rainfall": "800-1200mm annually",
        "ph": "6.0-7.5",
        "soil": "Loamy soils",
        "yield": "5100-5300",
        "season": "4-5",
        "demand": "Very High",
        "temp_range": "20-25",
        "rain_range": "800-1200",
        "ph_range": "6.0-7.5",
        "benefits": [
            "Highest grain yield per hectare among cereals",
            "Multiple industrial applications",
            "Used as animal feed and human food",
            "Improves soil fertility in rotation",
            "High market demand globally"
        ],
        "steps": [
            {"title": "Field Preparation", "description": "Do 2-3 plowings for good tilth. Add organic matter to improve soil."},
            {"title": "Seed Treatment", "description": "Use certified hybrid seeds. Treat with fungicides. Use 20-25kg seeds per hectare."},
            {"title": "Sowing", "description": "Sow in April-May. Maintain 60cm row spacing and 20-25cm plant spacing."},
            {"title": "Nutrient Management", "description": "Apply 100-120kg nitrogen, 60-80kg phosphorus, 40-50kg potassium per hectare."},
            {"title": "Irrigation & Weed Control", "description": "Irrigate based on rainfall. Do 1-2 weeding for weed management."},
            {"title": "Harvesting", "description": "Harvest when cobs turn reddish-brown. Dry grain to 12-14% moisture for storage."}
        ]
    },
    "sugarcane": {
        "name": "Sugarcane",
        "icon": "🌴",
        "tagline": "Sweet agricultural treasure with high returns",
        "description": "Sugarcane is a tall perennial grass that yields high sugar content. It's a major cash crop providing raw material for sugar, jaggery, ethanol, and bagasse. Sugarcane requires warm climate and abundant water.",
        "image": "https://plantix.net/en/library/assets/custom/crop-images/sugarcane.jpeg",
        "field_image": "https://media.istockphoto.com/id/93541349/photo/sugar-cane-plantation.jpg?s=612x612&w=0&k=20&c=mj-rR4mE718aFrPtXg8P7ZW7eZNROItjXlYjz5A9AvU=",
        "temperature": "25-30°C optimal",
        "rainfall": "1200-1800mm annually",
        "ph": "6.0-8.0",
        "soil": "Alluvial and Loamy soils",
        "yield": "6200-6400",
        "season": "12",
        "demand": "Very High",
        "temp_range": "25-30",
        "rain_range": "1200-1800",
        "ph_range": "6.0-8.0",
        "benefits": [
            "High economic returns and profitable crop",
            "Provides employment in sugar industry",
            "Helps control soil erosion",
            "Multiple products: sugar, jaggery, ethanol",
            "12-month crop provides year-round employment"
        ],
        "steps": [
            {"title": "Field Preparation", "description": "Deep plowing and incorporate FYM. Make raised beds for better drainage."},
            {"title": "Seed Selection", "description": "Use disease-free setts. Treat with fungicides. Use 20-25 tonnes setts per hectare."},
            {"title": "Planting", "description": "Plant in October-November at 90cm spacing. Bury setts 2 inches deep."},
            {"title": "Nutrient Management", "description": "Apply 100-150kg nitrogen, 50kg phosphorus, 40kg potassium per hectare in splits."},
            {"title": "Irrigation & Mulching", "description": "Provide 10-12 irrigations. Mulch with trash to conserve moisture."},
            {"title": "Harvesting", "description": "Harvest after 12 months in December-May when brix is 20-21. Cut close to ground."}
        ]
    },
    "alluvial": {
        "name": "Alluvial Specialty Crops",
        "icon": "👑",
        "tagline": "Premium specialty crops for premium soils",
        "description": "Alluvial soils are among the most fertile soils, ideal for growing premium specialty crops. These crops require optimal conditions and offer high market value. They include various horticultural and premium agricultural crops.",
        "image": "https://www.worldatlas.com/r/w1200/upload/47/20/0e/shutterstock-310464542.jpg",
        "field_image": "https://st4.depositphotos.com/3613639/27195/i/450/depositphotos_271959448-stock-photo-full-water-ditch-in-a.jpg",
        "temperature": "20-28°C optimal",
        "rainfall": "1000-1500mm annually",
        "ph": "6.8-7.5",
        "soil": "Alluvial soils",
        "yield": "Varies by crop",
        "season": "Varies",
        "demand": "Premium",
        "temp_range": "20-28",
        "rain_range": "1000-1500",
        "ph_range": "6.8-7.5",
        "benefits": [
            "Grown in most fertile alluvial soils",
            "High market value and premium prices",
            "Ideal for diversified farming systems",
            "Good for export markets",
            "Sustainable income generation"
        ],
        "steps": [
            {"title": "Soil Assessment", "description": "Test soil for nutrients. Alluvial soils are naturally fertile but need maintenance."},
            {"title": "Crop Selection", "description": "Choose crops suitable for premium markets based on soil and climate."},
            {"title": "Bed Preparation", "description": "Prepare raised or level beds with proper drainage systems."},
            {"title": "Premium Inputs", "description": "Use organic fertilizers and premium seeds for quality output."},
            {"title": "Precision Farming", "description": "Use drip irrigation and mulching for water conservation."},
            {"title": "Timely Harvest", "description": "Harvest at peak maturity for best quality and price in markets."}
        ]
    }
}

def load_models():
    """Load all trained models with error handling"""
    try:
        model_paths = {
            "crop_model": MODELS_DIR / "crop_model.pkl",
            "yield_model": MODELS_DIR / "yield_model.pkl",
            "soil_encoder": MODELS_DIR / "soil_encoder.pkl",
            "crop_encoder": MODELS_DIR / "crop_encoder.pkl",
        }
        
        models = {}
        for name, path in model_paths.items():
            if not path.exists():
                raise FileNotFoundError(f"Model file not found: {path}. Please run training/train_model.py first.")
            
            with open(path, "rb") as f:
                models[name] = pickle.load(f)
        
        logger.info("All models loaded successfully")
        return models
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        raise

# Load models on startup
try:
    models = load_models()
except Exception as e:
    logger.warning(f"Warning: {str(e)}")
    models = {}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    crop = None
    yield_value = None
    error = None
    history = session.get("history", [])
    insights = []
    
    if request.method == "POST":
        try:
            # Validate models are loaded
            if not models:
                error = "Models not loaded. Please run training/train_model.py first."
                return render_template("prediction.html", crop=crop, yield_value=yield_value, error=error, insights=insights, history=history)
            
            # Get form data
            soil = request.form.get("soil", "").strip()
            temperature = request.form.get("temperature", "").strip()
            rainfall = request.form.get("rainfall", "").strip()
            ph = request.form.get("ph", "").strip()
            
            # Validate inputs
            if not all([soil, temperature, rainfall, ph]):
                error = "All fields are required."
                return render_template("prediction.html", crop=crop, yield_value=yield_value, error=error, insights=insights, history=history)
            
            try:
                temp = float(temperature)
                rain = float(rainfall)
                ph_val = float(ph)
            except ValueError:
                error = "Temperature, Rainfall, and pH must be valid numbers."
                return render_template("prediction.html", crop=crop, yield_value=yield_value, error=error, insights=insights, history=history)
            
            # Validate value ranges
            if not (0 <= temp <= 50):
                error = "Temperature must be between 0-50°C."
                return render_template("prediction.html", crop=crop, yield_value=yield_value, error=error, insights=insights, history=history)
            
            if not (0 <= rain <= 500):
                error = "Rainfall must be between 0-500 mm."
                return render_template("prediction.html", crop=crop, yield_value=yield_value, error=error, insights=insights, history=history)
            
            if not (3.5 <= ph_val <= 9):
                error = "pH must be between 3.5-9."
                return render_template("prediction.html", crop=crop, yield_value=yield_value, error=error, insights=insights, history=history)
            
            # Encode soil type
            try:
                soil_encoded = models["soil_encoder"].transform([soil])[0]
            except ValueError:
                error = f"Invalid soil type: {soil}. Please select from available options."
                return render_template("prediction.html", crop=crop, yield_value=yield_value, error=error, insights=insights, history=history)
            
            # Prepare data for prediction
            data = [[soil_encoded, temp, rain, ph_val]]
            
            # Make predictions
            crop_pred = models["crop_model"].predict(data)[0]
            crop = models["crop_encoder"].inverse_transform([crop_pred])[0]
            yield_value = max(0, int(models["yield_model"].predict(data)[0]))

            crop_info = CROP_DATA.get(crop.lower(), {})
            if crop_info:
                try:
                    temp_min, temp_max = map(float, crop_info["temp_range"].split("-"))
                    rain_min, rain_max = map(float, crop_info["rain_range"].split("-"))
                    ph_min, ph_max = map(float, crop_info["ph_range"].split("-"))
                except Exception:
                    temp_min = temp_max = rain_min = rain_max = ph_min = ph_max = None

                if temp_min is not None and temp_max is not None:
                    if temp_min <= temp <= temp_max:
                        insights.append(f"Temperature {temp}°C is within the ideal range for {crop}.")
                    else:
                        insights.append(f"Temperature {temp}°C is outside the ideal range ({temp_min}-{temp_max}°C).")

                if rain_min is not None and rain_max is not None:
                    if rain_min <= rain <= rain_max:
                        insights.append(f"Rainfall {rain}mm matches the recommended range for {crop}.")
                    else:
                        insights.append(f"Rainfall {rain}mm is outside the recommended {rain_min}-{rain_max}mm range.")

                if ph_min is not None and ph_max is not None:
                    if ph_min <= ph_val <= ph_max:
                        insights.append(f"Soil pH {ph_val} is suitable for {crop}.")
                    else:
                        insights.append(f"Soil pH {ph_val} is outside the ideal range ({ph_min}-{ph_max}).")

                if soil.lower() in crop_info["soil"].lower():
                    insights.append(f"Selected soil type ({soil}) is a good match for {crop}.")
                else:
                    insights.append(f"Selected soil type ({soil}) may be less ideal for {crop}, please confirm soil compatibility.")
            else:
                insights.append("Recommendation generated from the crop model output.")

            prediction_entry = {
                "crop": crop,
                "yield_value": yield_value,
                "soil": soil,
                "temperature": temp,
                "rainfall": rain,
                "ph": ph_val,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            history.insert(0, prediction_entry)
            session["history"] = history[:5]

            logger.info(f"Prediction successful - Soil: {soil}, Temp: {temp}, Rainfall: {rain}, pH: {ph_val}")
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            error = f"An error occurred during prediction: {str(e)}"
    
    return render_template("prediction.html", crop=crop, yield_value=yield_value, error=error, insights=insights, history=history)

@app.route("/prediction/download", methods=["GET"])
def download_prediction():
    """Download the latest prediction as a CSV file."""
    history = session.get("history", [])
    if not history:
        return jsonify({"error": "No prediction history available."}), 404

    latest = history[0]
    output = StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(["Field", "Value"])
    csv_writer.writerow(["Timestamp", latest["timestamp"]])
    csv_writer.writerow(["Recommended Crop", latest["crop"]])
    csv_writer.writerow(["Expected Yield (kg)", latest["yield_value"]])
    csv_writer.writerow(["Soil Type", latest["soil"]])
    csv_writer.writerow(["Temperature (°C)", latest["temperature"]])
    csv_writer.writerow(["Rainfall (mm)", latest["rainfall"]])
    csv_writer.writerow(["Soil pH", latest["ph"]])

    response = make_response(output.getvalue())
    filename = f"prediction_{latest['timestamp'].replace(':', '-').replace(' ', '_')}.csv"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"
    return response


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "models_loaded": bool(models)
    })

@app.route("/crops", methods=["GET"])
def crops():
    """Display all crops catalog"""
    return render_template("crops.html")

@app.route("/crops/<crop_name>", methods=["GET"])
def crop_detail(crop_name):
    """Display detailed information about a specific crop"""
    crop_name_lower = crop_name.lower()
    
    if crop_name_lower not in CROP_DATA:
        return render_template("index.html", error=f"Crop '{crop_name}' not found"), 404
    
    crop = CROP_DATA[crop_name_lower]
    
    return render_template("crop_detail.html",
        crop_name=crop["name"],
        crop_icon=crop["icon"],
        crop_tagline=crop["tagline"],
        crop_description=crop["description"],
        crop_image=crop["image"],
        crop_field_image=crop["field_image"],
        crop_temperature=crop["temperature"],
        crop_rainfall=crop["rainfall"],
        crop_ph=crop["ph"],
        crop_soil=crop["soil"],
        crop_benefits=crop["benefits"],
        crop_steps=crop["steps"],
        crop_yield=crop["yield"],
        crop_season=crop["season"],
        crop_demand=crop["demand"],
        crop_temp_range=crop["temp_range"],
        crop_rain_range=crop["rain_range"],
        crop_ph_range=crop["ph_range"],
        enumerate=enumerate
    )

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template("index.html", error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return render_template("index.html", error="An internal server error occurred"), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
