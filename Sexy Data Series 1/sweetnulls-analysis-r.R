# ============================================
# YOUR FIRST SEX DATASET: R Edition
# Sweet Nulls | sweetnulls.com
# ============================================
# Install these once (uncomment and run):
# install.packages(c("tidyverse", "lubridate"))

library(tidyverse)
library(lubridate)

# --- STEP 1: Load your data ---
df <- read_csv("sweet_nulls_template.csv")

# --- STEP 2: Your first look ---
# How many encounters did you log?
cat("Total encounters:", nrow(df), "\n")
cat("Average satisfaction:", round(mean(df$satisfaction_rating), 1), "/ 10\n")
cat("Average duration:", round(mean(df$duration_minutes)), "minutes\n")

# --- STEP 3: When are you having the best sex? ---
# By day of week
day_summary <- df %>%
  group_by(day_of_week) %>%
  summarise(
    avg_satisfaction = round(mean(satisfaction_rating), 1),
    avg_duration = round(mean(duration_minutes)),
    count = n()
  ) %>%
  arrange(desc(avg_satisfaction))

cat("\n--- Your Best Days ---\n")
print(day_summary)

# By time of day
time_summary <- df %>%
  group_by(time_of_day) %>%
  summarise(
    avg_satisfaction = round(mean(satisfaction_rating), 1),
    count = n()
  ) %>%
  arrange(desc(avg_satisfaction))

cat("\n--- Morning Person or Night Owl? ---\n")
print(time_summary)

# --- STEP 4: Who starts it, and does it matter? ---
initiator_summary <- df %>%
  group_by(initiator) %>%
  summarise(
    avg_satisfaction = round(mean(satisfaction_rating), 1),
    avg_duration = round(mean(duration_minutes)),
    count = n()
  )

cat("\n--- Who Initiates (and does it matter?) ---\n")
print(initiator_summary)

# --- STEP 5: What activities correlate with satisfaction? ---
activities_long <- df %>%
  separate_rows(activities, sep = ";") %>%
  group_by(activities) %>%
  summarise(
    avg_satisfaction = round(mean(satisfaction_rating), 1),
    times_logged = n()
  ) %>%
  arrange(desc(avg_satisfaction))

cat("\n--- Your Satisfaction by Activity ---\n")
print(activities_long)

# --- STEP 6: Does duration actually matter? ---
cor_duration <- cor(df$duration_minutes, df$satisfaction_rating)
cat("\n--- Duration vs Satisfaction Correlation ---\n")
cat("Correlation:", round(cor_duration, 2), "\n")
if (cor_duration > 0.5) {
  cat("Longer sessions tend to be more satisfying for you.\n")
} else if (cor_duration < -0.5) {
  cat("Interestingly, shorter sessions tend to rate higher.\n")
} else {
  cat("Duration doesn't strongly predict your satisfaction. It's not about the clock.\n")
}

# --- STEP 7: Your cycle, your data ---
if (any(!is.na(df$cycle_day))) {
  cycle_summary <- df %>%
    filter(!is.na(cycle_day)) %>%
    mutate(cycle_phase = case_when(
      cycle_day <= 5  ~ "menstrual",
      cycle_day <= 13 ~ "follicular",
      cycle_day <= 16 ~ "ovulatory",
      cycle_day <= 28 ~ "luteal",
      TRUE ~ "other"
    )) %>%
    group_by(cycle_phase) %>%
    summarise(
      avg_satisfaction = round(mean(satisfaction_rating), 1),
      count = n()
    ) %>%
    arrange(desc(avg_satisfaction))

  cat("\n--- Satisfaction by Cycle Phase ---\n")
  print(cycle_summary)
}

# --- STEP 8: Make it pretty ---
# Satisfaction by day of week
ggplot(df, aes(x = fct_relevel(day_of_week, 
    "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"),
    y = satisfaction_rating)) +
  geom_point(size = 3, color = "#d4768a") +
  geom_smooth(method = "loess", se = FALSE, color = "#8a4d5e", group = 1) +
  labs(
    title = "When Does It Hit Different?",
    subtitle = "Satisfaction rating by day of week",
    x = "", y = "Satisfaction (1-10)",
    caption = "sweetnulls.com | your data, your pleasure"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold", size = 14))

ggsave("satisfaction_by_day.png", width = 8, height = 5)

# Duration vs satisfaction scatter
ggplot(df, aes(x = duration_minutes, y = satisfaction_rating)) +
  geom_point(size = 3, color = "#d4768a") +
  geom_smooth(method = "lm", se = TRUE, color = "#8a4d5e") +
  labs(
    title = "Is Longer Actually Better?",
    subtitle = paste0("Correlation: ", round(cor_duration, 2)),
    x = "Duration (minutes)", y = "Satisfaction (1-10)",
    caption = "sweetnulls.com | your data, your pleasure"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold", size = 14))

ggsave("duration_vs_satisfaction.png", width = 8, height = 5)

cat("\n\nDone! Check your folder for charts.\n")
cat("Now go make more data. For science.\n")
