import csv
import random

# --- Configuration ---
OUTPUT_FILE = "ml/risk-dataset-augmented.csv"
NUM_EXAMPLES_TO_GENERATE = 2000

# --- Word Banks / Entities ---
COMPANIES = ["Innovate Inc.", "Global Corp.", "Quantum Solutions", "Apex Industries", "Starlight Ventures", "Nexus Dynamics", "FutureTech", "EcoSystems Ltd.", "Pioneer Group", "Synergy Systems"]
PEOPLE = ["CEO John Smith", "CFO Maria Garcia", "founder Dr. Evelyn Reed", "lead engineer David Chen", "board member Sarah Jones"]
PRODUCTS = ["Odyssey Platform", "Project Titan", "the new X1 chip", "their flagship software", "a revolutionary new device"]
LOCATIONS = ["the new European headquarters", "a factory in North America", "their Asian market operations", "a research lab in California"]

POSITIVE_VERBS = ["announces", "unveils", "launches", "secures", "achieves", "completes", "expands", "partners with"]
NEGATIVE_VERBS_MEDIUM = ["faces scrutiny over", "is under investigation for", "postpones", "recalls", "warns about", "deals with allegations of"]
NEGATIVE_VERBS_HIGH = ["is found guilty of", "is sanctioned for", "is sued over", "shuts down", "files for bankruptcy following"]

GOOD_NEWS_SUBJECTS = ["record profits", "a successful quarter", "a strategic partnership", "a major breakthrough", "positive clinical trials", "a new sustainability initiative"]
BAD_NEWS_SUBJECTS_MEDIUM = ["supply chain disruptions", "a minor data breach", "customer complaints", "an internal review", "unexpected delays"]
BAD_NEWS_SUBJECTS_HIGH = ["widespread fraud", "a massive data breach", "environmental damages", "criminal charges", "a major product failure"]

# --- Sentence Templates ---
TEMPLATES = {
    "LOW": [
        "{company} {verb} {subject}.",
        "{person} from {company} highlights the success of {product}.",
        "{company} confirms plans to expand {location}.",
        "A successful launch of {product} leads to a surge in {company} stock.",
        "Industry analysts praise {company} for its innovative approach.",
    ],
    "MEDIUM": [
        "{company} {verb} its {subject}.",
        "Regulators are looking into {company} regarding {subject}.",
        "{person} has resigned from {company} amidst rumors of internal conflict.",
        "Reports indicate {company} is struggling with {subject}.",
        "An internal memo from {company} reveals potential issues with {product}.",
    ],
    "HIGH": [
        "{company} {verb} {subject}, leading to a government investigation.",
        "A class-action lawsuit has been filed against {company} concerning {subject}.",
        "{person} has been indicted on charges related to {subject} at {company}.",
        "The {product} from {company} has been linked to significant safety concerns.",
        "Following the scandal, {company} has seen its market value plummet.",
    ]
}

def generate_example(label):
    """Generates a single random example for a given label."""
    template = random.choice(TEMPLATES[label])
    
    if label == "LOW":
        return template.format(
            company=random.choice(COMPANIES),
            verb=random.choice(POSITIVE_VERBS),
            subject=random.choice(GOOD_NEWS_SUBJECTS),
            person=random.choice(PEOPLE),
            product=random.choice(PRODUCTS),
            location=random.choice(LOCATIONS)
        )
    elif label == "MEDIUM":
        return template.format(
            company=random.choice(COMPANIES),
            verb=random.choice(NEGATIVE_VERBS_MEDIUM),
            subject=random.choice(BAD_NEWS_SUBJECTS_MEDIUM),
            person=random.choice(PEOPLE),
            product=random.choice(PRODUCTS)
        )
    elif label == "HIGH":
        return template.format(
            company=random.choice(COMPANIES),
            verb=random.choice(NEGATIVE_VERBS_HIGH),
            subject=random.choice(BAD_NEWS_SUBJECTS_HIGH),
            person=random.choice(PEOPLE),
            product=random.choice(PRODUCTS)
        )

# --- Main Script ---
if __name__ == "__main__":
    print(f"Generating {NUM_EXAMPLES_TO_GENERATE} augmented examples...")
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['text', 'label'])  # Write header
        
        for i in range(NUM_EXAMPLES_TO_GENERATE):
            # Generate a balanced number of examples for each class
            if i % 3 == 0:
                label = "LOW"
            elif i % 3 == 1:
                label = "MEDIUM"
            else:
                label = "HIGH"
            
            text = generate_example(label)
            writer.writerow([text, label])
            
    print(f"Successfully created augmented dataset at {OUTPUT_FILE}")