import xml.etree.ElementTree as ET

def create_drawio_xml():
    root = ET.Element("mxfile", host="Electron", modified="2023-10-25T00:00:00.000Z", agent="Mozilla/5.0", version="21.5.0", type="device")
    diagram = ET.SubElement(root, "diagram", id="diagram1", name="Page-1")
    model = ET.SubElement(diagram, "mxGraphModel", dx="900", dy="900", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="827", pageHeight="1169", math="0", shadow="0")
    root_cell = ET.SubElement(model, "root")
    
    ET.SubElement(root_cell, "mxCell", id="0")
    ET.SubElement(root_cell, "mxCell", id="1", parent="0")

    def add_node(id_str, text, x, y, w, h, style):
        cell = ET.SubElement(root_cell, "mxCell", id=id_str, value=text, style=style, vertex="1", parent="1")
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"})
    
    def add_edge(id_str, source, target, style, exitX=None, exitY=None, entryX=None, entryY=None):
        style_full = f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1;fontColor=#000000;strokeColor=#000000;{style}"
        if exitX is not None: style_full += f"exitX={exitX};exitY={exitY};"
        if entryX is not None: style_full += f"entryX={entryX};entryY={entryY};"
        cell = ET.SubElement(root_cell, "mxCell", id=id_str, style=style_full, edge="1", parent="1", source=source, target=target)
        ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})

    # Styles mimicking the ORIGINAL PNG colors and square corners
    title_style = "text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=0;strokeColor=none;fillColor=none;fontSize=18;fontStyle=1;fontColor=#000000;"
    start_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;fontColor=#000000;fontStyle=1;fontSize=13;strokeWidth=1;"
    diamond_style = "rhombus;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;fontColor=#000000;fontStyle=1;fontSize=11;strokeWidth=1;"
    left_box_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;fontColor=#000000;fontStyle=0;fontSize=11;align=left;spacingLeft=10;spacingTop=6;strokeWidth=1;"
    right_box_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;fontColor=#000000;fontStyle=1;fontSize=12;align=center;strokeWidth=1;"
    
    matrix_title_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#f2f2f2;fontColor=#000000;fontStyle=1;fontSize=13;strokeWidth=1;"
    header_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#666666;fillColor=#f2f2f2;fontColor=#000000;fontStyle=1;fontSize=11;strokeWidth=1;align=center;verticalAlign=middle;"
    row_h_style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#666666;fillColor=#ffffff;fontColor=#000000;fontStyle=0;fontSize=11;strokeWidth=1;align=center;verticalAlign=middle;"
    
    g_col = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#666666;fillColor=#92d050;fontColor=#000000;fontStyle=0;fontSize=11;strokeWidth=1;"
    y_col = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#666666;fillColor=#ffc000;fontColor=#000000;fontStyle=0;fontSize=11;strokeWidth=1;"
    r_col = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#666666;fillColor=#c00000;fontColor=#ffffff;fontStyle=0;fontSize=11;strokeWidth=1;"

    desc_style = "text;html=1;strokeColor=none;fillColor=none;fontColor=#000000;fontStyle=0;fontSize=12;align=left;spacingLeft=10;spacingTop=6;"

    # Layout coordinates (width=800 center=400)
    add_node("title", "中年人群高血脂症与痰湿体质综合风险评估流程图", 100, 20, 600, 40, title_style)
    
    add_node("n_start", "初筛中老年评估及干预体检总人群", 280, 80, 240, 40, start_style)
    
    add_node("d1", "是否发生过相关的危急重症？\n（极严重的冠病、不可逆的躯体衰败）", 260, 150, 280, 70, diamond_style)
    add_edge("e1", "n_start", "d1", "")
    
    # Left Branch
    add_node("lbl_yes", "是", 160, 160, 40, 20, "text;html=1;align=center;fontColor=#000000;fontStyle=0;fontSize=13;")
    add_node("n_left", "符合下列任意条件者，可直接划为极高危干预人群快速跟进：<br><br>① 已确诊且无法扭转的相关原发代谢失序重症<br>② 重度痰湿（积分≥95）合并日常全功能活动瘫痪<br>③ 其他超出基本医疗调整干预容忍限度的病状", 
             40, 260, 280, 120, left_box_style)
    add_edge("e2", "d1", "n_left", "", exitX=0, exitY=0.5, entryX=0.5, entryY=0)
    
    # Right Branch
    add_node("lbl_no", "否", 600, 160, 40, 20, "text;html=1;align=center;fontColor=#000000;fontStyle=0;fontSize=13;")
    add_node("n_right", "不符合左侧直出条件者，进入下表综合多维度评价以细化至 低/中/高 危险层级", 
             480, 260, 280, 60, right_box_style)
    add_edge("e3", "d1", "n_right", "", exitX=1, exitY=0.5, entryX=0.5, entryY=0)
    
    # Matrix Layout
    Y_M = 430
    x_c1, x_c2, x_c3, x_c4, x_c5 = 40, 140, 260, 430, 600
    w_h1, w_h2, w_col = 100, 120, 170
    h_r = 40
    
    # Arrow to Matrix
    add_edge("e4", "n_right", "m_h4", "", exitX=0.5, exitY=1, entryX=0.5, entryY=0)
    
    # Headers
    add_node("m_h0", "痰湿体质积水平分层 (分)", x_c3, Y_M-30, w_col*3, 30, matrix_title_style)
    
    add_node("m_h1", "核心血脂状态\n分层", x_c1, Y_M, w_h1, h_r, header_style + "fillColor=#f2f2f2;")
    add_node("m_h_adl", "日常活动受限评分\n(ADL+IADL总量)", x_c2, Y_M, w_h2, h_r, header_style + "fillColor=#f2f2f2;")
    add_node("m_h2", "无或轻度痰湿\n(0≤积分<60)", x_c3, Y_M, w_col, h_r, header_style)
    add_node("m_h3", "中度痰湿阶段\n(60≤积分<80)", x_c4, Y_M, w_col, h_r, header_style)
    add_node("m_h4", "重度痰湿预警\n(≥80分)", x_c5, Y_M, w_col, h_r, header_style)
    
    acts = ["活动能力良好\n(活动量≥60)", "轻度活动受限\n(40≤活动量<60)", "显著活动受限\n(活动量<40)"]
    
    def get_style_and_text(val):
        if val == 'G': return g_col, "低危 (<5%)"
        if val == 'Y': return y_col, "中度/中危 (5%~9%)"
        if val == 'R': return r_col, "高度预警 (≥10%)"
        
    matrix_data = [
        ['G', 'G', 'G'], ['G', 'G', 'Y'], ['Y', 'R', 'R'],
        ['Y', 'Y', 'R'], ['Y', 'R', 'R'], ['R', 'R', 'R'],
    ]
    
    y_curr = Y_M + h_r
    for r in range(6):
        # Row headers col 1
        if r == 0:
            add_node(f"m_r1_1", "未诊断高血脂\n且核心各项\n指标正常区", x_c1, y_curr, w_h1, h_r*3, row_h_style + "fillColor=#f9fbf8;")
        elif r == 3:
            add_node(f"m_r1_2", "已确诊高血脂\n或某项核心指标\n显著异常", x_c1, y_curr, w_h1, h_r*3, row_h_style + "fillColor=#fffdf8;")
            
        # Row headers col 2
        add_node(f"m_r2_{r}", acts[r%3], x_c2, y_curr, w_h2, h_r, row_h_style)
        
        # Data cells
        s1, t1 = get_style_and_text(matrix_data[r][0])
        s2, t2 = get_style_and_text(matrix_data[r][1])
        s3, t3 = get_style_and_text(matrix_data[r][2])
        
        add_node(f"c_{r}_1", t1, x_c3, y_curr, w_col, h_r, s1)
        add_node(f"c_{r}_2", t2, x_c4, y_curr, w_col, h_r, s2)
        add_node(f"c_{r}_3", t3, x_c5, y_curr, w_col, h_r, s3)
        
        y_curr += h_r
        
    # Footnote
    Y_F = y_curr + 30
    note_text = ("<b>图注及模型参数判定说明：</b><br>"
                 "1. <b>高血脂初筛与指标截断</b>：参照《赛题》诊断指南及血指标健康预警阈值。凡满足诊断模型正向激活，或任意核心生化指标（如：TG/TC 等偏态分布尾部超越截断极值）异动者归左层。<br>"
                 "2. <b>特征边界量化界定与分类矩阵说明 (非线性耦合特征预警)</b>：此量化分层表格的界段直接映射了决策树 Gini 重要度评估结构 [2] 以及互信息（MI）对非线性关系的放大效应 [4]；<br>"
                 "&nbsp;&nbsp;具体阈值如：高危级对应于“血脂指标异常且痰湿积分≥80”及隐匿恶化物“血脂无异常但痰湿积分≥60且活动能力评分低于40分”等联合规则，精确对标多指标干预成本模型。<br>"
                 "3. <b>对调理模型（第三问）的触发机制</b>：高位（红）及中位（黄）将触发 6 个月跟踪的中期干预流程分配算法，进而进入成本与效用的最优寻梯。")
    add_node("m_footer", note_text, 40, Y_F, 720, 110, desc_style)

    xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
    with open("5_1_预警决策流程图_原版色直角纵向排版.drawio", "w", encoding="utf-8") as f:
        xml_str = xml_str.replace("&amp;lt;", "&lt;").replace("&amp;gt;", "&gt;").replace("&amp;nbsp;", "&nbsp;")
        f.write(xml_str)
        
create_drawio_xml()