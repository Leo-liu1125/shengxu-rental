import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import io

st.set_page_config(page_title="盛续物业租赁管理系统", page_icon="🏢", layout="wide")

# 完整房间数据（直接嵌入，不依赖外部文件）
ROOMS_DATA = [
    {"房间号": "402", "客户名称": "上海领筹智能科技有限公司", "面积": 108, "状态": "在租", "房租": 10688, "物业费": 3312, "合同开始": "2025-04-01", "合同结束": "2026-03-31"},
    {"房间号": "403", "客户名称": "上海超凡辰信息科技有限公司", "面积": 119, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "2026-01-01", "合同结束": "2027-12-31"},
    {"房间号": "405", "客户名称": "上海昀琦信息科技有限公司", "面积": 119, "状态": "在租", "房租": 14716, "物业费": 4284, "合同开始": "2025-04-15", "合同结束": "2027-04-30"},
    {"房间号": "406", "客户名称": "上海铭绘科技有限公司", "面积": 119, "状态": "在租", "房租": 15716, "物业费": 4284, "合同开始": "2024-06-06", "合同结束": "2026-06-05"},
    {"房间号": "407", "客户名称": "上海辕烽新能源科技有限公司", "面积": 123, "状态": "在租", "房租": 16990, "物业费": 4428, "合同开始": "2024-06-01", "合同结束": "2026-05-31"},
    {"房间号": "409", "客户名称": "上海东凯旭生物科技有限公司", "面积": 396, "状态": "在租", "房租": 22000, "物业费": 5000, "合同开始": "", "合同结束": ""},
    {"房间号": "410", "客户名称": "上海汇景税务师事务所有限公司", "面积": 24, "状态": "在租", "房租": 3636, "物业费": 864, "合同开始": "", "合同结束": ""},
    {"房间号": "411", "客户名称": "叶剑波", "面积": 165, "状态": "在租", "房租": 20060, "物业费": 5940, "合同开始": "2025-06-01", "合同结束": "2027-05-31"},
    {"房间号": "412", "客户名称": "", "面积": 130, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "413", "客户名称": "上海桥羿信息科技有限公司", "面积": 80, "状态": "在租", "房租": 11120, "物业费": 2880, "合同开始": "2024-07-01", "合同结束": "2026-06-30"},
    {"房间号": "415", "客户名称": "上海康佰联网络科技有限公司", "面积": 231, "状态": "在租", "房租": 29309, "物业费": 8316, "合同开始": "2024-08-05", "合同结束": "2026-07-04"},
    {"房间号": "416", "客户名称": "", "面积": 165, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "417", "客户名称": "", "面积": 165, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "418", "客户名称": "上海赛园科技有限公司", "面积": 207, "状态": "在租", "房租": 25000, "物业费": 5000, "合同开始": "", "合同结束": ""},
    {"房间号": "419", "客户名称": "", "面积": 99, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "420", "客户名称": "", "面积": 110, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "421", "客户名称": "上海执幸定岸文化科技有限责任公司", "面积": 110, "状态": "在租", "房租": 13540, "物业费": 3960, "合同开始": "2024-05-15", "合同结束": "2026-05-14"},
    {"房间号": "422", "客户名称": "", "面积": 35, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "423", "客户名称": "上海利敬商和科技有限公司", "面积": 40, "状态": "在租", "房租": 4488, "物业费": 1512, "合同开始": "2024-08-01", "合同结束": "2026-07-31"},
    {"房间号": "425", "客户名称": "上海谦欣乐科技有限公司", "面积": 76, "状态": "在租", "房租": 8264, "物业费": 2736, "合同开始": "2025-07-01", "合同结束": "2027-06-30"},
    {"房间号": "426", "客户名称": "上海英菲姆技术有限公司", "面积": 64, "状态": "在租", "房租": 8696, "物业费": 2304, "合同开始": "2024-09-01", "合同结束": "2026-08-31"},
    {"房间号": "427", "客户名称": "", "面积": 64, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "429", "客户名称": "", "面积": 64, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "431", "客户名称": "上海吉欣教育科技有限公司", "面积": 18, "状态": "在租", "房租": 2636, "物业费": 864, "合同开始": "2024-03-08", "合同结束": "2026-03-07"},
    {"房间号": "432", "客户名称": "", "面积": 40, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "433", "客户名称": "上海阿酷酷信息科技有限公司", "面积": 80, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "2026-01-01", "合同结束": "2027-12-31"},
    {"房间号": "501", "客户名称": "上海盛崴科技服务有限公司", "面积": 163, "状态": "在租", "房租": 21968, "物业费": 4032, "合同开始": "2024-06-01", "合同结束": "2026-09-30"},
    {"房间号": "502", "客户名称": "上海绘蝶教育科技有限公司", "面积": 108, "状态": "在租", "房租": 35904, "物业费": 8172, "合同开始": "2022-03-07", "合同结束": "2027-03-06"},
    {"房间号": "503", "客户名称": "", "面积": 119, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "505", "客户名称": "", "面积": 119, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "506", "客户名称": "上海翀淼科技有限公司", "面积": 119, "状态": "在租", "房租": 14716, "物业费": 4284, "合同开始": "2025-06-01", "合同结束": "2028-05-31"},
    {"房间号": "507", "客户名称": "上海翀淼教育科技有限公司", "面积": 123, "状态": "在租", "房租": 16006, "物业费": 4428, "合同开始": "2024-05-15", "合同结束": "2026-05-14"},
    {"房间号": "508", "客户名称": "上海樊伊翼体育科技有限公司", "面积": 740, "状态": "在租", "房租": 21000, "物业费": 9000, "合同开始": "2023-08-01", "合同结束": "2031-07-31"},
    {"房间号": "509", "客户名称": "上海仰绅信息科技有限公司", "面积": 176, "状态": "在租", "房租": 76163, "物业费": 22536, "合同开始": "2024-10-01", "合同结束": "2029-09-30"},
    {"房间号": "510", "客户名称": "上海至见源信息科技有限公司", "面积": 184, "状态": "在租", "房租": 20000, "物业费": 3875, "合同开始": "", "合同结束": ""},
    {"房间号": "511", "客户名称": "上海翰承艺信息科技有限公司", "面积": 136, "状态": "在租", "房租": 16800, "物业费": 4200, "合同开始": "2025-06-01", "合同结束": "2027-05-31"},
    {"房间号": "512", "客户名称": "", "面积": 156, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "513", "客户名称": "上海迈盛凯信息科技有限公司", "面积": 180, "状态": "在租", "房租": 18894, "物业费": 6106, "合同开始": "2025-04-01", "合同结束": "2027-03-31"},
    {"房间号": "515~517", "客户名称": "上海枫翊信息科技有限公司", "面积": 329, "状态": "在租", "房租": 38960, "物业费": 14040, "合同开始": "2024-12-01", "合同结束": "2026-11-30"},
    {"房间号": "518", "客户名称": "爱托付（上海）科技有限公司", "面积": 73, "状态": "在租", "房租": 8872, "物业费": 2628, "合同开始": "2025-03-01", "合同结束": "2027-02-28"},
    {"房间号": "519", "客户名称": "上海洲支新材料科技有限公司", "面积": 112, "状态": "在租", "房租": 13968, "物业费": 4032, "合同开始": "2024-01-01", "合同结束": "2026-03-09"},
    {"房间号": "520", "客户名称": "上海憬智科技有限公司", "面积": 112, "状态": "在租", "房租": 7696, "物业费": 2304, "合同开始": "2024-07-15", "合同结束": "2026-06-30"},
    {"房间号": "521~525", "客户名称": "上海君汇脉信息科技有限公司", "面积": 266, "状态": "在租", "房租": 22000, "物业费": 3574, "合同开始": "", "合同结束": ""},
    {"房间号": "526", "客户名称": "上海歆梦驰信息科技有限公司", "面积": 101, "状态": "在租", "房租": 10364, "物业费": 3636, "合同开始": "2024-08-01", "合同结束": "2026-07-31"},
    {"房间号": "529", "客户名称": "首誉光控资产管理有限公司", "面积": 18, "状态": "在租", "房租": 1542, "物业费": 792, "合同开始": "2025-08-01", "合同结束": "2026-07-31"},
    {"房间号": "530", "客户名称": "", "面积": 40, "状态": "空置", "房租": 0, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "531", "客户名称": "上海槃岩信息科技有限公司", "面积": 80, "状态": "在租", "房租": 9360, "物业费": 4640, "合同开始": "2023-08-01", "合同结束": "2031-07-31"},
    {"房间号": "532", "客户名称": "上海薇茂信息科技有限公司", "面积": 100, "状态": "在租", "房租": 14000, "物业费": 6000, "合同开始": "2023-08-01", "合同结束": "2031-07-31"},
    {"房间号": "533", "客户名称": "上海葭蕴信息科技有限公司", "面积": 100, "状态": "在租", "房租": 17000, "物业费": 8000, "合同开始": "2023-08-01", "合同结束": "2031-07-31"},
    {"房间号": "3个工位", "客户名称": "叁俩吱空间设计（上海）有限公司", "面积": 315, "状态": "在租", "房租": 3600, "物业费": 0, "合同开始": "", "合同结束": ""},
    {"房间号": "4个工位", "客户名称": "上海全鑫意（上海）智能科技事务所", "面积": 200, "状态": "在租", "房租": 4000, "物业费": 0, "合同开始": "", "合同结束": ""},
]

