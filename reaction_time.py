import time
import random
import csv
from datetime import datetime
from pathlib import Path

def calculate_percentile(rt):
    """compare to general population norms"""
    # based on typical adult reaction time distributions
    if rt < 180:
        return 99, "Exceptional - faster than 99% of people"
    elif rt < 200:
        return 95, "Excellent - faster than 95% of people"
    elif rt < 230:
        return 85, "Above average"
    elif rt < 270:
        return 50, "Average"
    elif rt < 320:
        return 25, "Below average"
    else:
        return 10, "Slow - you might be tired!"

def get_interpretation(avg_rt, time_of_day, trial_rts):
    """provide psychological interpretation of results"""
    
    insights = []
    
    # time of day effect
    hour = datetime.now().hour
    if 6 <= hour < 10:
        insights.append("☀️  Morning testing: cortisol levels are typically high, which can help reaction time")
    elif 14 <= hour < 16:
        insights.append("😴 Afternoon dip: this is when circadian alertness typically drops")
    elif 22 <= hour or hour < 6:
        insights.append("🌙 Late night: reduced alertness may be affecting your performance")
    
    # variability analysis (cognitive consistency)
    variability = max(trial_rts) - min(trial_rts)
    if variability < 30:
        insights.append("🎯 Very consistent responses - strong attentional control")
    elif variability < 60:
        insights.append("📊 Normal variability in responses")
    else:
        insights.append("📈 High variability - might indicate fluctuating attention or fatigue")
    
    # learning effect (comparing first vs last trials)
    first_half = sum(trial_rts[:len(trial_rts)//2]) / (len(trial_rts)//2)
    second_half = sum(trial_rts[len(trial_rts)//2:]) / (len(trial_rts) - len(trial_rts)//2)
    
    if second_half < first_half - 15:
        insights.append("⬆️  Practice effect detected: you got faster as you warmed up")
    elif second_half > first_half + 15:
        insights.append("⬇️  Fatigue effect detected: responses slowed over trials")
    
    return insights

def display_histogram(results):
    """show a simple visual of your reaction times"""
    
    print("\nYour reaction times:")
    for i, rt in enumerate(results, 1):
        bars = "█" * int(rt / 20)
        print(f"  Trial {i}: {bars} {rt:.0f}ms")

def load_history():
    """load previous results for comparison"""
    
    filepath = Path.home() / "reaction_time_log.csv"
    
    if not filepath.exists():
        return None
    
    all_averages = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                all_averages.append(float(row["avg_rt_ms"]))
            except:
                pass
    
    if len(all_averages) > 1:  # need previous sessions
        return all_averages[:-1]  # exclude current session
    return None

def reaction_time_test(num_trials=5):
    """run a comprehensive reaction time test"""
    
    results = []
    
    print("\n" + "=" * 50)
    print("🧠  REACTION TIME TEST  🧠")
    print("=" * 50)
    print("\nThis test measures your psychomotor vigilance—")
    print("the speed of your brain's response to visual stimuli.\n")
    print(f"You'll complete {num_trials} trials.")
    print("When you see '>>> GO! <<<', press Enter immediately.\n")
    
    input("Press Enter when you're ready to start...")
    
    for trial in range(1, num_trials + 1):
        print(f"\n{'─' * 30}")
        print(f"Trial {trial} of {num_trials}")
        print("Waiting...")
        
        # random delay between 2-5 seconds
        time.sleep(random.uniform(2, 5))
        
        print("\n>>> GO! <<<")
        start_time = time.time()
        input()
        end_time = time.time()
        
        reaction_time = (end_time - start_time) * 1000
        results.append(reaction_time)
        
        # immediate feedback
        if reaction_time < 200:
            print(f"⚡ {reaction_time:.0f} ms - Excellent!")
        elif reaction_time < 270:
            print(f"✓  {reaction_time:.0f} ms - Good")
        else:
            print(f"   {reaction_time:.0f} ms")
    
    # calculate stats
    avg_rt = sum(results) / len(results)
    fastest = min(results)
    slowest = max(results)
    percentile, percentile_desc = calculate_percentile(avg_rt)
    
    # display results
    print("\n" + "=" * 50)
    print("📊  RESULTS")
    print("=" * 50)
    
    display_histogram(results)
    
    print(f"\n  Average:  {avg_rt:.1f} ms")
    print(f"  Fastest:  {fastest:.1f} ms")
    print(f"  Slowest:  {slowest:.1f} ms")
    print(f"\n  Percentile: {percentile}th")
    print(f"  → {percentile_desc}")
    
    # psychological insights
    print("\n" + "=" * 50)
    print("🔬  ANALYSIS")
    print("=" * 50)
    
    insights = get_interpretation(avg_rt, datetime.now().hour, results)
    for insight in insights:
        print(f"\n  {insight}")
    
    # compare to history
    history = load_history()
    if history:
        personal_avg = sum(history) / len(history)
        diff = avg_rt - personal_avg
        print(f"\n  📈 Personal history ({len(history)} previous sessions):")
        print(f"     Your usual average: {personal_avg:.1f} ms")
        if diff < -10:
            print(f"     Today: {abs(diff):.0f} ms FASTER than usual 🎉")
        elif diff > 10:
            print(f"     Today: {diff:.0f} ms slower than usual")
        else:
            print(f"     Today: consistent with your baseline")
    
    # save results
    save_results(results, avg_rt)
    
    print("\n" + "=" * 50)
    print("Test complete!")
    print("=" * 50 + "\n")
    
    return results

def save_results(results, avg_rt):
    """save results to CSV"""
    
    filepath = Path.home() / "reaction_time_log.csv"
    file_exists = filepath.exists()
    
    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)
        
        if not file_exists:
            writer.writerow(["date", "time", "avg_rt_ms", "fastest_ms", "slowest_ms", "all_trials_ms"])
        
        now = datetime.now()
        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M"),
            f"{avg_rt:.1f}",
            f"{min(results):.1f}",
            f"{max(results):.1f}",
            "|".join([f"{rt:.1f}" for rt in results])
        ])
    
    print(f"\n✓ Results saved to {filepath}")

if __name__ == "__main__":
    reaction_time_test()
