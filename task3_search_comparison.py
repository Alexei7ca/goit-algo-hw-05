import timeit
import math
from typing import List, Tuple, Optional, Any, Dict, Dict

# Rabin-Karp Algorithm (No changes)
def rabin_karp(text: str, pattern: str) -> int:
    n = len(text)
    m = len(pattern)
    q = 101
    d = 256
    
    if m == 0 or m > n:
        return -1
        
    h = pow(d, m-1, q)
    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i+m] == pattern:
                return i
        
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
                
    return -1

# Knuth-Morris-Pratt (KMP) Algorithm (No changes)

def compute_lps(pattern: str) -> List[int]:
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> int:
    n = len(text)
    m = len(pattern)
    
    if m == 0 or m > n:
        return -1
        
    lps = compute_lps(pattern)
    i = 0
    j = 0
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return -1

# Boyer-Moore Algorithm 
def bad_char_heuristic(pattern: str, size: int) -> Dict[str, int]:
    # Stores the last occurrence index of each character in the pattern
    # Using a dictionary allows flexible indexing for Unicode (like Cyrillic)
    BAD_CHAR: Dict[str, int] = {}
    for i in range(size):
        BAD_CHAR[pattern[i]] = i
    return BAD_CHAR

def boyer_moore_search(text: str, pattern: str) -> int:
    n = len(text)
    m = len(pattern)
    
    if m == 0 or m > n:
        return -1
        
    bad_char = bad_char_heuristic(pattern, m)
    
    s = 0
    while s <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
            
        if j < 0:
            return s
        else:
            # Use .get() to safely handle characters not present in the pattern (defaulting to -1, or -1 if not found)
            mismatched_char = text[s + j]
            # If char is in BAD_CHAR, get its last index, else treat as if it occurred at index -1 (shift by j - (-1) = j + 1)
            last_occurrence = bad_char.get(mismatched_char, -1)
            
            shift = j - last_occurrence
            s += max(1, shift)
            
    return -1

# --- Measurement and Report Logic (No changes) ---

def read_text_file(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}. Please ensure article1.txt and article2.txt are present.")
        return ""

def measure_time(algorithm: callable, text: str, pattern: str, number: int = 100) -> float:
    func_name = algorithm.__name__
    
    stmt = f"{func_name}(text_to_search, pattern_to_search)"
    
    globals_dict = {
        'text_to_search': text, 
        'pattern_to_search': pattern, 
        func_name: algorithm
    }

    times = timeit.repeat(
        stmt, 
        setup="",
        repeat=3, 
        number=number, 
        globals=globals_dict
    )
    return min(times) / number

def run_comparisons(text_name: str, text_content: str, existing_pattern: str, fictitious_pattern: str) -> Dict[str, Dict[str, float]]:
    algorithms = [rabin_karp, kmp_search, boyer_moore_search]
    results = {}
    
    print(f"\nMeasuring Time for {text_name}...")

    for algo in algorithms:
        # Existing Substring
        time_existing = measure_time(algo, text_content, existing_pattern)
        print(f"{algo.__name__} (Existing): {time_existing:.8f} seconds")

        # Fictitious Substring
        time_fictitious = measure_time(algo, text_content, fictitious_pattern)
        print(f"{algo.__name__} (Fictitious): {time_fictitious:.8f} seconds")

        results[algo.__name__] = {
            "existing": time_existing,
            "fictitious": time_fictitious
        }
        
    return results

