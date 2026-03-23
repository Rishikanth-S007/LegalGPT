import json
import random
import os

# 1. Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(BASE_DIR, "..", "data", "legal_dataset.jsonl")
total_pairs = 500

# 2. Law Categories and Seeds
law_categories = [
    {
        "category": "Theft/Robbery",
        "statute": "Indian Penal Code (IPC)",
        "sections": "Sections 378-382",
        "helpline": "100 / 112 (Police)",
        "situations": [
            "My neighbor stole my bicycle from my porch.",
            "A group of people robbed the local grocery store at night.",
            "Someone snatched my gold chain while I was walking home.",
            "My servant stole cash from my drawer while I was away.",
            "A thief broke into my house and took electronic items.",
            "They stole my wallet at the market.",
            "My car was stolen from the parking lot.",
            "My laptop was taken from my classroom.",
            "Someone stole my jewelry box from my cupboard.",
            "A neighbor snatched my gold chain during a festival.",
            "I caught someone stealing my bicycle at midnight."
        ],
        "template": "Under {statute}, Section 378-382, the act described is considered theft or robbery. Definitions:\n- Section 378 defines theft.\n- Section 379 provides punishment for theft (up to 3 years and/or fine).\n- Section 380 covers theft in dwelling house, and Section 382 addresses theft after preparation to cause fear or violence. All these are cognizable and non-bailable offenses. Lodge a police complaint (FIR) at the earliest and preserve any evidence such as CCTV footage or witnesses."
    },
    {
        "category": "Assault/Physical Harm",
        "statute": "Indian Penal Code (IPC)",
        "sections": "Sections 323, 325, 351, 354",
        "helpline": "100 / 112 (Police)",
        "situations": [
            "A stranger slapped me during a heated argument in public.",
            "My landlord physically assaulted me for late rent.",
            "Someone hit me with a stick, causing a bone fracture.",
            "A man tried to outrag my modesty in a crowded bus.",
            "I was bullied and beaten up by a group of seniors.",
            "My boss slapped me in front of colleagues at work.",
            "My teacher hit me with a ruler in class.",
            "A colleague punched me during an office dispute.",
            "Someone kicked me in a road rage incident.",
            "My neighbor physically hurt me over a parking issue.",
            "I was slapped by a customer at my workplace.",
            "A senior officer hit me for being late."
        ],
        "template": "This act falls under {statute} {sections} regarding criminal force and assault. You should seek a medical examination (MLC) and report the incident to the police (100)."
    },
    {
        "category": "Rape/Sexual Assault",
        "statute": "IPC & POCSO Act",
        "sections": "IPC Sections 375, 376, 376AB; POCSO Sections 4, 6, 12",
        "helpline": "1091 (Women Helpline) / 100",
        "situations": [
            "A woman was sexually assaulted by a known person in her office.",
            "A minor girl was abused by a family relative.",
            "I want to know the punishment for rape in India.",
            "Someone forced themselves on me after a party.",
            "What is the POCSO Act for child protection?",
            "A 10-year-old boy was subject to inappropriate touching by a teacher.",
            "My friend’s daughter disclosed sexual abuse by an uncle.",
            "A case of aggravated sexual assault on a minor under 12 was reported.",
            "An adolescent faces repeated sexual harassment by landlord.",
            "A teacher sent explicit messages to a student.",
            "Sexual assault by an authority figure in a boarding school.",
            "A girl was drugged and raped during a trip.",
            "Neighbor molested a child during a birthday party.",
            "I need the law on child sexual exploitation material.",
            "My boyfriend is blackmailing with intimate videos."
        ],
        "template": "This is a grave offense under {statute} {sections} (Rape and POCSO offenses).\n- IPC 375 defines rape, 376 prescribes punishment, and 376AB covers aggravated punishment for minors.\n- POCSO Sections 4, 6 punish penetrative sexual assault on children.\n- Section 12 criminalizes sexual harassment of a child.\nSuch crimes attract rigorous imprisonment (up to life for aggravated cases) and are non-bailable. File a police report immediately and access medical care. Preserve evidence and call 1091 for crisis help."
    },
    {
        "category": "Murder/Homicide",
        "statute": "Indian Penal Code (IPC)",
        "sections": "Sections 302, 304, 307",
        "helpline": "100 / 112 (Police)",
        "situations": [
            "A person intentionally killed his business rival.",
            "Someone fired a gun at me but I survived.",
            "What are the charges for culpable homicide not amounting to murder?",
            "A mob lynched a person on suspicion of theft.",
            "My friend was stabbed to death in a fight."
        ],
        "template": "This is covered under {statute} {sections} (Murder/Attempt to Murder). These are non-bailable, cognizable offenses. Immediate police intervention and a post-mortem/MLC are required."
    },
    {
        "category": "Drug Trafficking",
        "statute": "NDPS Act",
        "sections": "Sections 20, 21, 27, 37",
        "helpline": "112 / NCB Helpline",
        "situations": [
            "Someone is selling ganja near a school campus.",
            "The police caught a person with 5kg of heroin.",
            "What is the punishment for consuming illegal drugs?",
            "A truck was intercepted carrying poppy husk.",
            "Someone planted drugs in my car to frame me."
        ,
            # Expanded for airports and smuggling
            "Caught with drugs at airport security.",
            "Tried to smuggle brown sugar inside shoes on a flight.",
            "Airport police detained me for possessing party drugs.",
            "A courier parcel with narcotics was stopped at customs.",
            "My relative hid heroin in a suitcase before an international flight."
        ],
        "template": "Possession or sale of narcotics is a serious crime under {statute} {sections}. Strict bail conditions apply under Section 37. Report sightings to the Narcotics Control Bureau or local police."
    },
    {
        "category": "Kidnapping/Abduction",
        "statute": "Indian Penal Code (IPC)",
        "sections": "Sections 359, 363, 364, 366, 368",
        "helpline": "100 / 112 (Police)",
        "situations": [
            "Someone stole my wife and is demanding ransom",
            "My wife was taken away forcefully by strangers",
            "A man abducted a woman from the street",
            "My child was kidnapped from school",
            "My sister was taken away by unknown persons",
            "Someone kidnapped my husband for money",
            "A woman was abducted and forced into marriage",
            "My daughter has been missing since yesterday",
            "A gang kidnapped a businessman for ransom",
            "My neighbor's child was taken by strangers"
        ],
        "template": "Acts of kidnapping or abduction are criminal offenses under {statute} {sections}. Section 359 defines kidnapping; Section 363 covers kidnapping of any person (punishable by 7 years and fine); Section 364 covers kidnapping for ransom (imprisonment for life); Section 366 for abduction of women to compel marriage or illicit intercourse; Section 368 covers concealing kidnapped or abducted persons (similar punishment as kidnapping/abduction). Immediate police complaint (FIR) is advised. Provide all details, witnesses, and evidence."
    },
    {
        "category": "Arms Act Offenses",
        "statute": "Arms Act",
        "sections": "Sections 3, 25, 27, 30",
        "helpline": "100 / 112 (Police)",
        "situations": [
            "I was caught carrying a pistol without licence in Delhi",
            "Police found an illegal gun in my house",
            "A person was found with unlicensed weapons",
            "Someone fired a gun in a crowded market",
            "I was arrested for carrying a country-made pistol",
            "Police seized an illegal rifle from my vehicle",
            "A man threatened people with an unlicensed firearm",
            "I have a gun at home but no licence for it",
            "Customs found a hidden weapon in my luggage",
            "A person was caught with prohibited arms"
        ],
        "template": "Unauthorized possession, use, or dealing of firearms is an offence under {statute} {sections}. Section 3: No person shall possess or carry any firearm or ammunition without a valid licence. Section 25: Possessing unlicensed arms is punishable with imprisonment up to 3 years; prohibited arms up to 7 years. Section 27: Using a firearm to cause hurt or fear—imprisonment not less than 3 years up to 7 years. Section 30: Possessing arms in prohibited areas—imprisonment up to 3 years or fine or both. Offenses are non-bailable and can lead to lengthy prison terms. Immediate reporting to law enforcement is required."
    },
    {
        "category": "Motor Vehicles Act Violations",
        "statute": "Motor Vehicles Act",
        "sections": "Sections 52, 122, 184, 206, 304A",
        "helpline": "100 (Police) / 1073 (Road Safety)",
        "situations": [
            "My car was impounded for wrong parking",
            "I hit a person with my bike and he got injured",
            "Police seized my vehicle for parking in no-parking zone",
            "I was in an accident and someone got hurt badly",
            "My vehicle was towed away by traffic police",
            "I knocked down a pedestrian while driving fast",
            "Police stopped me for dangerous driving on highway",
            "My car hit another vehicle and the driver is injured",
            "I was driving drunk and hit a person",
            "Traffic police impounded my truck for overloading"
        ],
        "template": "The Motor Vehicles Act prohibits unauthorized modification (Section 52), parking in no-parking zone (Section 122, vehicle may be impounded and fined), dangerous driving (Section 184, imprisonment or fine), and allows police to seize vehicles violating traffic rules (Section 206). Causing death by negligence (IPC Section 304A) leads to imprisonment up to 2 years. Offenders can be fined, arrested, or prosecuted. Visit the RTO or Traffic Police for clarification, pay fines as prescribed."
    },
    {
        "category": "Moneylender Harassment",
        "statute": "IPC & Money Lenders Act",
        "sections": "IPC Sections 383, 506, State Money Lenders Acts",
        "helpline": "112 / Regional Consumer Help",
        "situations": [
            "A local moneylender is threatening to take my house for a small loan.",
            "The recovery agents are beating me up for missing an EMI.",
            "Moneylender is charging 10% interest per month unlawfully.",
            "I am being harassed by an illegal loan app.",
            "Someone used force to recover a debt from my father."
        ],
        "template": "Extortion and criminal intimidation are punishable under {statute} {sections}. Illegal moneylending also violates State-specific Money Lenders Acts. You can file a complaint with the police and the District Magistrate."
    },
    {
        "category": "Domestic Violence",
        "statute": "DV Act & IPC",
        "sections": "DV Act 2005 (Sec 3, 18), IPC 498A",
        "helpline": "181 / 1091 (Women Helpline)",
        "situations": [
            "My husband and in-laws beat me for more dowry.",
            "I am being mentally harassed and locked in a room by my spouse.",
            "My parents are forcing me into an early marriage against my will.",
            "A woman is facing physical violence every day at home.",
            "How can I get a protection order against my abusive brother?",
            "My father-in-law physically abused my children.",
            "My mother-in-law is torturing me and my kids.",
            "My in-laws are abusing my children emotionally.",
            "A family member physically hurt my kids.",
            "My relative is abusing my children at home."
        ],
        "template": "You are protected under {statute} {sections}. Cruelty by husband or relatives is a cognizable offense. Call 181 or 1091 for immediate assistance. You can also approach a Protection Officer."
    },
    {
        "category": "Cybercrime",
        "statute": "Information Technology (IT) Act",
        "sections": "Sections 66, 66C, 67",
        "helpline": "1930 (Cybercrime Portal)",
        "situations": [
            "Someone hacked my Facebook account and is posting bad things.",
            "I lost money to an OTP scam on WhatsApp.",
            "Someone is sharing my private photos online without consent.",
            "A person created a fake profile in my name.",
            "My company's database was encrypted by ransomware.",
            "I lost money through a UPI fraud call.",
            "Someone called and scammed me with a fake bank alert.",
            "I received a fraud call asking for OTP and lost money.",
            "A scammer took money from my account through phone fraud.",
            "I was victim of a UPI scam and lost 50000 rupees.",
            "Someone stole money online through payment fraud.",
            "I lost money to digital fraud on a fake website."
        ],
        "template": "This is a cybercrime under {statute} {sections}. Report the incident immediately on www.cybercrime.gov.in or call 1930. Capture screenshots as evidence."
    },
    {
        "category": "Fraud/Cheating",
        "statute": "Indian Penal Code (IPC)",
        "sections": "Sections 420, 406",
        "helpline": "100 / 112 (Police)",
        "situations": [
            "A builder took my money but did not give the flat.",
            "Someone sold me fake gold jewelry.",
            "Expectation of high returns from a Ponzi scheme led to loss.",
            "My business partner ran away with company funds.",
            "A person misrepresented themselves to take a loan from me."
        ],
        "template": "Cheating and criminal breach of trust are criminal offenses under {statute} {sections}. You should file a police complaint and can also initiate civil recovery proceedings."
    },
    {
        "category": "Consumer Issues",
        "statute": "Consumer Protection Act (CPA)",
        "sections": "CPA 2019 (Sections 2(47), 35)",
        "helpline": "1800-11-4000 (National Consumer Helpline)",
        "situations": [
            "The laptop I bought has a manufacturing defect.",
            "The airline refused to refund my tickets for a cancelled flight.",
            "I was overcharged by a restaurant for bottled water.",
            "The online store sent me a stone instead of a phone.",
            "Service center is not repairing my AC under warranty.",
            "Builder delayed my flat possession by 3 years",
            "Real estate developer has not given possession after 4 years",
            "Apartment builder took money but construction stopped",
            "My flat was supposed to be delivered 2 years ago but still pending",
            "Housing project delayed and builder is not responding",
            "Property developer asking for more money after missing deadline"
        ],
        "template": "This constitutes deficiency in service/unfair trade practice under {statute} {sections}. You can file a complaint at the District Consumer Commission via the e-Daakhil portal. For builder delays specifically, RERA (Real Estate Regulation Act) Section 18 entitles you to full refund with interest or compensation if the builder fails to complete the project on time. Builder delay is considered deficiency in service under CPA Section 2(11)."
    },
    {
        "category": "Property Disputes",
        "statute": "Transfer of Property Act & IPC",
        "sections": "TOPA Sections 54, 106, 108; IPC Sections 441, 447",
        "helpline": "100 (Police) / Civil Courts",
        "situations": [
            "My neighbor is encroaching on my land and building a wall.",
            "The landlord refused to return my security deposit after I vacated.",
            "Someone forged my property documents and sold my land.",
            "My tenant is not vacating the house even after notice period.",
            "A family member illegally occupied my ancestral property.",
            "The builder did not transfer property ownership after full payment.",
            "My neighbor demolished the boundary wall of my plot.",
            "Someone is claiming ownership of my inherited property.",
            "The previous owner is refusing to hand over property possession.",
            "My landlord entered my rented flat without permission.",
            "A person trespassed into my farmland and destroyed crops.",
            "My property papers were stolen and used to create fake sale deed.",
            "The co-owner is not allowing me to use my share of property.",
            "Someone built a structure on my vacant plot without permission.",
            "My tenant changed the locks and is not giving me access.",
            "The landlord is harassing me to vacate before lease expiry.",
            "My neighbor diverted the water pipeline crossing my land.",
            "Someone illegally cut trees from my property.",
            "The society is not transferring flat ownership in my name.",
            "A person created fake documents showing ownership of my house.",
            "My business partner is claiming sole ownership of joint property.",
            "The seller took money but is not executing the sale deed.",
            "My family is forcing me to give up my property rights.",
            "The builder handed over property with defects and construction issues.",
            "My neighbor blocked the common pathway to my house.",
            "Someone occupied my shop during my absence and won't leave.",
            "The tenant sublet my property without my consent.",
            "My property was attached by court for someone else's debt.",
            "A person is using my land for parking without permission.",
            "The landlord is demanding illegal charges beyond rent agreement.",
            "My property boundaries are being disputed by neighbor.",
            "Someone forged my signature on property transfer documents.",
            "The housing society is not issuing NOC for property sale.",
            "My relative sold family property without consent of all members.",
            "The tenant caused major damage to my property and refuses to pay."
        ],
        "template": "Property disputes are governed by {statute} {sections}. TOPA Section 54 deals with sale of immovable property; Section 106 covers notice requirements for lease termination; Section 108 defines tenant and landlord rights. IPC Section 441 defines criminal trespass (entering property with intent to commit offense or intimidate); Section 447 prescribes punishment for criminal trespass (imprisonment up to 3 months or fine up to ₹500 or both). For civil matters like ownership, partition, eviction, file a civil suit in the appropriate court. For criminal trespass or forgery, file an FIR with police. Maintain all property documents, sale deeds, lease agreements, receipts, and correspondence as evidence. Consider mediation for family property disputes."
    },
    {
        "category": "Labour Law",
        "statute": "Industrial Disputes Act & Labour Laws",
        "sections": "IDA Sections 2A, 25F; EPF Act 1952; Payment of Wages Act 1936",
        "helpline": "1800-11-8005 (Labour Ministry) / Regional Labour Office",
        "situations": [
            "My employer terminated me without notice or compensation.",
            "The company has not paid my salary for 3 months.",
            "I was fired from job without any valid reason.",
            "My employer is not depositing PF contributions.",
            "The factory owner made me work 14 hours daily without overtime pay.",
            "I was removed from service after raising safety concerns.",
            "My company deducted salary without explanation.",
            "The employer is not providing appointment letter or payslips.",
            "I was denied maternity leave as per law.",
            "My wages are below minimum wage prescribed by government.",
            "The company forced me to resign by creating hostile environment.",
            "My employer is not giving relieving letter after resignation.",
            "I was terminated during medical leave for serious illness.",
            "The contractor is not paying wages to construction workers.",
            "My employer refuses to pay gratuity after 10 years of service.",
            "I was suspended without inquiry or charges.",
            "The company is forcing unpaid overtime and weekend work.",
            "My employer discriminated against me based on gender.",
            "I was laid off without proper retrenchment compensation.",
            "The factory has no safety equipment for workers.",
            "My employer is deducting excess amount from salary as penalty.",
            "I am being harassed at workplace by senior employees.",
            "The company changed my designation without consent and reduced salary.",
            "My employer is not providing ESI medical benefits.",
            "I was denied earned leave and casual leave.",
            "The contractor abandoned the project without paying workers.",
            "My employer terminated me after I complained about harassment.",
            "The company is forcing me to work on national holidays without extra pay.",
            "My salary is delayed every month by 20-30 days.",
            "I was removed for joining a workers' union.",
            "The employer is not issuing experience certificate after resignation.",
            "My workplace has unsafe conditions leading to accidents.",
            "The company reduced my salary without prior notice or agreement.",
            "I was denied promotion despite meeting all criteria.",
            "My employer refuses to accept my resignation and release me."
        ],
        "template": "Labour rights are protected under {statute} {sections}. IDA Section 2A defines 'appropriate government' for dispute resolution; Section 25F mandates notice and retrenchment compensation (15 days wages for each completed year of service). EPF Act 1952 makes employer contributions to Provident Fund mandatory for establishments with 20+ employees. Payment of Wages Act 1936 requires timely wage payment (within 7 days for establishments with <1000 workers; within 10 days for larger establishments) and restricts unauthorized deductions. Unfair termination, non-payment of wages, denial of statutory benefits (PF, ESI, gratuity, leave), workplace harassment, and unsafe working conditions are violations. File complaints with the Labour Commissioner, Regional Labour Office, or approach Labour Court. For PF/ESI grievances, contact EPFO or ESIC. For workplace harassment, approach Internal Complaints Committee (ICC) under POSH Act 2013. Maintain employment documents, salary slips, appointment letter, termination notice, and correspondence as evidence."
    },
    {
        "category": "Education & Student Rights",
        "statute": "RTE Act 2009, UGC Regulations 2015, IPC",
        "sections": "RTE Section 17, UGC Ragging Reg. 2015, IPC 323",
        "helpline": "1098 (Childline) / 1800-11-8000 (Education)",
        "situations": [
            "My teacher slapped me in front of the entire class.",
            "A college principal rusticated me without a fair hearing.",
            "A student was sexually harassed by a professor on campus.",
            "A school expelled a 12-year-old child because her parents protested against fee hike.",
            "My classmate was verbally abused and humiliated by staff for being from a minority group.",
            "A college is refusing to return my original certificates after I left the course."
        ],
        "template": "Physical punishment and harassment in educational settings are prohibited under the Right to Education (RTE) Act Section 17 and UGC (Curbing Ragging) Regulations 2015. IPC Section 323 makes voluntary causing of hurt a punishable offense. Every student has a right to safety and dignity in schools and colleges. Approach the Child Welfare Committee, school management, UGC, or the police as required."
    }
]