def get_default_rooms():
    return pd.DataFrame(ROOMS_DATA)

def get_default_expenses():
    return {"房租物业费": 600000, "职工薪酬": 88000, "水电费": 15000, "网络费": 3000, "行政费用": 4000, "交通费": 700, "服务费": 3000, "业务招待费": 3000, "其他": 250}

# 初始化 session state
if 'rooms_df' not in st.session_state:
    st.session_state.rooms_df = get_default_rooms()
if 'expenses' not in st.session_state:
    st.session_state.expenses = get_default_expenses()
if 'initial_balance' not in st.session_state:
    st.session_state.initial_balance = 792846.93
if 'predict_months' not in st.session_state:
    st.session_state.predict_months = 12
if 'monthly_received' not in st.session_state:
    st.session_state.monthly_received = {}
if 'future_predictions' not in st.session_state:
    # 未来出租预测：{房间号: {月份: {状态, 房租, 物业费}}}
    st.session_state.future_predictions = {}

# 侧边栏
with st.sidebar:
    st.title("🏢 盛续物业管理系统")
    st.markdown("---")
    page = st.radio("选择功能模块", ["📋 销控表与应收款", "✏️ 手动修改数据", "🔮 未来出租预测", "💰 现金流预测"], index=0)
    st.markdown("---")
    st.header("📊 数据管理")
    uploaded_file = st.file_uploader("导入 Excel 数据", type=['xlsx', 'xls'])
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state.rooms_df = df
            st.success(f"导入成功！共 {len(df)} 行")
            st.rerun()
        except Exception as e:
            st.error(f"导入失败：{e}")
    if st.button("📥 导出当前数据"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.rooms_df.to_excel(writer, sheet_name='房源销控', index=False)
        output.seek(0)
        st.download_button("下载 Excel", output, "房源数据.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.markdown("---")
    st.header("⏰ 时间设置")
    today = datetime.now()
    current_year = st.number_input("当前年份", 2020, 2030, today.year)
    current_month = st.slider("当前月份", 1, 12, today.month)
    st.session_state.current_date = datetime(current_year, current_month, 1)
    
    st.markdown("---")
    st.markdown("**说明**")
    st.markdown("- **应收**: 合同约定的应收金额")
    st.markdown("- **已收**: 实际收到的金额")
    st.markdown("- **历史月份**: 已收=Excel数据/人工填写")
    st.markdown("- **未来月份**: 已收=0（尚未收到）")

def get_contract_amount(room, month):
    """计算某房间在某月的合同应收金额"""
    status = room.get('状态', '空置')
    contract_start = str(room.get('合同开始', ''))
    contract_end = str(room.get('合同结束', ''))
    
    if status != '在租':
        return 0, '空置'
    
    try:
        if contract_start and contract_start not in ['', 'nan', 'None']:
            start_date = datetime.strptime(contract_start[:10], "%Y-%m-%d")
            if month < start_date:
                return 0, '未起租'
    except:
        pass
    
    try:
        if contract_end and contract_end not in ['', 'nan', 'None']:
            end_date = datetime.strptime(contract_end[:10], "%Y-%m-%d")
            if month > end_date:
                return 0, '已到期'
    except:
        pass
    
    monthly_rent = room.get('房租', 0) or 0
    monthly_fee = room.get('物业费', 0) or 0
    return monthly_rent + monthly_fee, '在租'

def get_receivable_received(room_id, month_str, room, month):
    """获取某房间某月的应收和已收金额"""
    receivable, status = get_contract_amount(room, month)
    
    current_date = st.session_state.get('current_date', datetime.now())
    is_future = month > current_date
    
    # 检查是否有未来出租预测
    if is_future and room_id in st.session_state.future_predictions:
        if month_str in st.session_state.future_predictions[room_id]:
            pred = st.session_state.future_predictions[room_id][month_str]
            receivable = pred.get('房租', 0) + pred.get('物业费', 0)
            status = '预测出租'
    
    if is_future:
        # 未来月份：已收 = 0（还没收到）
        received = 0
    else:
        # 历史月份：已收 = 手动填写的数据
        if room_id in st.session_state.monthly_received:
            received = st.session_state.monthly_received[room_id].get(month_str, 0)
        else:
            received = 0
    
    return receivable, received

# ==================== 页面1: 销控表与应收款 ====================
if page == "📋 销控表与应收款":
    st.title("📋 销控表与月度应收款")
    
    rooms_df = st.session_state.rooms_df.copy()
    current_date = st.session_state.get('current_date', datetime.now())
    
    # 时间范围：从2025年1月到未来12个月
    start_date = datetime(2025, 1, 1)
    months_to_show = (current_date.year - 2025) * 12 + current_date.month + st.session_state.predict_months
    
    month_columns = []
    for i in range(months_to_show):
        month = start_date + relativedelta(months=i)
        month_str = month.strftime("%Y-%m")
        month_columns.append(month_str)
    
    # 统计卡片
    col1, col2, col3, col4, col5 = st.columns(5)
    total_rooms = len(rooms_df)
    rented = len(rooms_df[rooms_df['状态'] == '在租'])
    vacant = len(rooms_df[rooms_df['状态'] == '空置'])
    total_area = rooms_df['面积'].sum() if '面积' in rooms_df.columns else 0
    rented_area = rooms_df[rooms_df['状态'] == '在租']['面积'].sum() if '面积' in rooms_df.columns and len(rooms_df[rooms_df['状态'] == '在租']) > 0 else 0
    
    col1.metric("总房间", total_rooms)
    col2.metric("在租", rented)
    col3.metric("空置", vacant)
    col4.metric("出租率", f"{rented_area/total_area*100:.1f}%" if total_area > 0 else "0%")
    
    current_month_str = current_date.strftime("%Y-%m")
    current_receivable = 0
    for _, room in rooms_df.iterrows():
        r, _ = get_contract_amount(room, current_date)
        current_receivable += r
    col5.metric("本月应收", f"¥{current_receivable:,.0f}")
    
    st.markdown("---")
    
    # 房间基础信息 - 显示全部
    st.subheader("📊 房间基础信息")
    base_cols = ["房间号", "客户名称", "面积", "状态", "房租", "物业费", "合同开始", "合同结束"]
    available_base_cols = [c for c in base_cols if c in rooms_df.columns]
    
    st.dataframe(
        rooms_df[available_base_cols],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # 月度应收款表
    st.subheader("📊 月度应收款明细")
    st.markdown(f"**时间范围**: 2025年1月 - {(start_date + relativedelta(months=months_to_show-1)).strftime('%Y年%m月')} | **当前月份**: {current_date.strftime('%Y年%m月')}")
    
    # 构建月度数据
    detail_rows = []
    
    for idx, room in rooms_df.iterrows():
        room_id = str(room.get('房间号', ''))
        row = {"房间号": room_id, "客户名称": room.get('客户名称', '')}
        
        total_receivable = 0
        total_received = 0
        
        for month_str in month_columns:
            month = datetime.strptime(month_str, "%Y-%m")
            receivable, received = get_receivable_received(room_id, month_str, room, month)
            
            row[f"{month_str}_应收"] = receivable
            row[f"{month_str}_已收"] = received
            
            total_receivable += receivable
            total_received += received
        
        row["应收合计"] = total_receivable
        row["已收合计"] = total_received
        row["未收合计"] = total_receivable - total_received
        
        detail_rows.append(row)
    
    detail_df = pd.DataFrame(detail_rows)
    
    # 月度汇总
    st.markdown("#### 月度汇总")
    
    summary_rows = []
    for month_str in month_columns:
        receivable_total = detail_df[f"{month_str}_应收"].sum()
        received_total = detail_df[f"{month_str}_已收"].sum()
        
        is_current = month_str == current_date.strftime("%Y-%m")
        is_future = datetime.strptime(month_str, "%Y-%m") > current_date
        
        row = {
            "月份": month_str + (" (当前)" if is_current else (" (预测)" if is_future else " (历史)")),
            "应收合计": receivable_total,
            "已收合计": received_total,
            "未收合计": receivable_total - received_total,
            "收缴率": f"{(received_total/receivable_total*100):.1f}%" if receivable_total > 0 else "-"
        }
        summary_rows.append(row)
    
    summary_df = pd.DataFrame(summary_rows)
    
    st.dataframe(
        summary_df.style.format({"应收合计": "¥{:,.0f}", "已收合计": "¥{:,.0f}", "未收合计": "¥{:,.0f}"}),
        use_container_width=True,
        hide_index=True
    )
    
    # 详细明细数据 - 直接显示
    st.markdown("---")
    st.markdown("#### 房间明细数据")
    
    # 只显示汇总列，避免列太多
    summary_cols = ["房间号", "客户名称", "应收合计", "已收合计", "未收合计"]
    st.dataframe(
        detail_df[summary_cols].style.format({"应收合计": "¥{:,.0f}", "已收合计": "¥{:,.0f}", "未收合计": "¥{:,.0f}"}),
        use_container_width=True,
        hide_index=True
    )
    
    # 可展开查看完整月度明细
    with st.expander("📊 查看完整月度明细（按月份）"):
        # 选择月份查看
        selected_month = st.selectbox("选择月份", month_columns, key="detail_month")
        month_detail_cols = ["房间号", "客户名称", f"{selected_month}_应收", f"{selected_month}_已收"]
        st.dataframe(
            detail_df[month_detail_cols].style.format({f"{selected_month}_应收": "¥{:,.0f}", f"{selected_month}_已收": "¥{:,.0f}"}),
            use_container_width=True,
            hide_index=True
        )
    
    # 导出按钮
    st.markdown("---")
    st.markdown("#### 导出Excel")
    
    if st.button("📥 导出完整应收款明细Excel"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            detail_df.to_excel(writer, sheet_name='应收款明细', index=False)
        output.seek(0)
        st.download_button(
            "下载 Excel",
            output,
            "应收款明细.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # 即将到期提醒
    st.markdown("---")
    st.subheader("⚠️ 即将到期合同（3个月内）")
    today = datetime.now()
    three_months = today + relativedelta(months=3)
    expiring = []
    for _, room in rooms_df.iterrows():
        contract_end = str(room.get('合同结束', ''))
        if contract_end and contract_end not in ['', 'nan', 'None'] and room.get('状态') == '在租':
            try:
                end_date = datetime.strptime(contract_end[:10], "%Y-%m-%d")
                if end_date <= three_months and end_date >= today:
                    expiring.append({
                        "房间号": room['房间号'],
                        "客户名称": room.get('客户名称', ''),
                        "合同结束": contract_end[:10],
                        "剩余天数": (end_date - today).days,
                        "月租金": room.get('房租', 0) + room.get('物业费', 0)
                    })
            except:
                pass
    if expiring:
        st.dataframe(pd.DataFrame(expiring).sort_values('剩余天数'), use_container_width=True, hide_index=True)
    else:
        st.info("暂无即将到期的合同")

# ==================== 页面2: 现金流预测 ====================
else:
    st.title("💰 现金流预测")
    st.markdown("基于销控表和已收款数据预测现金流")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ 参数设置")
        st.markdown("**期初现金余额**")
        initial_balance = st.number_input("期初余额（元）", min_value=0.0, value=float(st.session_state.initial_balance), step=10000.0, format="%.2f")
        st.session_state.initial_balance = initial_balance
        
        st.markdown("**固定月度支出**")
        expenses = {}
        total_expense = 0
        for item, amount in st.session_state.expenses.items():
            new_amount = st.number_input(f"{item}", 0, 1000000, int(amount), step=1000, key=f"expense_{item}")
            expenses[item] = new_amount
            total_expense += new_amount
        st.session_state.expenses = expenses
        st.metric("月固定支出合计", f"¥{total_expense:,}")
    
    with col2:
        st.subheader("📊 现金流预测表")
        
        rooms_df = st.session_state.rooms_df
        current_date = st.session_state.get('current_date', datetime.now())
        months = st.session_state.predict_months
        balance = st.session_state.initial_balance
        
        results = []
        for i in range(months):
            month = current_date + relativedelta(months=i)
            month_str = month.strftime("%Y-%m")
            
            income_received = 0  # 已收
            income_receivable = 0  # 应收
            income_unreceived = 0  # 未收
            deposit_refund = 0
            
            for idx, room in rooms_df.iterrows():
                room_id = str(room.get('房间号', ''))
                receivable, received = get_receivable_received(room_id, month_str, room, month)
                income_receivable += receivable
                income_received += received
                income_unreceived += (receivable - received)
            
            # 现金流计算：历史月份用已收，未来月份用应收
            current_date = st.session_state.get('current_date', datetime.now())
            is_future = month > current_date
            cash_income = income_receivable if is_future else income_received
            
            total_expense_month = total_expense + deposit_refund
            balance = balance + cash_income - total_expense_month
            
            results.append({
                "月份": month_str + (" (预测)" if is_future else " (历史)"),
                "期初余额": round(balance - cash_income + total_expense_month, 2),
                "应收租金": round(income_receivable, 2),
                "已收租金": round(income_received, 2),
                "未收租金": round(income_unreceived, 2),
                "现金流": round(cash_income, 2),
                "固定支出": round(total_expense, 2),
                "期末余额": round(balance, 2)
            })
        
        cashflow_df = pd.DataFrame(results)
        
        st.dataframe(
            cashflow_df.style.format({
                "期初余额": "¥{:,.2f}",
                "应收租金": "¥{:,.2f}",
                "已收租金": "¥{:,.2f}",
                "未收租金": "¥{:,.2f}",
                "现金流": "¥{:,.2f}",
                "固定支出": "¥{:,.2f}",
                "期末余额": "¥{:,.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # 未收款汇总（历史月份）
        st.markdown("---")
        st.subheader("📊 历史月份未收款统计")
        historical_df = cashflow_df[~cashflow_df['月份'].str.contains('预测')]
        if len(historical_df) > 0:
            total_unreceived = historical_df['未收租金'].sum()
            total_receivable = historical_df['应收租金'].sum()
            total_received = historical_df['已收租金'].sum()
            col_u1, col_u2, col_u3 = st.columns(3)
            col_u1.metric("历史应收", f"¥{total_receivable:,.0f}")
            col_u2.metric("历史已收", f"¥{total_received:,.0f}")
            col_u3.metric("历史未收", f"¥{total_unreceived:,.0f}", delta=f"收缴率 {total_received/total_receivable*100:.1f}%" if total_receivable > 0 else "")
        
        # 未来月份预测
        st.markdown("---")
        st.subheader("📊 未来月份预测（应收=现金流）")
        future_df = cashflow_df[cashflow_df['月份'].str.contains('预测')]
        if len(future_df) > 0:
            total_future_receivable = future_df['应收租金'].sum()
            st.metric("未来应收合计", f"¥{total_future_receivable:,.0f}")
        
        st.markdown("---")
        st.subheader("📈 现金流趋势")
        chart_df = cashflow_df[['月份', '应收租金', '已收租金', '未收租金', '现金流']].set_index('月份')
        st.bar_chart(chart_df[['应收租金', '已收租金', '未收租金']])
        
        st.markdown("---")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        total_receivable = cashflow_df['应收租金'].sum()
        total_received = cashflow_df['已收租金'].sum()
        total_unreceived = cashflow_df['未收租金'].sum()
        total_cashflow = cashflow_df['现金流'].sum()
        final_balance = cashflow_df['期末余额'].iloc[-1]
        
        col_m1.metric("应收合计", f"¥{total_receivable:,.0f}")
        col_m2.metric("已收合计", f"¥{total_received:,.0f}")
        col_m3.metric("未收合计", f"¥{total_unreceived:,.0f}")
        col_m4.metric("预测期末余额", f"¥{final_balance:,.0f}")

# ==================== 页面3: 手动修改数据 ====================
elif page == "✏️ 手动修改数据":
    st.title("✏️ 手动修改数据")
    st.markdown("手动填写历史月份的已收金额")
    
    current_date = st.session_state.get('current_date', datetime.now())
    
    # 选择房间
    rooms_df = st.session_state.rooms_df
    room_list = rooms_df['房间号'].tolist()
    selected_room = st.selectbox("选择房间", room_list)
    
    if selected_room:
        room_info = rooms_df[rooms_df['房间号'] == selected_room].iloc[0]
        st.markdown(f"**客户名称**: {room_info.get('客户名称', '')}")
        st.markdown(f"**状态**: {room_info.get('状态', '')}")
        st.markdown(f"**房租**: ¥{room_info.get('房租', 0):,.0f}")
        st.markdown(f"**物业费**: ¥{room_info.get('物业费', 0):,.0f}")
        
        st.markdown("---")
        st.subheader("📝 修改已收金额")
        
        # 选择月份（只显示历史月份）
        start_date = datetime(2025, 1, 1)
        historical_months = []
        for i in range(24):
            month = start_date + relativedelta(months=i)
            if month <= current_date:
                historical_months.append(month.strftime("%Y-%m"))
        
        selected_month = st.selectbox("选择月份", historical_months)
        
        if selected_month:
            # 获取当前已收金额
            current_received = 0
            if selected_room in st.session_state.monthly_received:
                current_received = st.session_state.monthly_received[selected_room].get(selected_month, 0)
            
            # 显示应收金额
            month = datetime.strptime(selected_month, "%Y-%m")
            receivable, _ = get_contract_amount(room_info, month)
            
            col_edit1, col_edit2 = st.columns(2)
            with col_edit1:
                st.metric("应收金额", f"¥{receivable:,.0f}")
            with col_edit2:
                new_received = st.number_input(
                    "已收金额", 
                    min_value=0, 
                    max_value=receivable * 2,
                    value=int(current_received),
                    step=1000,
                    key=f"edit_{selected_room}_{selected_month}"
                )
            
            if st.button("保存修改", type="primary"):
                if selected_room not in st.session_state.monthly_received:
                    st.session_state.monthly_received[selected_room] = {}
                st.session_state.monthly_received[selected_room][selected_month] = new_received
                st.success(f"已保存！{selected_room} {selected_month} 已收金额 = ¥{new_received:,.0f}")
    
    # 显示已修改的数据
    st.markdown("---")
    st.subheader("📊 已修改的数据")
    
    if st.session_state.monthly_received:
        modified_data = []
        for room_id, months_data in st.session_state.monthly_received.items():
            for month_str, received in months_data.items():
                if received > 0:
                    modified_data.append({
                        "房间号": room_id,
                        "月份": month_str,
                        "已收金额": received
                    })
        
        if modified_data:
            st.dataframe(pd.DataFrame(modified_data), use_container_width=True, hide_index=True)
        else:
            st.info("暂无修改记录")
    else:
        st.info("暂无修改记录")

# ==================== 页面4: 未来出租预测 ====================
elif page == "🔮 未来出租预测":
    st.title("🔮 未来出租预测")
    st.markdown("预测未来月份的出租房源和租金")
    
    current_date = st.session_state.get('current_date', datetime.now())
    rooms_df = st.session_state.rooms_df
    
    # 显示空置房源
    st.subheader("🏠 当前空置房源")
    vacant_rooms = rooms_df[rooms_df['状态'] == '空置']
    if len(vacant_rooms) > 0:
        st.dataframe(vacant_rooms[['房间号', '客户名称', '面积', '状态']], use_container_width=True, hide_index=True)
    else:
        st.info("暂无空置房源")
    
    st.markdown("---")
    st.subheader("🔮 添加出租预测")
    
    # 选择空置房间
    vacant_room_list = vacant_rooms['房间号'].tolist()
    if vacant_room_list:
        selected_vacant = st.selectbox("选择房间", vacant_room_list, key="predict_room")
        
        if selected_vacant:
            room_info = rooms_df[rooms_df['房间号'] == selected_vacant].iloc[0]
            st.markdown(f"**面积**: {room_info.get('面积', 0)} ㎡")
            
            col_pred1, col_pred2, col_pred3 = st.columns(3)
            
            with col_pred1:
                predict_month = st.date_input(
                    "预计起租日期",
                    value=current_date + relativedelta(months=1),
                    key="predict_date"
                )
            
            with col_pred2:
                predict_rent = st.number_input(
                    "预测月租金",
                    min_value=0,
                    value=int(room_info.get('房租', 0) or 10000),
                    step=500,
                    key="predict_rent"
                )
            
            with col_pred3:
                predict_fee = st.number_input(
                    "预测月物业费",
                    min_value=0,
                    value=int(room_info.get('物业费', 0) or 2000),
                    step=100,
                    key="predict_fee"
                )
            
            predict_tenant = st.text_input("预测租户名称（可选）", key="predict_tenant")
            
            if st.button("添加预测", type="primary"):
                if selected_vacant not in st.session_state.future_predictions:
                    st.session_state.future_predictions[selected_vacant] = {}
                
                month_str = predict_month.strftime("%Y-%m")
                st.session_state.future_predictions[selected_vacant][month_str] = {
                    "状态": "预测出租",
                    "房租": predict_rent,
                    "物业费": predict_fee,
                    "租户": predict_tenant
                }
                st.success(f"已添加预测！{selected_vacant} 预计 {month_str} 出租")
    
    # 显示已添加的预测
    st.markdown("---")
    st.subheader("📊 出租预测列表")
    
    if st.session_state.future_predictions:
        predict_data = []
        for room_id, predictions in st.session_state.future_predictions.items():
            for month_str, pred in predictions.items():
                predict_data.append({
                    "房间号": room_id,
                    "预计起租": month_str,
                    "预测租户": pred.get('租户', ''),
                    "预测房租": f"¥{pred.get('房租', 0):,.0f}",
                    "预测物业费": f"¥{pred.get('物业费', 0):,.0f}"
                })
        
        if predict_data:
            st.dataframe(pd.DataFrame(predict_data), use_container_width=True, hide_index=True)
            
            # 清除预测按钮
            if st.button("清除所有预测"):
                st.session_state.future_predictions = {}
                st.success("已清除所有预测")
                st.rerun()
        else:
            st.info("暂无预测记录")
    else:
        st.info("暂无预测记录")

st.markdown("---")
st.markdown("<center>盛续物业租赁管理系统 © 2026 | 共51个房间 | 时间范围：2025年1月起</center>", unsafe_allow_html=True)