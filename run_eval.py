from main import app
from eval_questions import eval_set

def check_answer(answer, expected_keywords):
    answer_lower = answer.lower()
    return any(kw.lower() in answer_lower for kw in expected_keywords)

def run_evaluation():
    correct = 0
    total = len(eval_set)
    results = []

    for item in eval_set:
        result = app.invoke({"question": item["question"]})
        answer = result["answer"]
        passed = check_answer(answer, item["expected_keywords"])
        correct += passed
        results.append({
            "question": item["question"],
            "answer": answer,
            "passed": passed
        })
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {item['question']}")
        if not passed:
            print(f"       Got: {answer[:100]}")

    accuracy = (correct / total) * 100
    print(f"\n=== Accuracy: {correct}/{total} ({accuracy:.1f}%) ===")
    return accuracy

if __name__ == "__main__":
    run_evaluation()