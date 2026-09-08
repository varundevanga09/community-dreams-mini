import os

docs = {
    "doc1.txt": "Q: What should I do if I have a mild fever?\nA: Rest, stay hydrated, and monitor your temperature. Seek medical care if fever exceeds 103°F or lasts more than 3 days.",
    "doc2.txt": "Q: How can I find free food assistance in my community?\nA: Contact your local food bank or community food alliance. Many organizations offer weekly distributions with no eligibility requirements.",
    "doc3.txt": "Q: What are signs of dehydration?\nA: Dry mouth, dizziness, dark yellow urine, and fatigue are common signs. Drink water and electrolytes, and seek care if symptoms are severe.",
    "doc4.txt": "Q: How do I apply for emergency housing assistance?\nA: Contact your local Department of Social Services or a housing nonprofit. Bring ID, proof of income, and proof of current housing situation.",
    "doc5.txt": "Q: What should I do for a minor cut or wound?\nA: Clean the wound with water, apply gentle pressure to stop bleeding, and cover with a clean bandage. Seek medical care if bleeding doesn't stop or the wound is deep.",
    "doc6.txt": "Q: How can I access free mental health counseling?\nA: Many community health centers offer sliding-scale or free counseling. Crisis lines are also available 24/7 for immediate support.",
    "doc7.txt": "Q: What is the recommended amount of daily water intake?\nA: A general guideline is about 8 cups (64 oz) per day, though needs vary based on activity level, climate, and body size.",
    "doc8.txt": "Q: How do I find free vaccination clinics?\nA: Check with your local public health department or community health center. Many offer free or low-cost vaccines regardless of insurance status.",
    "doc9.txt": "Q: What should I do if I'm experiencing chest pain?\nA: Chest pain can be a medical emergency. Call emergency services immediately, especially if accompanied by shortness of breath, sweating, or pain radiating to the arm.",
    "doc10.txt": "Q: How can I get help paying utility bills?\nA: Look into the Low Income Home Energy Assistance Program (LIHEAP) or contact your utility provider directly about hardship programs.",
    "doc11.txt": "Q: What are common symptoms of the flu versus a cold?\nA: Flu symptoms tend to be more severe and sudden, including high fever, body aches, and fatigue. Colds usually develop gradually with milder symptoms like a runny nose.",
    "doc12.txt": "Q: How do I find free legal aid services?\nA: Legal aid societies and nonprofit law clinics offer free services for qualifying individuals, often based on income. Search for legal aid organizations in your county.",
    "doc13.txt": "Q: What should I do to manage seasonal allergies?\nA: Over-the-counter antihistamines, avoiding known triggers, and keeping windows closed during high pollen days can help manage symptoms.",
    "doc14.txt": "Q: How can I access free job training programs?\nA: Local workforce development boards and community colleges often offer free or subsidized job training and certification programs.",
    "doc15.txt": "Q: What should I do if I think I have food poisoning?\nA: Stay hydrated, rest, and avoid solid foods until symptoms improve. Seek medical care if you have a high fever, blood in stool, or symptoms lasting more than 3 days.",
    "doc16.txt": "Q: How do I find childcare assistance programs?\nA: State-run childcare subsidy programs and local nonprofits can help cover costs based on income eligibility. Contact your state's department of human services.",
    "doc17.txt": "Q: What is the proper way to treat a minor burn?\nA: Cool the burn under running water for 10-15 minutes, do not apply ice directly, and cover loosely with a clean bandage. Seek care for burns larger than 3 inches or on the face.",
    "doc18.txt": "Q: How can I get help with transportation to medical appointments?\nA: Many Medicaid programs cover non-emergency medical transportation. Community organizations may also offer volunteer driver programs.",
    "doc19.txt": "Q: What should I know about managing high blood pressure?\nA: Regular monitoring, reducing sodium intake, staying active, and taking prescribed medication consistently are key. Consult a doctor for personalized guidance.",
    "doc20.txt": "Q: How do I find free English language classes?\nA: Public libraries, community colleges, and nonprofit organizations often offer free ESL classes for adults, sometimes with childcare provided.",
}

os.makedirs("docs", exist_ok=True)
for filename, content in docs.items():
    with open(os.path.join("docs", filename), "w") as f:
        f.write(content)
    print(f"Created: {filename}")

print(f"\nDone. {len(docs)} files created in ./docs")