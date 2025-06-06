import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
data = pd.read_csv('data/validator_stats.csv')

COST_PER_VALIDATOR = 5079  # USD per month
COST_PER_SOL = COST_PER_VALIDATOR / 1230  # $4.13 per SOL per month (baseline)

def plot_stake_probability_distribution(data):
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Stake Range', y='Probability', data=data, color='skyblue', edgecolor='black')
    plt.title('Stake Probability Distribution (Validators by Stake Range)')
    plt.xlabel('Stake Range (SOL)')
    plt.ylabel('Probability')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('stake_probability_distribution.png')
    plt.show()

def plot_stake_vs_validators_imbalance(data):
    # Calculate fraction of total staked SOL per range
    data['Fraction_Staked'] = data['Total Staked'] / data['Total Staked'].sum()
    # Prepare data for grouped bar plot
    plot_df = pd.DataFrame({
        'Stake Range': data['Stake Range'],
        'Fraction of Validators': data['Probability'],
        'Fraction of Total Staked': data['Fraction_Staked']
    })
    plot_df = plot_df.melt(id_vars='Stake Range', var_name='Metric', value_name='Fraction')
    plt.figure(figsize=(14, 7))
    sns.barplot(x='Stake Range', y='Fraction', hue='Metric', data=plot_df)
    plt.title('Imbalance: Fraction of Validators vs Fraction of Total Staked SOL')
    plt.xlabel('Stake Range (SOL)')
    plt.ylabel('Fraction of Total')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Metric')
    plt.tight_layout()
    plt.savefig('stake_vs_validators_imbalance.png')
    plt.show()

def plot_validators_vs_stake(data):
    # Prepare data for grouped bar plot
    plot_df = pd.DataFrame({
        'Stake Range': data['Stake Range'],
        'Unique Validators': data['Number of Validators'],
        'Total Staked SOL': data['Total Staked']
    })
    plot_df = plot_df.melt(id_vars='Stake Range', var_name='Metric', value_name='Value')
    plt.figure(figsize=(14, 7))
    sns.barplot(x='Stake Range', y='Value', hue='Metric', data=plot_df)
    plt.title('Unique Validators vs Total Staked SOL per Stake Range')
    plt.xlabel('Stake Range (SOL)')
    plt.ylabel('Count / SOL')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Metric')
    plt.tight_layout()
    plt.savefig('validators_vs_stake.png')
    plt.show()

def plot_cost_per_sol_staked(data):
    # Avoid division by zero
    cost_per_sol = COST_PER_VALIDATOR / data['Median Stake'].replace(0, np.nan)
    plt.figure(figsize=(14, 7))
    sns.barplot(x=data['Stake Range'], y=cost_per_sol, color='salmon', edgecolor='black')
    plt.title('Cost per SOL Staked by Stake Range')
    plt.xlabel('Stake Range (SOL)')
    plt.ylabel('Cost per SOL Staked ($/SOL/month)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('cost_per_sol_staked.png')
    plt.show()

def plot_total_cost_per_bucket(data, cost_per_sol=COST_PER_SOL):
    total_cost = data['Total Staked'] * cost_per_sol
    plt.figure(figsize=(14, 7))
    sns.barplot(x=data['Stake Range'], y=total_cost, color='mediumseagreen', edgecolor='black')
    plt.title(f'Total Cost per Bucket (at ${cost_per_sol:.2f} per SOL per month)')
    plt.xlabel('Stake Range (SOL)')
    plt.ylabel('Total Cost per Bucket ($/month)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('total_cost_per_bucket.png')
    plt.show()

def plot_continuous_cost_vs_stake(cost_per_sol=COST_PER_SOL, max_stake=1000000):
    # max_stake can be set to the max in your data or higher for visualization
    sol_staked = np.linspace(0, max_stake, 500)
    total_cost = sol_staked * cost_per_sol
    plt.figure(figsize=(12, 6))
    plt.plot(sol_staked, total_cost, color='blue', linewidth=2)
    plt.title(f'Continuous Total Cost vs SOL Staked (at ${cost_per_sol:.2f} per SOL per month)')
    plt.xlabel('SOL Staked')
    plt.ylabel('Total Cost ($/month)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('continuous_cost_vs_stake.png')
    plt.show()

def main():
    print('Generating distributions...')
    plot_stake_probability_distribution(data)
    plot_stake_vs_validators_imbalance(data)
    plot_validators_vs_stake(data)
    plot_cost_per_sol_staked(data)
    plot_total_cost_per_bucket(data)

if __name__ == '__main__':
    main() 