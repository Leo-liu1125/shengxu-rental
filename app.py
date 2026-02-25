import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import io
import openpyxl

# 页面配置
st.set_page_config(
    page_title="盛续物业租赁管理系统",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 样式
st.markdown("""
<style>
    .status-rented { background-color: #F0FFF0 !important; }
    .status-vacant { background-color: #E6E6FA !important; }
    .status-expiring { background-color: #FFE4B5 !important; }
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 初始化数据 ====================
def get_default_rooms():
    """默认房间数据（基于你的Excel）"""
    return pd.DataFrame([
        {"房间号": "402", "客户名称": "上海领筹智能科技有限公司", "面积": 108, "状态": "在租", 
         "月租金": 10688, "月物业费": 3312, "合同开始": "2025-04-01", "合同结束": "2026-03-31", "押金": 42000},
        {"房间号": "403", "客户名称": "", "面积": 119, "状态": "空置", 
         "月租金": 14000, "月物业费": 4000, "合同开始": "", "合同结束": "", "押金": 0},
        {"房间号": "405", "客户名称": "上海昀琦信息科技有限公司", "面积": 119, "状态": "在租", 
         "月租金": 14716, "月物业费": 4284, "合同开始": "2025-04-15", "合同结束": "2027-04-30", "押金": 57000},
        {"房间号": "406", "客户名称": "上海铭绘科技有限公司", "面积": 119, "状态": "在租", 
         "月租金": 15716, "月物业费": 4284, "合同开始": "2024-06-06", "合同结束": "2026-06-05", "押金": 60000},
        {"房间号": "407", "客户名称": "上海辕烽新能源科技有限公司", "面积": 123, "状态": "在租", 
         "月租金": 16990, "月物业费": 4428, "合同开始": "2024-06-01", "合同结束": "2026-05-31", "押金": 64254},
        {"房间号": "409", "客户名称": "上海东凯旭生物科技有限公司", "面积": 396, "状态": "在租", 
         "月租金": 22000, "月物业费": 5000, "合同开始": "2024-08-01", "合同结束": "2026-07-31", "押金": 81000},
        {"房间号": "410", "客户名称": "上海汇景税务师事务所有限公司", "面积": 24, "状态": "在租", 
         "月租金": 3636, "月物业费": 864, "合同开始": "2024-03-08", "合同结束": "2026-03-07", "押金": 13500},
        {"房间号": "411", "客户名称": "叶剑波", "面积": 165, "状态": "在租", 
         "月租金": 20060, "月物业费": 5940, "合同开始": "2025-06-01", "合同结束": "2027-05-31", "押金": 78000},
        {"房间号": "412", "客户名称": "", "面积": 130, "状态": "空置", 
         "月租金": 14000, "月物业费": 4000, "合同开始": "", "合同结束": "", "押金": 0},
        {"房间号": "413", "客户名称": "上海桥羿信息科技有限公司", "面积": 80, "状态": "在租", 
         "月租金": 11120, "月物业费": 2880, "合同开始": "2024-07-01", "合同结束": "2026-06-30", "押金": 42000},
        {"房间号": "415", "客户名称": "上海康佰联网络科技有限公司", "面积": 231, "状态": "在租", 
         "月租金": 29309, "月物业费": 8316, "合同开始": "2024-08-05", "合同结束": "2026-07-04", "押金": 112875},
        {"房间号": "416", "客户名称": "", "面积": 165, "状态": "空置", 
         "月租金": 26500, "月物业费": 6500, "合同开始": "", "合同结束": "", "押金": 0},
        {"房间号": "417", "客户名称": "", "面积": 165, "状态": "空置", 
         "月租金": 26500, "月物业费": 6500, "合同开始": "", "合同结束": "", "押金": 0},
        {"房间号": "418", "客户名称": "上海赛园科技有限公司", "面积": 207, "状态": "在租", 
         "月租金": 25000, "月物业费": 5000, "合同开始": "2024-09-01", "合同结束": "2026-08-31", "押金": 90000},
        {"房间号": "421", "客户名称": "上海执幸定岸文化科技有限责任公司", "面积": 110, "状态": "在租", 
         "月租金": 13540, "月物业费": 3960, "合同开始": "2024-05-15", "合同结束": "2026-05-14", "押金": 52500},
        {"房间号": "423", "客户名称": "上海利敬商和科技有限公司", "面积": 40, "状态": "在租", 
         "月租金": 4488, "月物业费": 1512, "合同开始": "2024-08-01", "合同结束": "2026-07-31", "押金": 18000},
        {"房间号": "425", "客户名称": "上海谦欣乐科技有限公司", "面积": 76, "状态": "在租", 
         "月租金": 8264, "月物业费": 2736, "合同开始": "2025-07-01", "合同结束": "2027-06-30", "押金": 33000},
        {"房间号": "426", "客户名称": "上海英菲姆技术有限公司", "面积": 64, "状态": "在租", 
         "月租金": 8696, "月物业费": 2304, "合同开始": "2024-09-01", "合同结束": "2026-08-31", "押金": 33000},
        {"房间号": "431", "客户名称": "上海吉欣教育科技有限公司", "面积": 18, "状态": "在租", 
         "月租金": 2636, "月物业费": 864, "合同开始": "2024-03-08", "合同结束": "2026-03-07", "押金": 10500},
        {"房间号": "501", "客户名称": "上海盛崴科技服务有限公司", "面积": 163, "状态": "在租", 
         "月租金": 21968, "月物业费": 4032, "合同开始": "2024-06-01", "合同结束": "2026-09-30", "押金": 78000},
        {"房间号": "502", "客户名称": "上海绘蝶教育科技有限公司", "面积": 108, "状态": "在租", 
         "月租金": 35904, "月物业费": 8172, "合同开始": "2022-03-07", "合同结束": "2027-03-06", "押金": 132228},
    ])

def get_default_expenses():
    """默认固定支出"""
    return {
        "房租物业费": 600000,
        "职工薪酬": 88000,
        "水电费": 15000,
        "网络费": 3000,
        "行政费用": 4000,
        "交通费": 700,
        "服务费": 3000,
        "业务招待费": 3000,
        "其他": 250
    }

# Session state
if 'rooms_df' not in st.session_state:
    st.session_state.rooms_df = get_default_rooms()

if 'expenses' not in st.session_state:
    st.session_state.expenses = get_default_expenses()

if 'initial_balance' not in st.session_state:
    st.session_state.initial_balance = 792846.93  # 2026年期初余额

if 'predict_months' not in st.session_state:
    st.session_state.predict_months = 12

# ==================== 侧边栏 ====================
with st.sidebar:
    st.title("🏢 盛续物业管理系统")
    st.markdown("---")
    
    page = st.radio(
        "选择功能模块",
        ["📋 房屋销控表", "💰 现金流预测"],
        index=0
    )
    
    st.markdown("---")
    st.header("📊 数据管理")
    
    # 导入Excel
    uploaded_file = st.file_uploader("导入 Excel 数据", type=['xlsx', 'xls'])
    if uploaded_file:
        try:
            # 尝试读取应收款台账sheet
            xl = pd.ExcelFile(uploaded_file)
            if '2025-2026应收款台账' in xl.sheet_names:
                df = pd.read_excel(uploaded_file, sheet_name='2025-2026应收款台账', header=1)
                st.success(f"检测到应收款台账，共 {len(df)} 行")
            else:
                df = pd.read_excel(uploaded_file)
            st.session_state.rooms_df = df
            st.rerun()
        except Exception as e:
            st.error(f"导入失败：{e}")
    
    # 导出Excel
    if st.button("📥 导出当前数据"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.rooms_df.to_excel(writer, sheet_name='房源销控', index=False)
            
            # 创建现金流预测sheet
            cf_df = calculate_cashflow_preview()
            cf_df.to_excel(writer, sheet_name='现金流预测', index=False)
            
        output.seek(0)
        st.download_button(
            "下载 Excel 文件",
            output,
            "盛续物业数据.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ==================== 计算函数 ====================
def calculate_cashflow_preview():
    """预览现金流计算"""
    rooms_df = st.session_state.rooms_df
    expenses = st.session_state.expenses
    initial_balance = st.session_state.initial_balance
    months = st.session_state.predict_months
    
    start_date = datetime.now()
    results = []
    balance = initial_balance
    
    for i in range(months):
        month = start_date + relativedelta(months=i)
        month_str = month.strftime("%Y-%m")
        
        # 计算当月收入
        income = 0
        deposit_refund = 0
        
        for _, room in rooms_df.iterrows():
            status = room.get('状态', '空置')
            contract_end = room.get('合同结束', '')
            
            if status == '在租':
                monthly_rent = room.get('月租金', 0) or 0
                monthly_fee = room.get('月物业费', 0) or 0
                income += monthly_rent + monthly_fee
                
                # 检查合同是否本月到期，需要退押金
                if contract_end:
                    try:
                        end_date = datetime.strptime(str(contract_end), "%Y-%m-%d")
                        # 合同结束当月退押金
                        if month.year == end_date.year and month.month == end_date.month:
                            deposit = room.get('押金', 0) or 0
                            deposit_refund += deposit
                    except:
                        pass
        
        # 固定支出
        total_expense = sum(expenses.values()) + deposit_refund
        
        # 期末余额
        balance = balance + income - total_expense
        
        results.append({
            "月份": month_str,
            "期初余额": round(balance - income + total_expense, 2),
            "租金收入": round(income, 2),
            "固定支出": round(sum(expenses.values()), 2),
            "退押金": round(deposit_refund, 2),
            "支出合计": round(total_expense, 2),
            "期末余额": round(balance, 2)
        })
    
    return pd.DataFrame(results)

# ==================== 页面1: 房屋销控表 ====================
if page == "📋 房屋销控表":
    st.title("📋 房屋销控表")
    st.markdown("管理所有房间的租赁状态、合同信息")
    
    # 统计卡片
    col1, col2, col3, col4 = st.columns(4)
    rooms_df = st.session_state.rooms_df
    
    total_rooms = len(rooms_df)
    rented = len(rooms_df[rooms_df['状态'] == '在租'])
    vacant = len(rooms_df[rooms_df['状态'] == '空置'])
    total_area = rooms_df['面积'].sum()
    rented_area = rooms_df[rooms_df['状态'] == '在租']['面积'].sum()
    
    col1.metric("总房间数", total_rooms)
    col2.metric("在租", rented, f"{rented/total_rooms*100:.1f}%")
    col3.metric("空置", vacant, f"{vacant/total_rooms*100:.1f}%")
    col4.metric("出租率", f"{rented_area/total_area*100:.1f}%")
    
    st.markdown("---")
    
    # 数据编辑器
    edited_df = st.data_editor(
        rooms_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "状态": st.column_config.SelectboxColumn(
                "状态",
                options=["在租", "空置", "即将到期"],
                required=True,
            ),
            "合同开始": st.column_config.DateColumn("合同开始", format="YYYY-MM-DD"),
            "合同结束": st.column_config.DateColumn("合同结束", format="YYYY-MM-DD"),
            "月租金": st.column_config.NumberColumn("月租金", format="¥%,d"),
            "月物业费": st.column_config.NumberColumn("月物业费", format="¥%,d"),
            "押金": st.column_config.NumberColumn("押金", format="¥%,d"),
            "面积": st.column_config.NumberColumn("面积 (㎡)", format="%d"),
        },
        hide_index=True,
    )
    
    if not edited_df.equals(st.session_state.rooms_df):
        st.session_state.rooms_df = edited_df
        st.success("数据已更新！")
    
    # 即将到期提醒
    st.markdown("---")
    st.subheader("⚠️ 即将到期合同（3个月内）")
    
    today = datetime.now()
    three_months_later = today + relativedelta(months=3)
    
    expiring = []
    for _, room in rooms_df.iterrows():
        contract_end = room.get('合同结束', '')
        if contract_end and room.get('状态') == '在租':
            try:
                end_date = datetime.strptime(str(contract_end), "%Y-%m-%d")
                if end_date <= three_months_later and end_date >= today:
                    expiring.append({
                        "房间号": room['房间号'],
                        "客户名称": room['客户名称'],
                        "合同结束": contract_end,
                        "剩余天数": (end_date - today).days,
                        "押金": room.get('押金', 0)
                    })
            except:
                pass
    
    if expiring:
        expiring_df = pd.DataFrame(expiring).sort_values('剩余天数')
        st.dataframe(expiring_df, use_container_width=True, hide_index=True)
    else:
        st.info("暂无即将到期的合同")

# ==================== 页面2: 现金流预测 ====================
else:
    st.title("💰 现金流预测")
    st.markdown("基于销控表自动预测未来现金流")
    
    # 参数设置
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ 参数设置")
        
        st.markdown("**期初现金余额**")
        initial_balance = st.number_input(
            "期初余额（元）",
            min_value=0.0,
            value=float(st.session_state.initial_balance),
            step=10000.0,
            format="%.2f"
        )
        st.session_state.initial_balance = initial_balance
        
        st.markdown("**预测月数**")
        months = st.slider("月数", 3, 24, st.session_state.predict_months)
        st.session_state.predict_months = months
        
        st.markdown("**固定月度支出**")
        expenses = {}
        total_expense = 0
        for item, amount in st.session_state.expenses.items():
            new_amount = st.number_input(
                f"{item}",
                0, 1000000, 
                int(amount), 
                step=1000,
                key=f"expense_{item}"
            )
            expenses[item] = new_amount
            total_expense += new_amount
        st.session_state.expenses = expenses
        
        st.metric("月固定支出合计", f"¥{total_expense:,}")
    
    with col2:
        st.subheader("📊 现金流预测表")
        
        # 计算现金流
        cashflow_df = calculate_cashflow_preview()
        
        # 显示表格
        st.dataframe(
            cashflow_df.style.format({
                "期初余额": "¥{:,.2f}",
                "租金收入": "¥{:,.2f}",
                "固定支出": "¥{:,.2f}",
                "退押金": "¥{:,.2f}",
                "支出合计": "¥{:,.2f}",
                "期末余额": "¥{:,.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # 图表
        st.markdown("---")
        st.subheader("📈 现金流趋势")
        
        chart_df = cashflow_df[['月份', '租金收入', '支出合计', '期末余额']].set_index('月份')
        st.line_chart(chart_df)
        
        # 汇总指标
        st.markdown("---")
        col_m1, col_m2, col_m3 = st.columns(3)
        
        total_income = cashflow_df['租金收入'].sum()
        total_outcome = cashflow_df['支出合计'].sum()
        final_balance = cashflow_df['期末余额'].iloc[-1]
        
        col_m1.metric(f"{months}个月总收入", f"¥{total_income:,.0f}")
        col_m2.metric(f"{months}个月总支出", f"¥{total_outcome:,.0f}")
        col_m3.metric("预测期末余额", f"¥{final_balance:,.0f}", 
                      delta=f"{'+' if final_balance > initial_balance else ''}{final_balance - initial_balance:,.0f}")

# 页脚
st.markdown("---")
st.markdown("<center>盛续物业租赁管理系统 © 2026 | 数据基于 Excel 表格结构设计</center>", 
            unsafe_allow_html=True)