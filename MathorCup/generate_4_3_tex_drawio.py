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
        style_full = f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=1.5;fontColor=#333333;strokeColor=#333333;{style}"
        if exitX is not None: style_full += f"exitX={exitX};exitY={exitY};"
        if entryX is not None: style_full += f"entryX={entryX};entryY={entryY};"
        cell = ET.SubElement(root_cell, "mxCell", id=id_str, style=style_full, edge="1", parent="1", source=source, target=target)
        ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})

    # Styles mimicking the PNG
    title_style = "text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=0;strokeColor=none;fillColor=none;fontSize=19;fontStyle=1;fontColor=#1a1a1a;"
    start_style = "rounded=1;whiteSpace=wrap;html=1;strokeColor=#333333;fillColor=#f5f5f5;fontColor=#000000;fontStyle=1;fontSize=13;strokeWidth=1.2;"
    diamond_style = "rhombus;whiteSpace=wrap;html=1;strokeColor=#333333;fillColor=#eef5ff;fontColor=#000000;fontStyle=1;fontSize=11;strokeWidth=1.2;"
    left_box_style = "rounded=1;whiteSpace=wrap;html=1;strokeColor=#333333;fillColor=#fff0f0;fontColor=#000000;fontStyle=0;fontSize=11;align=left;spacingLeft=10;spacingTop=6;strokeWidth=1.2;"
    right_box_style = "rounded=1;whiteSpace=wrap;html=1;strokeColor=#333333;fillColor=#f0faef;fontColor=#000000;fontStyle=1;fontSize=12;align=center;strokeWidth=1.2;"
    
    matrix_title_style = "rounded=1;whiteSpace=wrap;html=1;strokeColor=#333333;fillColor=#e6f0ff;fontColor=#003380;fontStyle=1;fontSize=13;strokeWidth=1.2;"
    header_style = "rounded=1;whiteSpace=wrap;html=1;strokeColor=#333333;fillColor=#f8f9fa;fontColor=#000000;fontStyle=1;fontSize=11;strokeWidth=1.2;align=center;verticalAlign=middle;"
    row_h_style = "rounded=1;whiteSpace=wrap;html=1;strokeColor=#333333;fillColor=#ffffff;fontColor=#000000;fontStyle=0;fontSize=11;strokeWidth=1.2;align=center;verticalAlign=middle;"
    
    g_col = "rounded=1;whiteSpace=wrap;html=1;strokeColor=#333333;fillColor=#d4edd9;fontColor=#1a6b29;fontStyle=1;fontSize=11;strokeWidth=1.2;"
    y_col = "rounded=1;whiteSpace=wrap;html=1;strokeColor=#333333;fillColor=#ffebb3;fontColor=#996b00;fontStyle=1;fontSize=11;strokeWidth=1.2;"
    r_col = "rounded=1;whiteSpace=wrap;html=1;strokeColor=#333333;fillColor=#ffd1cf;fontColor=#9e1511;fontStyle=1;fontSize=11;strokeWidth=1.2;"

    desc_style = "rounded=1;whiteSpace=wrap;html=1;strokeColor=#cccccc;fillColor=#fcfcfc;fontColor=#444444;fontStyle=0;fontSize=12;align=left;spacingLeft=10;spacingTop=6;strokeWidth=1;"

    # Layout coordinates (width=800 center=400)
    add_node("title", "中年人群高血脂症与痰湿体质综合风险评估流程图", 100, 20, 600, 40, title_style)
    
    add_node("n_start", "初筛：中老年评估及干预体检总人群", 280, 80, 240, 40, start_style)
    
    add_node("d1", "是否存在较严重的合并病史？\n(如严重冠心病、缺血性脑卒中等)", 260, 150, 280, 70, diamond_style)
    add_edge("e1", "n_start", "d1", "")
    
    # Left Branch
    add_node("lbl_yes", "是", 160, 160, 40, 20, "text;html=1;align=center;fontColor=#c00000;fontStyle=1;fontSize=13;")
    add_node("n_left", "<b>【极高危干预分流】</b><br><br>符合下列任意条件者直接纳入极危预警：<br><br>① 近期心肌梗死或重大脑血管病史<br>② 极度高胆固醇 (LDL-C ≥4.9 mmol/L)<br>③ 满级重度痰湿伴日常活动完全受限<br>④ 不可逆的器官靶向病变", 
             40, 260, 280, 150, left_box_style)
    add_edge("e2", "d1", "n_left", "", exitX=0, exitY=0.5, entryX=0.5, entryY=0)
    
    # Right Branch
    add_node("lbl_no", "否", 600, 160, 40, 20, "text;html=1;align=center;fontColor=#2ca02c;fontStyle=1;fontSize=13;")
    add_node("n_right", "不符合上方左侧各项危重症指标者，\n进入常规队列，综合下列表格确立危险等级", 
             480, 260, 280, 60, right_box_style)
    add_edge("e3", "d1", "n_right", "", exitX=1, exitY=0.5, entryX=0.5, entryY=0)
    
    # Pre-Matrix Title
    add_node("n_mat_title", "多维特征交叉预警与发病层级评估矩阵", 40, 430, 720, 30, matrix_title_style)
    add_edge("e4", "n_right", "n_mat_title", "", exitX=0.5, exitY=1, entryX=0.79, entryY=0)
    
    # Matrix Layout
    Y_M = 470
    x_c1, x_c2, x_c3, x_c4, x_c5 = 40, 140, 260, 430, 600
    w_h1, w_h2, w_col = 100, 120, 170
    h_r = 40
    
    # Headers
    add_node("m_h1", "核心血脂状态 | 日常活动受限量级", x_c1, Y_M, w_h1+w_h2, h_r, header_style + "fillColor=#f8f9fa;")
    add_node("m_h2", "无或轻度痰湿\n(0≤积分<60)", x_c3, Y_M, w_col, h_r, header_style)
    add_node("m_h3", "中度痰湿阶段\n(60≤积分<80)", x_c4, Y_M, w_col, h_r, header_style)
    add_node("m_h4", "重度痰湿预警\n(≥80分)", x_c5, Y_M, w_col, h_r, header_style)
    
    acts = ["活动能力良好\n(分数≥60)", "轻度活动受限\n(40≤分数<60)", "显著活动受限\n(分数<40)"]
    
    def get_style_and_text(val):
        if val == 'G': return g_col, "低危人群 (<5%)"
        if val == 'Y': return y_col, "中危界定 (5-9%)"
        if val == 'R': return r_col, "高危突变 (≥10%)"
        
    matrix_data = [
        ['G', 'G', 'G'], ['G', 'G', 'Y'], ['Y', 'R', 'R'],
        ['Y', 'Y', 'R'], ['Y', 'R', 'R'], ['R', 'R', 'R'],
    ]
    
    y_curr = Y_M + h_r
    for r in range(6):
        # Row headers col 1
        if r == 0:
            add_node(f"m_r1_1", "未确诊高血脂\n且各项生化指标\n无异常溢出", x_c1, y_curr, w_h1, h_r*3, row_h_style)
        elif r == 3:
            add_node(f"m_r1_2", "已确诊高血脂\n或某项靶向指标\n发生显著异常", x_c1, y_curr, w_h1, h_r*3, row_h_style + "fillColor=#fcfcfc;")
            
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
    note_text = ("<b>【 理论融合说明 】</b><br>"
                 "• <b>血脂异常识别阻断</b>：遵循赛题核心指标与预警诊断要求，任意单项生化边界极端异常，无条件降级入下半层警戒组。<br>"
                 "• <b>特征耦合非线性预设</b>：矩阵划界高度契合前述随机森林(Random Forest)的 Gini 权重排序及互信息(MI)非线性评估结论。<br>"
                 "&nbsp;&nbsp;例如：“重期痰湿伴严重活动障碍”即使处于血脂正常组，仍表现出高位(红色)共线性致病倾向，实现无缝隐匿预警。<br>"
                 "• <b>与运筹模型耦合机制</b>：红黄绿危阶直通下文最优化干预模型，作为划定干预强度、限制月度成本(≤2000元)的核心参量。")
    add_node("m_footer", note_text, 40, Y_F, 720, 110, desc_style)

    xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
    with open("5_1_高质预警决策流程图_Tex纵向排版.drawio", "w", encoding="utf-8") as f:
        xml_str = xml_str.replace("&amp;lt;", "&lt;").replace("&amp;gt;", "&gt;").replace("&amp;nbsp;", "&nbsp;")
        f.write(xml_str)
        
create_drawio_xml()