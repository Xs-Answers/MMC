import plotly.graph_objects as go

def generate_sankey():
    # Nodes:
    # 0 = 全体病患 (1000)
    # 1 = 血脂异常: 是 (741)
    # 2 = 血脂异常: 否 (259)
    # 3 = 痰湿积分>=80或活动能力<40 (极高危特征) (400)
    # 4 = 痰湿积分>=60或活动能力<60 (中高危特征) (350)
    # 5 = 其他 (250)
    # 6 = 高风险 (649)
    # 7 = 中风险 (292)
    # 8 = 低风险 (59)
    
    label = [
        "全体病患样本<br>(n=1000)",         # 0
        "血脂异常 (是)",                    # 1
        "血脂异常 (否)",                    # 2
        "核心特征组合A<br>(痰湿≥80/活动受阻)", # 3
        "核心特征组合B<br>(痰湿≥60/活动轻限)", # 4
        "无明显特征",                      # 5
        "高风险 (n=649)",                 # 6
        "中风险 (n=292)",                 # 7
        "低风险 (n=59)"                   # 8
    ]
    
    color_node = [
        "#808080", "#FF6B6B", "#4ECDC4", 
        "#FF9F43", "#FDCB6E", "#A4B0BE", 
        "#D63031", "#E17055", "#00B894" 
    ]
    
    # Links
    source = [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5]
    target = [1, 2, 3, 4, 5, 3, 4, 5, 6, 7, 6, 7, 8, 6, 7, 8]
    value =  [741, 259, 310, 280, 151, 90, 70, 99, 360, 40, 249, 90, 11, 40, 162, 48]
    
    color_link = [
        "rgba(255, 107, 107, 0.4)", "rgba(78, 205, 196, 0.4)",
        "rgba(255, 159, 67, 0.4)", "rgba(253, 203, 110, 0.4)", "rgba(164, 176, 190, 0.4)",
        "rgba(255, 159, 67, 0.3)", "rgba(253, 203, 110, 0.3)", "rgba(164, 176, 190, 0.3)",
        "rgba(214, 48, 49, 0.5)", "rgba(225, 112, 85, 0.4)",
        "rgba(214, 48, 49, 0.4)", "rgba(225, 112, 85, 0.5)", "rgba(0, 184, 148, 0.4)",
        "rgba(214, 48, 49, 0.3)", "rgba(225, 112, 85, 0.4)", "rgba(0, 184, 148, 0.5)"
    ]

    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 20,
          thickness = 30,
          line = dict(color = "black", width = 0.5),
          label = label,
          color = color_node,
        ),
        textfont = dict(size=14, family="SimHei"),
        link = dict(
          source = source,
          target = target,
          value = value,
          color = color_link
      ))])

    fig.update_layout(
        title_text="三级风险阈值的人群划分走向图", 
        font=dict(size=14, family="SimHei"),
        width=1000,
        height=600
    )
    
    fig.write_image("3_2_三级风险阈值的人群划分走向_Sankey.png", scale=2)
    print("Sankey diagram generated successfully.")

if __name__ == "__main__":
    generate_sankey()
