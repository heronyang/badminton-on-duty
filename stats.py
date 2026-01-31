import os
import re
import glob
from collections import Counter, defaultdict
from itertools import combinations
import statistics

# --- 設定 ---
DATA_DIR = '.' 

def get_files_by_year(directory):
    """
    Returns a dictionary: {'2024': ['2024-01-01', ...], '2025': ...}
    """
    files = glob.glob(os.path.join(directory, "????-??-??.txt"))
    year_map = defaultdict(list)
    
    for f in files:
        basename = os.path.basename(f)
        if re.match(r'\d{4}-\d{2}-\d{2}\.txt$', basename):
            date_str = basename.replace('.txt', '')
            year = date_str.split('-')[0]
            year_map[year].append(date_str)
            
    for year in year_map:
        year_map[year].sort()
        
    return dict(sorted(year_map.items()))

def normalize_name(raw_name):
    # 移除開頭的數字 (e.g., "1. ")
    clean = re.sub(r'^\d+\.\s+', '', raw_name.strip())
    return clean

def get_host_handle(name_str):
    # 判斷是誰帶的朋友
    match = re.search(r'\((@[\w_.]+)\)', name_str)
    if match: return match.group(1)
    if name_str.startswith('@'): return name_str
    return None

def calculate_streaks(all_session_dates, attendance_map):
    """
    計算目前的連續出席週數 (Current Streak)
    """
    current_streaks = {}
    all_people = set()
    for ppl in attendance_map.values():
        all_people.update(ppl)
        
    sorted_dates = sorted(all_session_dates, reverse=True)
    
    for person in all_people:
        streak = 0
        for date in sorted_dates:
            if person in attendance_map[date]:
                streak += 1
            else:
                break 
        current_streaks[person] = streak
        
    return current_streaks

