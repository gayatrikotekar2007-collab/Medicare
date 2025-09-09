from database import get_db

# Home remedies database
remedies_data = {
    "headache": {
        "name": "Headache",
        "remedies": [
            {
                "title": "Hydration",
                "description": "Dehydration is a common cause of headaches. Drink plenty of water throughout the day.",
                "steps": ["Drink a full glass of water", "Continue sipping water throughout the day"],
                "precautions": "If headache persists for more than 24 hours, consult a doctor."
            },
            {
                "title": "Cold Compress",
                "description": "Applying a cold compress can help reduce inflammation that causes headaches.",
                "steps": ["Wrap ice packs or frozen vegetables in a towel", "Apply to forehead or neck for 15 minutes"],
                "precautions": "Never apply ice directly to skin."
            },
            {
                "title": "Peppermint Oil",
                "description": "Peppermint oil has menthol which can help relax muscles and ease pain.",
                "steps": ["Dilute a few drops of peppermint oil with a carrier oil", "Gently massage onto temples"],
                "precautions": "Do not use on broken skin or near eyes."
            }
        ]
    },
    "cough": {
        "name": "Cough",
        "remedies": [
            {
                "title": "Honey and Lemon",
                "description": "Honey coats the throat while lemon provides vitamin C.",
                "steps": ["Mix 2 teaspoons of honey with 1 teaspoon of lemon juice", "Take this mixture 2-3 times a day"],
                "precautions": "Do not give honey to children under 1 year old."
            },
            {
                "title": "Steam Inhalation",
                "description": "Steam helps loosen mucus and soothe irritated airways.",
                "steps": ["Boil water and pour into a bowl", "Lean over the bowl with a towel over your head", "Breathe deeply for 5-10 minutes"],
                "precautions": "Be careful to avoid burns from hot water or steam."
            },
            {
                "title": "Salt Water Gargle",
                "description": "Reduces inflammation and helps clear mucus from the throat.",
                "steps": ["Dissolve 1/2 teaspoon of salt in a glass of warm water", "Gargle for 30 seconds and spit out", "Repeat 2-3 times daily"],
                "precautions": "Do not swallow the salt water."
            }
        ]
    },
    "fever": {
        "name": "Fever",
        "remedies": [
            {
                "title": "Stay Hydrated",
                "description": "Fever can lead to dehydration, so it's important to drink fluids.",
                "steps": ["Drink water, clear broths, or electrolyte solutions", "Avoid caffeine and alcohol"],
                "precautions": "Seek medical attention if fever is above 103°F (39.4°C)."
            },
            {
                "title": "Cool Compress",
                "description": "Helps lower body temperature and provide comfort.",
                "steps": ["Soak a washcloth in cool water", "Wring out excess water", "Apply to forehead, wrists, or calves"],
                "precautions": "Do not use ice-cold water as it may cause shivering."
            },
            {
                "title": "Rest",
                "description": "Your body needs energy to fight off infection.",
                "steps": ["Get plenty of sleep", "Avoid strenuous activities", "Stay home from work or school"],
                "precautions": "If fever persists for more than 3 days, see a doctor."
            }
        ]
    },
    "sore_throat": {
        "name": "Sore Throat",
        "remedies": [
            {
                "title": "Salt Water Gargle",
                "description": "Reduces swelling and discomfort in the throat.",
                "steps": ["Mix 1/2 teaspoon of salt in a glass of warm water", "Gargle for 30 seconds and spit out", "Repeat every few hours"],
                "precautions": "Do not swallow the salt water."
            },
            {
                "title": "Honey Tea",
                "description": "Honey has natural antibacterial properties and soothes the throat.",
                "steps": ["Brew a cup of herbal tea", "Add 1-2 teaspoons of honey", "Sip slowly while warm"],
                "precautions": "Do not give honey to children under 1 year old."
            },
            {
                "title": "Humidifier",
                "description": "Adds moisture to the air, preventing throat dryness.",
                "steps": ["Use a cool-mist humidifier in your bedroom", "Clean regularly to prevent mold growth"],
                "precautions": "Keep humidifier out of reach of children."
            }
        ]
    },
    "indigestion": {
        "name": "Indigestion",
        "remedies": [
            {
                "title": "Ginger Tea",
                "description": "Ginger has properties that help settle the stomach.",
                "steps": ["Slice fresh ginger and steep in hot water for 10 minutes", "Strain and drink slowly"],
                "precautions": "Limit consumption if you have a history of gallstones."
            },
            {
                "title": "Peppermint",
                "description": "Helps relax digestive system muscles and reduce spasms.",
                "steps": ["Drink peppermint tea", "Or suck on sugar-free peppermint candies"],
                "precautions": "Avoid if you have GERD as it may worsen symptoms."
            },
            {
                "title": "Apple Cider Vinegar",
                "description": "Can help improve digestion by increasing stomach acid.",
                "steps": ["Mix 1 tablespoon of raw apple cider vinegar in a glass of water", "Drink before meals"],
                "precautions": "Always dilute and rinse mouth afterward to protect tooth enamel."
            }
        ]
    },
    "cold": {
        "name": "Common Cold",
        "remedies": [
            {
                "title": "Chicken Soup",
                "description": "Has anti-inflammatory properties and helps with congestion.",
                "steps": ["Eat warm chicken soup", "Add garlic and ginger for extra benefits"],
                "precautions": "Ensure the soup is not too hot to avoid burning."
            },
            {
                "title": "Vitamin C",
                "description": "Boosts immune system and may shorten cold duration.",
                "steps": ["Eat citrus fruits like oranges and lemons", "Consider vitamin C supplements"],
                "precautions": "Don't exceed recommended daily intake of vitamin C."
            },
            {
                "title": "Rest and Hydration",
                "description": "Allows your body to focus on fighting the virus.",
                "steps": ["Get plenty of sleep", "Drink fluids like water, tea, and broth"],
                "precautions": "See a doctor if symptoms persist beyond 10 days."
            }
        ]
    },
    "allergies": {
        "name": "Allergies",
        "remedies": [
            {
                "title": "Saline Rinse",
                "description": "Helps clear allergens from nasal passages.",
                "steps": ["Use a neti pot or saline spray", "Rinse nasal passages 1-2 times daily"],
                "precautions": "Use distilled or sterilized water, not tap water."
            },
            {
                "title": "Local Honey",
                "description": "May help build tolerance to local pollen.",
                "steps": ["Consume a teaspoon of local honey daily", "Start several weeks before allergy season"],
                "precautions": "Not recommended for children under 1 year."
            },
            {
                "title": "Steam Inhalation",
                "description": "Helps relieve nasal congestion and irritation.",
                "steps": ["Inhale steam from a bowl of hot water", "Add a few drops of eucalyptus oil for extra relief"],
                "precautions": "Be careful to avoid burns from hot water."
            }
        ]
    }
}

def get_remedies_for_symptom(symptom):
    """Get home remedies for a specific symptom"""
    symptom_lower = symptom.lower()
    
    # Check for direct matches
    if symptom_lower in remedies_data:
        return remedies_data[symptom_lower]
    
    # Check for partial matches
    for key in remedies_data:
        if key in symptom_lower or symptom_lower in key:
            return remedies_data[key]
    
    # Return general advice if no specific remedy found
    return {
        "name": symptom,
        "remedies": [
            {
                "title": "General Advice",
                "description": "While we don't have specific remedies for your symptom, here are some general tips:",
                "steps": [
                    "Get plenty of rest",
                    "Stay hydrated by drinking water",
                    "Eat nutritious foods to support your immune system",
                    "Avoid strenuous activities until you feel better"
                ],
                "precautions": "If symptoms persist or worsen, please consult a healthcare professional."
            }
        ]
    }

def get_all_remedies():
    """Get all available home remedies"""
    return remedies_data