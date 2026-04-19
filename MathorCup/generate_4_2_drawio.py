def generate_drawio():
    xml_template = """<mxfile host="Electron" modified="2024-01-01T12:00:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="heatmap" name="速查图">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1000" pageHeight="800" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- 标题 -->
        <mxCell id="title" value="&lt;b&gt;&lt;font style=&quot;font-size: 20px;&quot;&gt;患者特征匹配干预策略速查热力矩阵&lt;/font&gt;&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="300" y="40" width="400" height="40" as="geometry" />
        </mxCell>

        <!-- X轴和Y轴标签 -->
        <mxCell id="xlabel_title" value="&lt;b&gt;活动总分评价区间&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="400" y="650" width="200" height="30" as="geometry" />
        </mxCell>
        <mxCell id="ylabel_title" value="&lt;b&gt;初&lt;br&gt;始&lt;br&gt;痰&lt;br&gt;湿&lt;br&gt;积&lt;br&gt;分&lt;br&gt;区&lt;br&gt;间&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="50" y="320" width="40" height="150" as="geometry" />
        </mxCell>
        {cells}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""

    activity = ["&lt;40 严重受限", "40~60 中度", "&gt;=60 优良"]
    phlegm = ["三级 (极高)", "二级 (中度)", "一级 (轻度)"]
    
    # 十六进制颜色渐变 (难到易)
    colors = [
        ["#ff6666", "#ff9966", "#ffcc66"],
        ["#ff9966", "#ffcc66", "#ffff99"],
        ["#ffcc66", "#ffff99", "#ccffcc"]
    ]
    
    strategies = [
        ["强烈(u5)&lt;br&gt;频次5", "强干预(u4)&lt;br&gt;频次4", "中干预(u3)&lt;br&gt;频次4"],
        ["强干预(u4)&lt;br&gt;频次5", "中强(u3)&lt;br&gt;频次3", "常规(u2)&lt;br&gt;频次3"],
        ["中强(u3)&lt;br&gt;频次3", "常规(u2)&lt;br&gt;频次2", "轻微(u1)&lt;br&gt;频次1"]
    ]
    costs = [
        [1800, 1500, 1200],
        [1600, 1200, 900],
        [1200, 900, 500]
    ]

    cells_str = ""
    cell_id_counter = 100
    
    start_x = 200
    start_y = 150
    w = 220
    h = 150
    
    # 绘制X轴标签
    for j, label in enumerate(activity):
        cell_id_counter += 1
        cells_str += f'''
        <mxCell id="x_label_{j}" value="&lt;font style=&quot;font-size: 14px;&quot;&gt;{label}&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=bottom;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="{start_x + j*w}" y="{start_y - 40}" width="{w}" height="30" as="geometry" />
        </mxCell>'''
        
    # 绘制Y轴标签
    for i, label in enumerate(phlegm):
        cell_id_counter += 1
        cells_str += f'''
        <mxCell id="y_label_{i}" value="&lt;font style=&quot;font-size: 14px;&quot;&gt;{label}&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="{start_x - 130}" y="{start_y + i*h}" width="120" height="{h}" as="geometry" />
        </mxCell>'''

    # 绘制方块，气泡，文字
    for i in range(3):
        for j in range(3):
            base_x = start_x + j*w
            base_y = start_y + i*h
            center_x = base_x + w/2
            center_y = base_y + h/2
            
            # 方块底色
            cell_id_counter += 1
            cells_str += f'''
        <mxCell id="rect_{i}_{j}" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor={colors[i][j]};strokeColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="{base_x}" y="{base_y}" width="{w}" height="{h}" as="geometry" />
        </mxCell>'''
            
            # 策略展示卡片（带有动态大小的圆角矩形）
            cell_id_counter += 1
            ratio = (costs[i][j] - 500) / 1300
            shape_w = 130 + ratio * 60  # 宽度从 130 到 190 渐变
            shape_h = 70 + ratio * 40   # 高度从 70 到 110 渐变
            text_val = f"&lt;b&gt;{strategies[i][j]}&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#444444&quot; size=&quot;1&quot;&gt;(预估总成本: {costs[i][j]}元)&lt;/font&gt;"
            cells_str += f'''
        <mxCell id="shape_{i}_{j}" value="{text_val}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;opacity=90;arcSize=20;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="{center_x - shape_w/2}" y="{center_y - shape_h/2}" width="{shape_w}" height="{shape_h}" as="geometry" />
        </mxCell>'''

    with open("4_2_患者特征匹配策略速查图.drawio", "w", encoding="utf-8") as f:
        f.write(xml_template.format(cells=cells_str))
    
    print("Draw.io file generated successfully.")

if __name__ == "__main__":
    generate_drawio()