def generate_variation(situation, template, cat_info):
    # Add some variability to the situation
    prefixes = ["Hello, ", "Please guide me: ", "I need help, ", "What to do if ", ""]
    situation = random.choice(prefixes) + situation
    
    # Construct output with structured labels as requested
    output = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are LegalGPT, an AI assistant for Indian Law. Your goal is to map user queries accurately to the correct laws (IPC, NDPS, IT Act, CPA, etc.). Never answer criminal queries with the Consumer Protection Act.

<|start_header_id|>user<|end_header_id|>
{situation}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
**Applicable Law + Section:** {cat_info['statute']}, {cat_info['sections']}
**Legal Position:** {template.format(statute=cat_info['statute'], sections=cat_info['sections'])}
**Predicted Outcome:** High probability of legal action if evidence (photos, documents, witness) is present.
**Risk Level:** {'High' if 'Murder' in cat_info['category'] or 'Rape' in cat_info['category'] else 'Medium'}
**Next Steps:** 1. Gather evidence. 2. Contact legal counsel. 3. File a formal complaint.
**Helpline Numbers:** {cat_info['helpline']}
**Disclaimer:** This is AI-generated advice. Consult a licensed advocate for court matters.<|eot_id|>"""
    
    return {
        "instruction": situation,
        "output": output,
        "category": cat_info['category'],
        "statute": cat_info['statute']
    }

def main():
    print("Generating balanced legal dataset...")
    dataset = []
    
    records_per_category = total_pairs // len(law_categories)
    
    for cat_info in law_categories:
        situations = cat_info['situations']
        template = cat_info['template']
        
        for _ in range(records_per_category):
            base_situation = random.choice(situations)
            # Add some slight variation logic here if needed
            dataset.append(generate_variation(base_situation, template, cat_info))
    
    # Shuffle dataset
    random.shuffle(dataset)
    
    # Ensure dir exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save as JSONL
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    # Count categories for verification
    counts = {}
    for entry in dataset:
        cat = entry['category']
        counts[cat] = counts.get(cat, 0) + 1
    
    print("Dataset Generation Summary:")
    for cat, count in counts.items():
        print(f" - {cat}: {count}")
    print(f"\nTotal: {len(dataset)} pairs across {len(law_categories)} categories.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()
