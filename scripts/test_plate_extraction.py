import re
from backend.ai.normaliser import normalize_plate

def extract_plate_from_ocr(results):
    """
    Given EasyOCR results: list of (bbox, text, prob)
    Smartly extract and normalize Indian vehicle registration number.
    Handles:
    - Single line: 'MH 12 AB 3456', 'GJ01AB1234'
    - Multi-line / Split boxes: ['MH 12', 'AB 3456']
    - Noise prefixes: ['IND', 'MH12AB3456']
    - Common optical confusions: 'HH' -> 'MH', '4B' -> 'AB', 'O' -> '0', etc.
    """
    if not results:
        return None, 0.0

    raw_candidates = []
    # 1. Inspect each box individually
    for item in results:
        text = item[1]
        prob = item[2]
        clean = re.sub(r'[^A-Z0-9]', '', text.upper())
        if clean and not any(k in clean for k in ["SETU", "EDGE", "HIGHWAY", "STATUS", "WHEP"]):
            raw_candidates.append((clean, prob))

    # Pattern for Indian plates
    pattern = re.compile(r'([A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4})')

    # Strategy A: Check each candidate directly (with and without normalization)
    for clean, prob in raw_candidates:
        norm = normalize_plate(clean)
        m = pattern.search(norm)
        if m:
            return m.group(1), prob
        m_raw = pattern.search(clean)
        if m_raw:
            return normalize_plate(m_raw.group(1)), prob

    # Strategy B: Combine adjacent/all text boxes (sorted by vertical position)
    # Sort boxes top to bottom, then left to right
    sorted_results = sorted(results, key=lambda r: (r[0][0][1], r[0][0][0]))
    combined_clean = ""
    avg_prob = 0.0
    valid_count = 0
    for r in sorted_results:
        text = r[1]
        c = re.sub(r'[^A-Z0-9]', '', text.upper())
        # Strip 'IND' country code commonly found on Indian HSRP plates on the left
        if c == "IND":
            continue
        if any(k in c for k in ["SETU", "EDGE", "HIGHWAY", "STATUS", "WHEP"]):
            continue
        combined_clean += c
        avg_prob += r[2]
        valid_count += 1

    if valid_count > 0:
        avg_prob /= valid_count

    norm_comb = normalize_plate(combined_clean)
    m = pattern.search(norm_comb)
    if m:
        return m.group(1), avg_prob

    m_raw = pattern.search(combined_clean)
    if m_raw:
        return normalize_plate(m_raw.group(1)), avg_prob

    # Strategy C: Relaxed match (e.g. 8-10 chars if starting with valid/confusable state)
    if 8 <= len(norm_comb) <= 11:
        if norm_comb[:2].isalpha() and norm_comb[-4:].isdigit():
            return norm_comb, avg_prob

    return None, 0.0

if __name__ == "__main__":
    test_cases = [
        [([(0,0)], "HH12AB3456", 0.9)],
        [([(0,0)], "MH 12 AB 3456", 0.92)],
        [([(0,0)], "MH 12", 0.88), ([(0,10)], "AB 3456", 0.91)],
        [([(0,0)], "IND", 0.95), ([(0,0)], "MH 12", 0.88), ([(0,10)], "4B 3456", 0.91)],
        [([(0,0)], "GJ01AB1234", 0.97)],
        [([(0,0)], "G301AB1234", 0.85)],
        [([(0,0)], "DL01AB4321", 0.93)],
    ]
    for tc in test_cases:
        res, prob = extract_plate_from_ocr(tc)
        print(f"Inputs: {[t[1] for t in tc]} => Detected: {res} (Conf: {prob:.2f})")
