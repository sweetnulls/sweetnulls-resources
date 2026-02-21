# ============================================
# YOUR FIRST SEX DATASET: Python Edition
# Sweet Nulls | sweetnulls.com
# ============================================
# Install these once (uncomment and run):
# pip install pandas matplotlib seaborn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Make the charts pretty
sns.set_theme(style="whitegrid")
palette = ["#d4768a", "#8a4d5e", "#c9a0aa", "#5e2d3a", "#f0d4da"]

# --- STEP 1: Load your data ---
df = pd.read_csv("sweet_nulls_template.csv")

# --- STEP 2: Your first look ---
print(f"Total encounters: {len(df)}")
print(f"Average satisfaction: {df['satisfaction_rating'].mean():.1f} / 10")
print(f"Average duration: {df['duration_minutes'].mean():.0f} minutes")

# --- STEP 3: When are you having the best sex? ---
day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
df["day_of_week"] = pd.Categorical(df["day_of_week"], categories=day_order, ordered=True)

day_summary = df.groupby("day_of_week", observed=True).agg(
    avg_satisfaction=("satisfaction_rating", "mean"),
    avg_duration=("duration_minutes", "mean"),
    count=("satisfaction_rating", "count")
).round(1)

print("\n--- Your Best Days ---")
print(day_summary.sort_values("avg_satisfaction", ascending=False))

# By time of day
time_summary = df.groupby("time_of_day").agg(
    avg_satisfaction=("satisfaction_rating", "mean"),
    count=("satisfaction_rating", "count")
).round(1)

print("\n--- Morning Person or Night Owl? ---")
print(time_summary.sort_values("avg_satisfaction", ascending=False))

# --- STEP 4: Who starts it, and does it matter? ---
initiator_summary = df.groupby("initiator").agg(
    avg_satisfaction=("satisfaction_rating", "mean"),
    avg_duration=("duration_minutes", "mean"),
    count=("satisfaction_rating", "count")
).round(1)

print("\n--- Who Initiates (and does it matter?) ---")
print(initiator_summary)

# --- STEP 5: What activities correlate with satisfaction? ---
activities_expanded = df.assign(
    activities=df["activities"].str.split(";")
).explode("activities")

activity_summary = activities_expanded.groupby("activities").agg(
    avg_satisfaction=("satisfaction_rating", "mean"),
    times_logged=("satisfaction_rating", "count")
).round(1).sort_values("avg_satisfaction", ascending=False)

print("\n--- Your Satisfaction by Activity ---")
print(activity_summary)

# --- STEP 6: Does duration actually matter? ---
cor_duration = df["duration_minutes"].corr(df["satisfaction_rating"])
print(f"\n--- Duration vs Satisfaction Correlation ---")
print(f"Correlation: {cor_duration:.2f}")
if cor_duration > 0.5:
    print("Longer sessions tend to be more satisfying for you.")
elif cor_duration < -0.5:
    print("Interestingly, shorter sessions tend to rate higher.")
else:
    print("Duration doesn't strongly predict your satisfaction. It's not about the clock.")

# --- STEP 7: Your cycle, your data ---
if df["cycle_day"].notna().any():
    def get_phase(day):
        if pd.isna(day): return "unknown"
        if day <= 5: return "menstrual"
        if day <= 13: return "follicular"
        if day <= 16: return "ovulatory"
        if day <= 28: return "luteal"
        return "other"

    df["cycle_phase"] = df["cycle_day"].apply(get_phase)

    cycle_summary = df.groupby("cycle_phase").agg(
        avg_satisfaction=("satisfaction_rating", "mean"),
        count=("satisfaction_rating", "count")
    ).round(1).sort_values("avg_satisfaction", ascending=False)

    print("\n--- Satisfaction by Cycle Phase ---")
    print(cycle_summary)

# --- STEP 8: Make it pretty ---

# Chart 1: Satisfaction by day of week
fig, ax = plt.subplots(figsize=(8, 5))
day_plot = df.groupby("day_of_week", observed=True)["satisfaction_rating"].mean()
day_plot.plot(kind="bar", color="#d4768a", ax=ax)
ax.set_title("When Does It Hit Different?", fontsize=14, fontweight="bold")
ax.set_ylabel("Avg Satisfaction (1-10)")
ax.set_xlabel("")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
plt.figtext(0.99, 0.01, "sweetnulls.com | your data, your pleasure",
            ha="right", fontsize=8, style="italic", color="gray")
plt.tight_layout()
plt.savefig("satisfaction_by_day.png", dpi=150)
print("\nSaved: satisfaction_by_day.png")

# Chart 2: Duration vs satisfaction
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df["duration_minutes"], df["satisfaction_rating"],
           color="#d4768a", s=80, zorder=5)
z = pd.np.polyfit(df["duration_minutes"], df["satisfaction_rating"], 1) if hasattr(pd, 'np') else __import__('numpy').polyfit(df["duration_minutes"], df["satisfaction_rating"], 1)
p = __import__('numpy').poly1d(z)
x_line = sorted(df["duration_minutes"])
ax.plot(x_line, p(x_line), color="#8a4d5e", linewidth=2)
ax.set_title("Is Longer Actually Better?", fontsize=14, fontweight="bold")
ax.set_xlabel("Duration (minutes)")
ax.set_ylabel("Satisfaction (1-10)")
ax.annotate(f"r = {cor_duration:.2f}", xy=(0.05, 0.95), xycoords="axes fraction",
            fontsize=11, color="#8a4d5e")
plt.figtext(0.99, 0.01, "sweetnulls.com | your data, your pleasure",
            ha="right", fontsize=8, style="italic", color="gray")
plt.tight_layout()
plt.savefig("duration_vs_satisfaction.png", dpi=150)
print("Saved: duration_vs_satisfaction.png")

print("\n\nDone! Check your folder for charts.")
print("Now go make more data. For science.")