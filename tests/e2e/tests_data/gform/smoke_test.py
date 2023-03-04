from loader.gform_loader import load_gform_results

PATH = "tests/gform/smoke_test_gform_results.xlsx"

def run_smoke_test():
    df = load_gform_results(PATH, "some_key")
    print(df)

if __name__ == "__main__":
    run_smoke_test()