def analyze_year(year, dates):
    print(f"\n{'='*12} 🏸 {year} 羽球群年度回顧 🏸 {'='*12}")
    print(f"統計期間：共 {len(dates)} 次打球活動\n")

    attendance_map = defaultdict(list)
    signup_positions = defaultdict(list)
    on_duty_counts = Counter()
    
    # 解析檔案
    for date in dates:
        # 1. 報名名單
        signup_path = os.path.join(DATA_DIR, f"{date}.txt")
        if os.path.exists(signup_path):
            with open(signup_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and re.match(r'^\d+\.', line):
                        # 抓取報名順序
                        pos_match = re.match(r'^(\d+)\.', line)
                        position = int(pos_match.group(1))
                        
                        name = normalize_name(line)
                        attendance_map[date].append(name)
                        signup_positions[name].append(position)

        # 2. 值日生名單
        output_path = os.path.join(DATA_DIR, f"{date}-output.txt")
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                for line in f:
                    match = re.search(r':\d{2}.*:\s+(.+?)\s+\+\s+(.+?)$', line)
                    if match:
                        p1, p2 = match.group(1).strip(), match.group(2).strip()
                        on_duty_counts[p1] += 1
                        on_duty_counts[p2] += 1

    # --- 開始計算各項數據 ---

    # 1. 出席總數
    total_attendance = Counter()
    for attendees in attendance_map.values():
        total_attendance.update(attendees)

    # 2. 揪團王
    promoters = Counter()
    for name in total_attendance.keys():
        host = get_host_handle(name)
        if host and host != name:
            promoters[host] += total_attendance[name]

    # 3. 黏踢踢 CP (計算同時出席的次數)
    social_pairs = Counter()
    for attendees in attendance_map.values():
        # 排序以確保 A+B 和 B+A 視為同一組
        sorted_attendees = sorted(attendees)
        for pair in combinations(sorted_attendees, 2):
            social_pairs[pair] += 1

    # 4. 值日生機率 (至少出席 3 次才列入)
    ratios = []
    for person, attended in total_attendance.items():
        if attended >= 3:
            duties = on_duty_counts[person]
            ratio = (duties / attended) * 100
            ratios.append((person, attended, duties, ratio))
    
    most_likely_duty = sorted(ratios, key=lambda x: x[3], reverse=True)
    least_likely_duty = sorted(ratios, key=lambda x: x[3])

    # 5. 手速排行 (平均報名順位) - 至少出席 3 次
    speed_stats = []
    for person, positions in signup_positions.items():
        if len(positions) >= 3:
            avg_pos = statistics.mean(positions)
            speed_stats.append((person, avg_pos))
            
    fastest_fingers = sorted(speed_stats, key=lambda x: x[1])
    slow_pokes = sorted(speed_stats, key=lambda x: x[1], reverse=True)

    # 6. 連續出席 (Current Streak)
    streaks = calculate_streaks(dates, attendance_map)
    sorted_streaks = sorted(streaks.items(), key=lambda x: x[1], reverse=True)

    # --- 輸出結果 (台灣鄉民風標題) ---

    def print_list(emoji, title, items, formatter):
        print(f"\n{emoji} {title}")
        print("-" * 40)
        for i, item in enumerate(items[:5], 1):
            print(f"{i}. {formatter(item)}")

    # 1. 出席王
    print_list("🏟️", "球場地縛靈 (出席次數最多)", 
               total_attendance.most_common(), 
               lambda x: f"{x[0]}: {x[1]} 次")

    # 2. 連續出席
    print_list("🔥", "風雨無阻全勤獎 (目前連續出席)", 
               [s for s in sorted_streaks if s[1] > 1], 
               lambda x: f"{x[0]}: 連續 {x[1]} 週")

    # 3. 手速最快
    print_list("⚡", "單身二十年的手速 (平均報名順位)", 
               fastest_fingers, 
               lambda x: f"{x[0]}: 平均第 {x[1]:.1f} 順位")
    
    # 4. 手速最慢
    print_list("🐢", "心臟最大顆壓線王 (最晚報名)", 
               slow_pokes, 
               lambda x: f"{x[0]}: 平均第 {x[1]:.1f} 順位")

    # 5. 值日生王 (衰)
    print_list("🧹", "命中注定值日生 (被抽中機率最高)", 
               most_likely_duty, 
               lambda x: f"{x[0]}: {x[3]:.1f}% ({x[2]}/{x[1]} 次)")

    # 6. 閃躲王 (運氣好)
    print_list("🌟", "天公伯有保庇 (被抽中機率最低)", 
               least_likely_duty, 
               lambda x: f"{x[0]}: {x[3]:.1f}% ({x[2]}/{x[1]} 次)")

    # 7. CP 榜 (特殊過濾邏輯)
    print(f"\n💖 黏踢踢 CP (最常一起出現的組合)")
    print("-" * 40)
    
    seen_people = set()
    count = 0
    # 從最常出現的 pair 開始遍歷
    for pair, freq in social_pairs.most_common():
        p1, p2 = pair
        # 如果這對 CP 的任何一人已經在榜單上了，就跳過 (避免 A 跟 B, A 跟 C 重複出現)
        if p1 not in seen_people and p2 not in seen_people:
            count += 1
            print(f"{count}. {p1} & {p2}: {freq} 次")
            seen_people.add(p1)
            seen_people.add(p2)
            
            if count >= 5: # 只取前 5 對
                break

    # 8. 揪團王
    if promoters:
        print_list("📢", "最強揪團王 (帶最多朋友)", 
                   promoters.most_common(), 
                   lambda x: f"{x[0]}: {x[1]} 人")

def main():
    years_data = get_files_by_year(DATA_DIR)
    
    if not years_data:
        print("找不到資料檔案，請確認目錄下是否有 YYYY-MM-DD.txt 格式的檔案。")
        return

    for year, dates in years_data.items():
        analyze_year(year, dates)
        print("\n\n")

if __name__ == "__main__":
    main()
