import matplotlib.pyplot as plt
import numpy as np

# Define the labels and categories for each dimension
labels = np.array(
    [
        "Information Firehose",  # High = 3
        "Mental Bandwidth",  # High = 3
        "Belief about Alpha",  # Believe Active search = 3
        "Portfolio Construction",  # Major, Alts, meme = 3
        "Research Focus",  # Each = 1 pt
        "Attitude towards Fundamentals",  # Part of my strategy = 3
        "Time Horizon",  # Long-term = 3
        "Approach towards Twitter",  # Abstain = 1, Lurker = 2, Reluctant = 3, Enjoyeer = 4
        "Market Cycles",  # Does not = 1, Does = 2
        "Investing Logistics",  # High pain = 3
        "Social Style",  # Only me = 1, Close Friends = 2
    ]
)
num_vars = len(labels)

# Define the values for each persona (scale of 1 to 3 for each dimension)
# Momentum Maven
momentum_maven = np.array([3, 3, 3, 3, 2, 1, 2, 3, 2, 1, 2])
# Casual Chloe
diligence_doer = np.array([1, 1, 2, 2, 2, 3, 3, 1, 1, 3, 1])
# Speculative Sam
opportunistic_owner = np.array([2, 1, 1, 2, 1, 1, 3, 2, 2, 2, 2])
# Diligent Dana
strategic_speculator = np.array([3, 2, 2, 3, 2, 2, 2, 3, 1, 1, 1])

# Compute angle for each axis
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# The plot is circular, so we need to "complete the loop" and append the start to the end.
momentum_maven = np.concatenate((momentum_maven, [momentum_maven[0]]))
diligence_doer = np.concatenate((diligence_doer, [diligence_doer[0]]))
opportunistic_owner = np.concatenate((opportunistic_owner, [opportunistic_owner[0]]))
strategic_speculator = np.concatenate((strategic_speculator, [strategic_speculator[0]]))
angles += angles[:1]

# Plot
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.fill(angles, momentum_maven, color="red", alpha=0.25)
ax.fill(angles, diligence_doer, color="blue", alpha=0.25)
ax.fill(angles, opportunistic_owner, color="green", alpha=0.25)
ax.fill(angles, strategic_speculator, color="yellow", alpha=0.25)

# Add labels to the plot
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

# Add legend and title
plt.title("Crypto Investor Personas Spider Chart", size=20, color="black", y=1.1)
plt.legend(
    ["Momentum Maven", "Diligence Doer", "Opportunistic Owner", "Strategic Speculator"],
    loc="upper right",
    bbox_to_anchor=(0.1, 0.1),
)

plt.show()
