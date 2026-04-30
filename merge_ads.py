import pandas as pd

# --- Load CSV files ---
fb = pd.read_csv("01_facebook_ads.csv")
gg = pd.read_csv("02_google_ads.csv")
tt = pd.read_csv("03_tiktok_ads.csv")

# --- Inspect columns (optional debugging) ---
print("Facebook columns:", fb.columns.tolist())
print("Google columns:", gg.columns.tolist())
print("TikTok columns:", tt.columns.tolist())

# --- Standardize Facebook ---
fb = fb.rename(columns={
    'date': 'date',
    'campaign_name': 'campaign',
    'impressions': 'impressions',
    'clicks': 'clicks',
    'spend': 'spend',
    'conversions': 'conversions'
})
fb['platform'] = 'Facebook'

# --- Standardize Google ---
gg = gg.rename(columns={
    'date': 'date',
    'campaign': 'campaign',
    'impressions': 'impressions',
    'clicks': 'clicks',
    'cost': 'spend',
    'conversions': 'conversions'
})
gg['platform'] = 'Google'

# --- Standardize TikTok ---
tt = tt.rename(columns={
    'date': 'date',
    'campaign_name': 'campaign',
    'views': 'impressions',
    'clicks': 'clicks',
    'ad_cost': 'spend',
    'conversions': 'conversions'
})
tt['platform'] = 'TikTok'

# --- Keep only unified columns ---
cols = ['date', 'platform', 'campaign', 'impressions', 'clicks', 'spend', 'conversions']

fb = fb[cols]
gg = gg[cols]
tt = tt[cols]

# --- Merge datasets ---
df = pd.concat([fb, gg, tt], ignore_index=True)

# --- Clean data types ---
df['date'] = pd.to_datetime(df['date'], errors='coerce')

for col in ['impressions', 'clicks', 'spend', 'conversions']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# --- Create metrics ---
df['ctr'] = df['clicks'] / df['impressions'].replace(0, pd.NA)
df['cpc'] = df['spend'] / df['clicks'].replace(0, pd.NA)
df['cpa'] = df['spend'] / df['conversions'].replace(0, pd.NA)

# --- Final cleanup ---
df = df.fillna(0)

# --- Save unified dataset ---
df.to_csv("unified_ads.csv", index=False)

print("✅ unified_ads.csv created successfully")
print(df.head())