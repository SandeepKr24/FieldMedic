import json

from src.agents.orchestrator import triage_patient


def run_evaluation():
    with open("src/eval/test_cases.json", "r") as f:
        test_cases = json.load(f)

    total = len(test_cases)
    correct = 0

    for case in test_cases:

        result = triage_patient(
            symptoms=case["symptoms"]
        )

        prediction = result.triage

        expected = case["expected_triage"]

        passed = prediction == expected

        if passed:
            correct += 1

        print("=" * 60)
        print(case["name"])
        print(f"Expected : {expected}")
        print(f"Predicted: {prediction}")
        print(f"PASS: {passed}")

    accuracy = correct / total * 100

    print("=" * 60)
    print(f"Accuracy: {accuracy:.2f}% ({correct}/{total})")


if __name__ == "__main__":
    run_evaluation()