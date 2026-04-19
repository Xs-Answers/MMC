import matplotlib.pyplot as plt
import numpy as np

def generate_trajectory():
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("三位高风险病患个体化干预方案执行轨迹图", fontsize=18, y=1.05)
    
    months = np.arange(1, 7)
    
    score1 = [85, 76, 68, 62, 57, 52] 
    cost1 = [800, 750, 680, 680, 500, 500] 
    acc_cost1 = np.cumsum(cost1)
    
    score2 = [72, 66, 62, 58, 55, 50] 
    cost2 = [600, 600, 550, 480, 480, 450]
    acc_cost2 = np.cumsum(cost2)
    
    score3 = [65, 62, 59, 56, 53, 49]
    cost3 = [500, 480, 480, 450, 400, 400]
    acc_cost3 = np.cumsum(cost3)
    
    scores = [score1, score2, score3]
    acc_costs = [acc_cost1, acc_cost2, acc_cost3]
    initial_scores = [85, 72, 65]
    
    for i in range(3):
        ax1 = axes[i]
        
        ax1.axhspan(80, 100, facecolor="#ffcccc", alpha=0.3, label="三级调理")
        ax1.axhspan(60, 80, facecolor="#ffffcc", alpha=0.3, label="二级调理")
        ax1.axhspan(40, 60, facecolor="#ccffcc", alpha=0.3, label="一级调理")
        
        target_score = initial_scores[i] * 0.90
        ax1.axhline(target_score, color="red", linestyle="--", linewidth=1.5, label="10%降分红线")
        
        ax1.plot(months, scores[i], "o-", color="#2c3e50", linewidth=2.5, markersize=8, label="痰湿积分")
        ax1.set_xlabel("干预时间 (月)", fontsize=12)
        ax1.set_ylabel("痰湿积分", fontsize=12, color="#2c3e50")
        ax1.set_ylim(35, 95)
        ax1.tick_params(axis="y", labelcolor="#2c3e50")
        
        ax2 = ax1.twinx()
        ax2.bar(months, acc_costs[i], color="#3498db", alpha=0.5, width=0.5, label="累计干预成本 (元)")
        ax2.set_ylabel("累计成本 (元)", fontsize=12, color="#2980b9")
        ax2.set_ylim(0, 5000)
        ax2.tick_params(axis="y", labelcolor="#2980b9")
        
        ax1.set_title(f"样本 {i+1} (初始分: {initial_scores[i]})", fontsize=14)
        
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=9)
        
    plt.tight_layout()
    plt.savefig("4_1_三位病患的干预轨迹组合图.png", dpi=300, bbox_inches="tight")
    print("Trajectory plot generated.")

if __name__ == "__main__":
    generate_trajectory()