def generate_markdown_report(all_results: Dict[str, Any], existing_pat: str, fictitious_pat: str):
    report = ["# 📊 Substring Search Algorithm Efficiency Comparison\n"]
    
    def find_fastest(data: Dict[str, float]) -> str:
        if not data: return "N/A"
        return min(data.keys(), key=lambda k: data[k])
    
    report.append("## Детальні результати вимірювань (час на одне виконання в секундах)\n")
    
    for text_name, results in all_results.items():
        report.append(f"### {text_name}\n")
        report.append("| Algorithm | Existing Pattern ('{}') | Fictitious Pattern ('{}') |\n".format(existing_pat, fictitious_pat))
        report.append("| :--- | :---: | :---: |\n")
        
        existing_times = {algo: results[algo]['existing'] for algo in results}
        fictitious_times = {algo: results[algo]['fictitious'] for algo in results}
        
        fastest_existing = find_fastest(existing_times)
        fastest_fictitious = find_fastest(fictitious_times)

        for algo in results.keys():
            e_time = results[algo]['existing']
            f_time = results[algo]['fictitious']
            
            e_str = f"**{e_time:.8f}** (Fastest)" if algo == fastest_existing else f"{e_time:.8f}"
            f_str = f"**{f_time:.8f}** (Fastest)" if algo == fastest_fictitious else f"{f_time:.8f}"
            
            report.append(f"| {algo} | {e_str} | {f_str} |\n")
        report.append("\n")

    report.append("## 🏆 Визначення найшвидшого алгоритму\n")
    report.append("### Найшвидший алгоритм для кожного тексту окремо\n")
    
    report.append("| Текст | Найшвидший (Існуючий підрядок) | Найшвидший (Вигаданий підрядок) |\n")
    report.append("| :--- | :---: | :---: |\n")
    
    for text_name, results in all_results.items():
        existing_times = {algo: results[algo]['existing'] for algo in results}
        fictitious_times = {algo: results[algo]['fictitious'] for algo in results}
        
        fastest_existing = find_fastest(existing_times)
        fastest_fictitious = find_fastest(fictitious_times)
        
        report.append(f"| {text_name} | **{fastest_existing}** | **{fastest_fictitious}** |\n")
    
    report.append("\n### Висновки щодо швидкостей алгоритмів (Загалом)\n")
    
    overall_existing_times = {}
    overall_fictitious_times = {}
    
    for text_name, results in all_results.items():
        for algo in results:
            overall_existing_times.setdefault(algo, []).append(results[algo]['existing'])
            overall_fictitious_times.setdefault(algo, []).append(results[algo]['fictitious'])
            
    overall_avg_existing = {algo: sum(times) / len(times) for algo, times in overall_existing_times.items()}
    overall_avg_fictitious = {algo: sum(times) / len(times) for algo, times in overall_fictitious_times.items()}
    
    overall_fastest_existing = find_fastest(overall_avg_existing)
    overall_fastest_fictitious = find_fastest(overall_avg_fictitious)
    
    report.append("* **Для існуючого підрядка ('{}'):** Найшвидшим за середнім часом виконання виявився алгоритм **{}**.\n".format(existing_pat, overall_fastest_existing))
    report.append("* **Для вигаданого підрядка ('{}'):** Найшвидшим за середнім часом виконання виявився алгоритм **{}**.\n".format(fictitious_pat, overall_fastest_fictitious))
    report.append("\n")
    
    report.append("Очікується, що алгоритм **Боєра-Мура (boyer_moore_search)** буде найшвидшим, особливо для довгих текстів, оскільки він має найменшу асимптотичну складність у найкращому випадку ($O(N/M)$) і використовує стратегію пропуску символів (зсуву).\n")
    report.append("Алгоритм **Кнута-Морріса-Пратта (kmp_search)** ($O(N+M)$) є дуже ефективним у найгіршому випадку (коли підрядок не знайдено), тоді як **Рабіна-Карпа (rabin_karp)** може дещо сповільнюватися через обчислення хешів.")
    
    return "\n".join(report)


def run_task3():
    text1 = read_text_file("article1.txt")
    text2 = read_text_file("article2.txt")
    
    if not text1 or not text2:
        print("Cannot run comparison: Text files could not be loaded.")
        return

    existing_substring = "алгоритм" 
    fictitious_substring = "неіснуюча_послідовність" 

    all_results = {}

    results1 = run_comparisons(
        "Article 1 (стаття 1.txt)", 
        text1, 
        existing_substring, 
        fictitious_substring
    )
    all_results["Article 1 (стаття 1.txt)"] = results1

    results2 = run_comparisons(
        "Article 2 (стаття 2.txt)", 
        text2, 
        existing_substring, 
        fictitious_substring
    )
    all_results["Article 2 (стаття 2.txt)"] = results2
    
    report_content = generate_markdown_report(all_results, existing_substring, fictitious_substring)

    with open("RESULTS.md", "w", encoding="utf-8") as f:
        f.write(report_content)

if __name__ == "__main__":
    run_task3()