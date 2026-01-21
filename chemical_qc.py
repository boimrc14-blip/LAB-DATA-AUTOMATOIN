import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ====================
# CHEMICAL QC DASHBOARD
# ====================

print("\n" + "="*60)
print("CHEMICAL QUALITY CONTROL DASHBOARD")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("="*60)

# 1. CREATE SAMPLE CHEMICAL DATA
np.random.seed(42)  # For reproducible results

samples = 20
data = {
    'Batch': [f'B{str(i+1).zfill(3)}' for i in range(samples)],
    'pH': np.random.uniform(6.5, 7.5, samples).round(2),
    'Viscosity_cSt': np.random.uniform(110, 140, samples).round(1),
    'Density_gmL': np.random.uniform(0.85, 0.95, samples).round(3),
    'Impurity_ppm': np.random.uniform(0, 50, samples).round(1),
    'Temperature_C': np.random.uniform(22, 28, samples).round(1)
}

# Add QC Status based on criteria
df = pd.DataFrame(data)
df['QC_Status'] = np.where(
    (df['pH'] >= 6.8) & (df['pH'] <= 7.3) & 
    (df['Viscosity_cSt'] >= 115) & (df['Viscosity_cSt'] <= 135) &
    (df['Impurity_ppm'] <= 30),
    'PASS', 'FAIL'
)

# 2. DISPLAY DATA
print("\n📊 FIRST 10 SAMPLES:")
print(df.head(10).to_string(index=False))

# 3. BASIC STATISTICS
print("\n📈 QC STATISTICS:")
print(f"Total Samples: {len(df)}")
print(f"Passed: {(df['QC_Status'] == 'PASS').sum()} ({(df['QC_Status'] == 'PASS').sum()/len(df)*100:.1f}%)")
print(f"Failed: {(df['QC_Status'] == 'FAIL').sum()} ({(df['QC_Status'] == 'FAIL').sum()/len(df)*100:.1f}%)")

print("\n🧪 PARAMETER RANGES:")
for col in ['pH', 'Viscosity_cSt', 'Density_gmL', 'Impurity_ppm']:
    print(f"{col:15s}: Min={df[col].min():.2f}, Max={df[col].max():.2f}, Avg={df[col].mean():.2f}")

# 4. VISUALIZATION
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Chemical Quality Control Dashboard', fontsize=16, fontweight='bold')

# Plot 1: pH Distribution
axes[0,0].hist(df['pH'], bins=8, edgecolor='black', alpha=0.7, color='skyblue')
axes[0,0].axvline(x=7.0, color='red', linestyle='--', label='Target pH')
axes[0,0].set_title('pH Distribution')
axes[0,0].set_xlabel('pH')
axes[0,0].set_ylabel('Frequency')
axes[0,0].legend()
axes[0,0].grid(True, alpha=0.3)

# Plot 2: Viscosity vs Density
colors = ['green' if s == 'PASS' else 'red' for s in df['QC_Status']]
scatter = axes[0,1].scatter(df['Viscosity_cSt'], df['Density_gmL'], 
                           c=colors, s=80, alpha=0.7, edgecolors='black')
axes[0,1].set_title('Viscosity vs Density')
axes[0,1].set_xlabel('Viscosity (cSt)')
axes[0,1].set_ylabel('Density (g/mL)')
axes[0,1].grid(True, alpha=0.3)

# Plot 3: Impurity Levels
axes[0,2].bar(df['Batch'], df['Impurity_ppm'], color=colors, edgecolor='black')
axes[0,2].axhline(y=30, color='red', linestyle='--', label='Max Limit (30 ppm)')
axes[0,2].set_title('Impurity Levels by Batch')
axes[0,2].set_xlabel('Batch ID')
axes[0,2].set_ylabel('Impurity (ppm)')
axes[0,2].tick_params(axis='x', rotation=45)
axes[0,2].legend()
axes[0,2].grid(True, alpha=0.3)

# Plot 4: QC Status Pie Chart
status_counts = df['QC_Status'].value_counts()
axes[1,0].pie(status_counts.values, labels=status_counts.index, 
             autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'],
             startangle=90, explode=(0.05, 0))
axes[1,0].set_title('QC Status Distribution')

# Plot 5: Temperature Trend
axes[1,1].plot(df['Batch'], df['Temperature_C'], marker='o', linewidth=2, color='orange')
axes[1,1].fill_between(df['Batch'], df['Temperature_C'], alpha=0.3, color='orange')
axes[1,1].set_title('Temperature Trend')
axes[1,1].set_xlabel('Batch ID')
axes[1,1].set_ylabel('Temperature (°C)')
axes[1,1].tick_params(axis='x', rotation=45)
axes[1,1].grid(True, alpha=0.3)

# Plot 6: Parameter Correlation
corr_data = df[['pH', 'Viscosity_cSt', 'Density_gmL', 'Impurity_ppm']]
corr_matrix = corr_data.corr()
im = axes[1,2].imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
axes[1,2].set_title('Parameter Correlation Matrix')
axes[1,2].set_xticks(range(len(corr_matrix.columns)))
axes[1,2].set_yticks(range(len(corr_matrix.columns)))
axes[1,2].set_xticklabels(corr_matrix.columns, rotation=45)
axes[1,2].set_yticklabels(corr_matrix.columns)
plt.colorbar(im, ax=axes[1,2])

plt.tight_layout()
plt.savefig('chemical_qc_dashboard.png', dpi=150, bbox_inches='tight')
print(f"\n✅ Dashboard saved as 'chemical_qc_dashboard.png'")

# 5. EXPORT TO EXCEL
with pd.ExcelWriter('chemical_qc_report.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Raw Data', index=False)
    
    # Summary sheet
    summary_data = {
        'Metric': ['Total Batches', 'Pass Rate', 'Fail Rate', 
                   'Average pH', 'Average Viscosity', 'Average Impurity',
                   'Analysis Date'],
        'Value': [len(df), 
                  f"{(df['QC_Status'] == 'PASS').sum()/len(df)*100:.1f}%",
                  f"{(df['QC_Status'] == 'FAIL').sum()/len(df)*100:.1f}%",
                  f"{df['pH'].mean():.2f}",
                  f"{df['Viscosity_cSt'].mean():.1f} cSt",
                  f"{df['Impurity_ppm'].mean():.1f} ppm",
                  datetime.now().strftime('%Y-%m-%d %H:%M')]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    # Statistics sheet
    stats_df = df[['pH', 'Viscosity_cSt', 'Density_gmL', 'Impurity_ppm']].describe()
    stats_df.to_excel(writer, sheet_name='Statistics')

print("✅ Excel report saved as 'chemical_qc_report.xlsx'")

print("\n" + "="*60)
print("ANALYSIS COMPLETE! 🎉")
print("="*60)
