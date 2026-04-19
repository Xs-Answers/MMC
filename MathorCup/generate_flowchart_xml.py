import xml.etree.ElementTree as ET

def create_drawio_xml():
    root = ET.Element("mxfile", host="Electron", modified="2023-10-25T00:00:00.000Z", agent="Mozilla/5.0", version="21.5.0", type="device")
    diagram = ET.SubElement(root, "diagram", id="diagram1", name="Page-1")
    model = ET.SubElement(diagram, "mxGraphModel", dx="1000", dy="800", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1000", pageHeight="1000", math="0", shadow="0")
    root_cell = ET.SubElement(model, "root")
    
    ET.SubElement(root_cell, "mxCell", id="0")
    ET.SubElement(root_cell, "mxCell", id="1", parent="0")

    def add_node(id_str, text, x, y, w, h, style):
        cell = ET.SubElement(root_cell, "mxCell", id=id_str, value=text, style=style, vertex="1", parent="1")
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"})
    
    def add_edge(id_str, source, target, style, exitX=None, exitY=None, entryX=None, entryY=None):
        style_full = f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;{style}"
        if exitX is not None: style_full += f"exitX={exitX};exitY={exitY};"
        if entryX is not None: style_full += f"entryX={entryX};entryY={entryY};"
        cell = ET.SubElement(root_cell, "mxCell", id=id_str, style=style_full, edge="1", parent="1", source=source, target=target)
        ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})

    # Common Styles
    base_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;"
    title_style = "text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1;"
    desc_style = "text;html=1;align=left;verticalAlign=top;resizable=0;points=[];autosize=0;strokeColor=none;fillColor=none;fontSize=12;spacing=4;spacingTop=6;spacingLeft=4;"
    
    green_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#666666;fillColor=#92d050;fontColor=#000000;fontStyle=0;"
    yellow_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#666666;fillColor=#ffc000;fontColor=#000000;fontStyle=0;"
    red_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#666666;fillColor=#c00000;fontColor=#ffffff;fontStyle=0;"
    header_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#666666;fillColor=#f2f2f2;fontColor=#000000;fontStyle=1;align=center;verticalAlign=middle;"
    row_header_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#666666;fillColor=#ffffff;fontColor=#000000;align=center;verticalAlign=middle;"
    
    # 1. Top Flowchart nodes
    add_node("title", "中年人群高血脂症与痰湿及干预综合预警评估流程图", 300, 20, 400, 30, title_style)
    add_node("n_start", "初筛中老年评估及干预体检总人群", 400, 70, 200, 40, base_style)
    
    add_node("d1", "是否发生过相关的危急重症？\n（极严重的冠病、不可逆的躯体衰败）", 380, 140, 240, 60, "rhombus;whiteSpace=wrap;html=1;strokeColor=#000000;")
    
    # Add Edge from Start to d1
    add_edge("e1", "n_start", "d1", "")
    
    # Branches
    add_node("n_secondary_label", "是", 290, 140, 40, 20, "text;html=1;align=center;")
    add_node("n_primary_label", "否", 670, 140, 40, 20, "text;html=1;align=center;")

    add_node("n_secondary", "二级强化预防流程", 260, 210, 160, 40, base_style)
    add_node("n_primary", "综合等级评估与日常干预", 580, 210, 160, 40, base_style)
    
    add_edge("e2", "d1", "n_secondary", "", exitX=0, exitY=0.5, entryX=0.5, entryY=0)
    add_edge("e3", "d1", "n_primary", "", exitX=1, exitY=0.5, entryX=0.5, entryY=0)
    
    # Left box
    sec_box_text = ("符合下列任意条件者，可直接划为极高危干预人群快速跟进：\n\n"
                    "① 已确诊且无法扭转的相关原发代谢失序重症\n"
                    "② 重度痰湿（积分≥95）合并日常全功能活动瘫痪\n"
                    "③ 其他超出基本医疗调整干预容忍限度的病状")
    add_node("n_sec_box", sec_box_text, 140, 310, 330, 90, "shape=rectangle;whiteSpace=wrap;html=1;align=left;spacingLeft=10;spacingTop=10;fontStyle=0")
    add_edge("e4", "n_secondary", "n_sec_box", "endArrow=classic;")
    
    # Right box
    add_node("n_prim_box", "不符合左侧直出条件者，进入下表综合多维度评价以细化至 低/中/高 危险层级", 520, 310, 280, 40, "shape=rectangle;whiteSpace=wrap;html=1;align=center;fontStyle=0")
    add_edge("e5", "n_primary", "n_prim_box", "endArrow=classic;")
    
    # Draw arrow down to the matrix
    add_node("p_matrix_anchor", "", 660, 420, 0, 0, "text;html=1;")
    add_edge("e6", "n_prim_box", "p_matrix_anchor", "endArrow=classic;", exitX=0.5, exitY=1, entryX=0.5, entryY=0)
    
    # 2. Risk Matrix Table (x_start = 140, y_start = 420)
    Y_M = 420
    
    # Table main grouping box (visual wrapper)
    add_node("m_wrapper", "", 140, Y_M+30, 720, 310, "rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=2;")
    
    # Headers
    add_node("m_h1", "痰湿体质积水平分层 (分)", 380, Y_M, 480, 30, header_style)
    add_node("m_h2_1", "核心血脂状态\n分层", 140, Y_M+30, 100, 40, header_style)
    add_node("m_h2_2", "日常活动受限评分\n(ADL+IADL总量)", 240, Y_M+30, 140, 40, header_style)
    add_node("m_h2_3", "无或轻度痰湿分\n(0≤积分<60)", 380, Y_M+30, 160, 40, header_style)
    add_node("m_h2_4", "中度痰湿失常\n(60≤积分<80)", 540, Y_M+30, 160, 40, header_style)
    add_node("m_h2_5", "重度痰湿特征\n(80≤积分≤100)", 700, Y_M+30, 160, 40, header_style)
    
    # Left headers matching ASCVD layout (span rows)
    add_node("m_row1_1", "未诊断高血脂\n且核心各项\n指标正常区", 140, Y_M+70, 100, 120, row_header_style + "fillColor=#f9fbf8;")
    add_node("m_row2_1", "已确诊高血脂\n或某项核心指标\n显著异常", 140, Y_M+190, 100, 120, row_header_style + "fillColor=#fffdf8;")
    
    # Activity score headers
    acts = ["活动能力良好\n(活动量≥60)", "轻度活动受限\n(40≤活动量<60)", "显著活动受限\n(活动量<40)"]
    for i in range(3):
        add_node(f"act1_{i}", acts[i], 240, Y_M+70 + i*40, 140, 40, row_header_style)
        add_node(f"act2_{i}", acts[i], 240, Y_M+190 + i*40, 140, 40, row_header_style)
        
    # Cells (3x6 matrix)
    # Group 1: Lipid Normal
    data_g1 = [
        [green_style, "低危 (<5%)", green_style, "低危 (<5%)", green_style, "低危 (<5%)"],
        [green_style, "低危 (<5%)", green_style, "低危 (<5%)", yellow_style, "中度/中危 (5%~9%)"],
        [yellow_style, "中度/中危 (5%~9%)", red_style, "高度预警 (≥10%)", red_style, "高度预警 (≥10%)"]
    ]
    # Group 2: Lipid Abnormal
    data_g2 = [
        [yellow_style, "中度/中危 (5%~9%)", yellow_style, "中度/中危 (5%~9%)", red_style, "高度预警 (≥10%)"],
        [yellow_style, "中度/中危 (5%~9%)", red_style, "高度预警 (≥10%)", red_style, "高度预警 (≥10%)"],
        [red_style, "高度预警 (≥10%)", red_style, "高度预警 (≥10%)", red_style, "高度预警 (≥10%)"]
    ]
    
    # Render Group 1 Cells
    y_curr = Y_M + 70
    for r, r_data in enumerate(data_g1):
        add_node(f"c1_{r}_0", r_data[1], 380, y_curr, 160, 40, r_data[0])
        add_node(f"c1_{r}_1", r_data[3], 540, y_curr, 160, 40, r_data[2])
        add_node(f"c1_{r}_2", r_data[5], 700, y_curr, 160, 40, r_data[4])
        y_curr += 40
        
    # Render Group 2 Cells
    y_curr = Y_M + 190
    for r, r_data in enumerate(data_g2):
        add_node(f"c2_{r}_0", r_data[1], 380, y_curr, 160, 40, r_data[0])
        add_node(f"c2_{r}_1", r_data[3], 540, y_curr, 160, 40, r_data[2])
        add_node(f"c2_{r}_2", r_data[5], 700, y_curr, 160, 40, r_data[4])
        y_curr += 40
        
    # 3. Bottom Annotations
    Y_A = Y_M + 360
    anno = ("<b>图注及模型参数判定说明：</b><br>"
            "1. <b>高血脂初筛与指标截断</b>：参照《赛题》诊断指南及血指标健康预警阈值。凡满足诊断模型正向激活，或任意核心生化指标（如：TG/TC 等偏态分布尾部超越截断极值）异动者归左层。<br>"
            "2. <b>特征边界量化界定与分类矩阵说明 (非线性耦合特征预警)</b>：此量化分层表格的界段直接映射了决策树 Gini 重要度评估结构 [2] 以及互信息（MI）对非线性关系的放大效应 [4]；具体阈值如：高危级对应于“血脂指标异常且痰湿积分≥80”及隐匿恶化物“血脂无异常但痰湿积分≥60且活动能力评分低于40分”等联合规则，精确对标多指标干预成本模型。<br>"
            "3. <b>对调理模型（第三问）的触发机制</b>：高位（红）及中位（黄）将触发 6 个月跟踪的中期干预流程分配算法，进而进入成本与效用的最优寻梯。")
    add_node("m_anno", anno, 140, Y_A, 720, 80, desc_style)

    xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
    with open("基于风险分层的预警决策模型全图.drawio", "w", encoding="utf-8") as f:
        # replace angle brackets inside tags from our html descriptions
        xml_str = xml_str.replace("&amp;lt;", "&lt;").replace("&amp;gt;", "&gt;")
        f.write(xml_str)
        
create_drawio_xml()
