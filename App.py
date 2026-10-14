
import streamlit as st

st.set_page_config(
    page_title="Tính chỉ số DTI",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 HỆ THỐNG TÍNH CHỈ SỐ DTI")
st.write("Nhập thông tin tài chính của khách hàng để đánh giá khả năng vay vốn.")

st.subheader("1. Thông tin khoản vay")

STV = st.number_input(
    "Số tiền vay (VNĐ)",
    min_value=0,
    value=800_000_000,
    step=10_000_000
)

THV = st.number_input(
    "Thời hạn vay (năm)",
    min_value=1,
    value=5,
    step=1
)

LS = st.number_input(
    "Lãi suất vay (%/năm)",
    min_value=0.0,
    value=12.0,
    step=0.5
)

st.subheader("2. Thông tin tài chính")

TN = st.number_input(
    "Thu nhập hàng tháng (VNĐ)",
    min_value=0,
    value=45_000_000,
    step=1_000_000
)

NC = st.number_input(
    "Nợ cũ phải trả hàng tháng (VNĐ)",
    min_value=0,
    value=10_000_000,
    step=1_000_000
)

CPSH = st.number_input(
    "Chi phí sinh hoạt mỗi người/tháng (VNĐ)",
    min_value=0,
    value=4_000_000,
    step=500_000
)

SN = st.number_input(
    "Số người trong gia đình",
    min_value=1,
    value=3,
    step=1
)

if st.button("TÍNH CHỈ SỐ DTI", type="primary",
             use_container_width=True):

    if TN <= CPSH * SN:
        st.error(
            "Thu nhập không đủ chi trả chi phí sinh hoạt. "
            "Vui lòng kiểm tra lại thông tin."
        )

    elif THV <= 0:
        st.error("Thời hạn vay phải lớn hơn 0.")

    else:
        # Quy đổi lãi suất từ % sang số thập phân
        lai_suat_thang = LS / 100 / 12

        # Tiền gốc phải trả hàng tháng
        tien_goc_thang = STV / (THV * 12)

        # Tiền lãi tháng theo công thức ban đầu
        tien_lai_thang = STV * lai_suat_thang

        # Tổng nghĩa vụ trả nợ hàng tháng
        tong_tra_no = (
            tien_goc_thang
            + tien_lai_thang
            + NC
        )

        # Thu nhập còn lại sau chi phí sinh hoạt
        thu_nhap_con_lai = TN - CPSH * SN

        # Tính chỉ số DTI
        DTI = tong_tra_no / thu_nhap_con_lai

        st.subheader("3. Kết quả đánh giá")

        st.metric(
            label="Chỉ số DTI",
            value=f"{DTI * 100:.2f}%"
        )

        st.progress(min(DTI, 1.0))

        st.write(
            f"**Tổng tiền trả nợ/tháng:** "
            f"{tong_tra_no:,.0f} VNĐ"
        )

        st.write(
            f"**Thu nhập còn lại sau sinh hoạt:** "
            f"{thu_nhap_con_lai:,.0f} VNĐ"
        )

        # Kết luận theo yêu cầu
        if DTI < 0.70:
            st.error(
                " ĐƯỢC VAY "
                "(DTI < 70%)"
            )
        else:
            st.success(
                " KHÔNG ĐƯỢC VAY "
                "(DTI >= 70%)"
            )
